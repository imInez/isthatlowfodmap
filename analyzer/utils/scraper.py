import json
import re

import requests
from bs4 import BeautifulSoup


class Meal:
    def __init__(self, url, name, ingredients, images):
        self.url = url
        self.name = name
        self.ingredients = ingredients
        self.images = images

    def print(self):
        print('link: {}'.format(self.url))
        print('name: {}'.format(self.name))
        print('ingredients:\n{}'.format(self.ingredients))
        print('images:\n{}'.format(self.images))


class Scraper:
    def get_url(self, url):
        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                                 'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;'
                             'q=0.9,image/webp,*/*;q=0.8'}
        try:
            req = session.get(url, headers=headers).text
        except requests.exceptions.RequestException:
            raise
        return BeautifulSoup(req, 'lxml')

    def find_name(self, page_obj, url):
        # get name of a meal
        # try from h
        header = page_obj.select('h1')
        if header is not None and len(header) > 0:
            return str(set(h.get_text() for h in header)).strip('{}')
        # try from slug
        name_from_url = url.split('/')[-1].replace('-', ' ') if '-' in url.split('/')[-1] else None
        if name_from_url is not None and len(name_from_url) > 0:
            return name_from_url
        # try from first class with *header
        header_class = page_obj.find(attrs={'class': re.compile('[a-zA-Z]*-*header|[a-zA-Z]*|-*')})
        if header_class is not None and len(header_class) > 0:
            return '\n'.join(h for h in header_class)

    def find_ingredients_keyword_tag(self, page_obj):
        # search for tag where ingredients word is
        ingr = page_obj.find_all(['h2', 'h3', 'h4', 'h5', 'span', 'p', 'strong', 'div'],
                                 text=re.compile('Składniki|Składniki:|SKŁADNIKI|SKŁADNIKI:|składniki:|składniki'
                                                 'INGREDIENTS|Ingredients|ingredients:|INGREDIENTS:|ingredients'))
        if len(ingr) == 0:
            return None
        if len(ingr) == 1:
            return ingr[0]
        else:
            # check if one tag is in another
            not_duplicate = [tag for tag in ingr if not tag.findChildren()]
            if len(not_duplicate) == 1:
                return not_duplicate[0]
            # alphabetical sort will be ok to get headers first, then span, then p
            tags = sorted([tag.name for tag in ingr])
            tag = [tag for tag in ingr if tag.name == tags[0]]
            return tag[0]

    def get_parent(self, tag):
        return tag.parent

    def check_if_more_content(self, tag):
        if len(tag.find_all('p')) > 5:
            return True
        return False


    def find_ingredients_by_keyword(self, page_obj):
        ingredients_keyword_tag = self.find_ingredients_keyword_tag(page_obj)
        check = None
        if ingredients_keyword_tag is not None:
            try:
                parent = self.get_parent(ingredients_keyword_tag)
                if self.check_if_more_content(parent) is True:
                    check =  self.check_popular(check_gen=ingredients_keyword_tag.next_siblings, check_list=True)
                    if check is not None:
                        return check
                else:
                    while check is None:
                        check = self.check_popular(check_tag=parent, check_list=True)
                        if check is not None:
                            return check
                        check = self.check_popular(check_gen=parent.next_siblings, check_list=True)
                        if check is not None:
                            return check
                        parent = self.get_parent(parent)
            except:
                raise

    def check_popular(self, check_tag=None, check_gen=None, check_list=False):
        if check_gen:
            for item in check_gen:
                if self.check_popular(check_tag=item):
                    return self.check_popular(check_tag=item)
        if check_tag:
            check_item_popular = self.find_ingredients_by_popular(tag=check_tag)
            if check_item_popular:
                item_popular = check_tag
                if check_list is True:
                        found_list = item_popular.find_all('ul')
                        if found_list:
                            return self.check_popular(check_gen=found_list)
                        else:
                            return item_popular.get_text(separator="\n")
                else:
                    return item_popular.get_text(separator="\n")
            else:
                return None


    def find_ingredients_by_popular(self, page_obj=None, tag=None):
        # searched = tag if tag else page_obj
        popular_ingredients = ['cukier', 'cukru ', 'miód', 'miodu', 'sól', 'soli', 'pieprz', 'pieprzu',
                               'mąka', 'mąki', 'masło', 'masła', 'jaja', 'jajka', 'jajek',
                               'śmietana', 'śmietany', 'mleko', 'mleka', 'ser', 'sera',
                               'cebula', 'cebuli', 'cebul', 'czosnek', 'czosnku'
                               'sugar', 'honey', 'salt', 'pepper', 'flour', 'butter', 'egg', 'eggs', 'milk', 'cream',
                               'onion', 'garlic', 'cheese']
        found_tags = []
        if tag:
            for ingr in popular_ingredients:
                try:
                    found = tag.find(string=re.compile(ingr))
                except TypeError:  # found a string
                    continue
                if found is not None:
                    found_tags.append(found)
            return True if found_tags else None
        if page_obj:
            section = None
            for ingr in popular_ingredients:
                found = page_obj.find(string=re.compile(ingr))
                if any(element in str(found) for element in ['@', '{', '}', 'href']): found = None
                # print('\n' * 5, 'FOUND INGR: ', ingr, 'IN: ', found, 'of type: ', type(found))
                if found is not None:
                    found_tags.append(found)
                    try:
                        found = found.parent  # found is NavigableString as above looks for string so get it's parent
                        while section is None:
                            if found.name in ['ul', 'div']:
                                section = True
                            else:
                                found = self.get_parent(found)
                        return found.get_text(separator='\n')
                    except AttributeError:
                        return found_tags


    def check_for_schema(self, ingredients):
        if "recipeIngredient" in ''.join(ingredients):
            schema = json.loads(''.join(ingredients))
            return ','.join(schema["recipeIngredient"])
        else:
            return ingredients

    def find_ingredients(self, page_obj):
        # if found 'ingredients' look around for ingredients list
        ingredients = self.find_ingredients_by_keyword(page_obj)
        if ingredients:
            ingredients = self.check_for_schema(ingredients)
            return ingredients
        # if ingredients tag is None, search for popular products in body
        else:
            ingredients = self.find_ingredients_by_popular(page_obj=page_obj)
            if ingredients:
                ingredients = self.check_for_schema(ingredients)
                return ingredients

    def find_images(self, page_obj):
        images = [img['src'] for img in page_obj.find_all('img') if img.has_attr('src')and
                      img['src'].lower().startswith(('http', 'www.', '//')) and (
                        img['src'].lower().endswith(('.png', '.jpg', '.jpeg')) or
                        '.jpg?' in img['src'])]
        return images

    def parse(self, url):
        soup = self.get_url(url)
        if soup is not None:
            name = self.find_name(soup, url)
            ingredients = self.find_ingredients(soup)
            images = self.find_images(soup)
            meal = Meal(url, name, str(ingredients).strip(), images)
            return meal

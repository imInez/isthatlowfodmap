import re
import requests
from bs4 import BeautifulSoup
import lxml
import json
from PIL import Image
from urllib import request

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
        print('*'*200)

class LinkedWebsite:
    def __init__(self, url):
        self.url = url


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
                                 text=re.compile('Składniki|Składniki:|SKŁADNIKI|SKŁADNIKI:|składniki:|'
                                                 'INGREDIENTS|Ingredients|ingredients:|INGREDIENTS:'))
        # print('\n'*5, "INGR KEYWORDS: ", ingr)
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
        print("KEYWORD TAG: ", ingredients_keyword_tag)
        check = None
        if ingredients_keyword_tag is not None:
            try:
                parent = self.get_parent(ingredients_keyword_tag)
                if self.check_if_more_content(parent) is True:
                    print('\n'*5,"PARENT HAS MORE CONTENT")
                    check =  self.check_popular(check_gen=ingredients_keyword_tag.next_siblings, check_list=True)
                    if check is not None:
                        print('\n'*5,"RETURNED FROM MORE CONTENT: ", check)
                        return check
                else:
                    while check is None:
                        print('\n'*5,'CHECKING PARENT: ', parent)
                        check = self.check_popular(check_tag=parent, check_list=True)
                        print('\n'*5,"RETURNED: ", check)
                        if check is not None:
                            print('\n'*5,'FOUND IN PARENT: ', check)
                            found = check
                            return check
                        check = self.check_popular(check_gen=parent.next_siblings, check_list=True)
                        if check is not None:
                            print('FOUND IN PARENT SIBLING: ', check)
                            found = check
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
            # print('\n'*5,"CHECKING TAG: ", check_tag)
            check_item_popular = self.find_ingredients_by_popular(tag=check_tag)
            # print('\n'*5,"CHECK ITEM POPULAR: ", check_item_popular)
            if check_item_popular:
                item_popular = check_tag
                # print('\n' * 5, "ITEM POPULAR: ", item_popular)
                if check_list is True:
                        # print("SEARCHING FOR LIST")
                        found_list = item_popular.find_all('ul')
                        # print('\n'*5,'FOUND LIST: ', str(found_list),  type(found_list))
                        if found_list:
                            # print('\n'*5,"LEN FOUND LIST: ", len(found_list), found_list)
                            return self.check_popular(check_gen=found_list)
                        else:
                            # print('NO LIST HERE, returning item')
                            return item_popular.get_text(separator="\n")
                else:
                    # print('\n' * 5, 'RETURNING: ', item_popular)
                    return item_popular.get_text(separator="\n")
            else:
                # print('\n'*5,"NO POPULAR ")
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
            # print('\n'*5, 'CHECKING TAG BY POPULAR: ', tag)
            for ingr in popular_ingredients:
                try:
                    found = tag.find(string=re.compile(ingr))
                except TypeError:  # found a string
                    continue
                if found is not None:
                    found_tags.append(found)
            # print("FOUND TAGS: ", found_tags)
            return True if found_tags else None
        if page_obj:
            # print('\n' * 5, 'CHECKING PAGE: ')
            section = None
            for ingr in popular_ingredients:
                found = page_obj.find(string=re.compile(ingr))
                print("FOUND: ", found)
                if any(element in str(found) for element in ['@', '{', '}', 'href']): found = None
                # print('\n' * 5, 'FOUND INGR: ', ingr, 'IN: ', found, 'of type: ', type(found))
                if found is not None:
                    found_tags.append(found)
                    try:
                        found = found.parent  # found is NavigableString as above looks for string so get it's parent
                        # print('\n' * 5, 'CHECKING TAG PARENT: ', found)
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
            # print("SCHEMA: ", schema)
            return ','.join(schema["recipeIngredient"])
        else:
            return ingredients

    def find_ingredients(self, page_obj):
        # if found 'ingredients' look around for ingredients list
        ingredients = self.find_ingredients_by_keyword(page_obj)
        if ingredients:
            print('INGREDIENTS FROM KEYWORD: ', ingredients)
            ingredients = self.check_for_schema(ingredients)
            return ingredients
        # if ingredients tag is None, search for popular products in body
        else:
            ingredients = self.find_ingredients_by_popular(page_obj=page_obj)
            if ingredients:
                print('INGREDIENTS FROM POPULAR: ', ingredients)
                ingredients = self.check_for_schema(ingredients)
                return ingredients

    def find_images(self, page_obj):
        images_all = [img['src'] for img in page_obj.find_all('img') if img.has_attr('src')and
                      img['src'].lower().startswith(('http', 'www.', '//')) and (
                        img['src'].lower().endswith(('.png', '.jpg', '.jpeg')) or
                        'jpg?' in img['src'])]
        images = []
        # TODO this is taking too long
        images = images_all
        # print('IMAGES ALL: ', images_all)
        return images

    def parse(self, url):
        soup = self.get_url(url)
        if soup is not None:
            name = self.find_name(soup, url)
            print('NAME: ', name)
            ingredients = self.find_ingredients(soup)
            images = self.find_images(soup)
            meal = Meal(url, name, str(ingredients).strip(), images)
            # print('scraper INGREDIENTS: ', ingredients.strip())
            # print('type scraper INGREDIENTS: ', type(ingredients.strip()))
            return meal

# TODO if name is a list, check if theres any ingrdient and choose this
# TODO remove /r from title

pages = [
    # 'https://gotowanie.onet.pl/przepisy/schabowe-z-piekarnika/nbntkgd', #fail - glowne skladniki

    # 'http://www.lunchoteka.com/kalafiorowe-curry-z-ciecierzyca/', #fail due to tags on page :(

    # 'http://ewawachowicz.pl/przepisy,1,1283.html', #weird formatting

    # 'https://uwielbiam.pl/przepis/kokosowe-pancakes-z-borowkami-i-platkami-lubella-duo-caramel', - osobno miary
    # 'https://www.przepisy.pl/przepis/kaszotto-z-burakami-serem-kozim-i-pestkami-slonecznika', - measurments separate
    # 'https://www.przepisy.pl/przepis/salatka-z-rukola-i-truskawkami', # steps included

    # 'https://www.doradcasmaku.pl/przepis-co-na-obiad-schab-po-chinsku-wg-piotra-oginskiego-411041', # measurments are seperate # captcha :D
    # 'https://www.agamasmaka.pl/2019/11/bezglutenowy-murzynek-z-marchewka-bez-jajek-bez-kakao.html', # captcha
    # 'https://www.kuchniaplus.pl/przepisy/poledwiczki-w-sosie-tunczykowym', # captcha

    # 'https://cookingforemily.pl/2017/05/gofry-ze-szpinakiem-i-truskawkami/',
    # 'https://www.fodmap.pl/chleb-low-fodmap/',
    # 'https://www.kwestiasmaku.com/przepis/salatka-z-gruszka-suszona-szynka-i-orzechami-wloskimi',
    # 'https://www.mniammniam.com/tort-kanapkowy-z-pasta-jajeczna',
    # 'http://wielkiezarcie.com/przepisy/ciasto-jablkowe-z-orzechowa-polewa-14452135208050114926',
    # 'http://beszamel.se.pl/wegetarianskie/mujadara-pyszny-ryz-z-soczewica-i-chrupiaca-cebulka,20951/',
    # 'https://aniagotuje.pl/przepis/salatka-z-wedzonym-kurczakiem',
    # 'https://pysznosci.pl/przepisy/drozdzowki-z-jablkami-domowej-roboty/',
    # 'https://www.winiary.pl/przepis.aspx/141151/omlet-tex-mex-z-papryka-szynka-pomidorami-i-kukurydza',
    # 'https://www.przyslijprzepis.pl/przepis/zupa-krem-z-dyni-na-soku-z-pomaranczy',
    # "https://kuchnialidla.pl/razowe-grzanki-z-musem-z-awokado-i-wedzonym-lososiem",
    # http://niebonatalerzu.pl/2019/10/spaghetti-bazylia-orzeszkami-parmezanem.html,
    # 'https://www.winiary.pl/przepis.aspx/138679/bagietka-z-kurczakiem',
    # 'https://www.olgasmile.com/makaron-z-kurkami-i-szpinakiem.html',
    # 'http://wielkiezarcie.com/przepisy/ziemniaki-w-panierce-9871633111520561407',
    # 'https://www.ofeminin.pl/kuchnia/przepisy/fit-leczo-z-cukinii-z-patelni-smaczny-i-szybki-przepis/b6ys8bt',
    # 'https://smaker.pl/przepisy-dania-glowne/przepis-dahl-z-czerwonej-soczewicy-i-buraka-z-domowym-serkiem-i-pesto-z-pietruszki,176374,healthycreations.html',
    # 'https://przepisytradycyjne.pl/kruche-ciastka-bez-cukru/',
    # 'https://zakochanewzupach.pl/ajo-blanco-czyli-hiszpanski-chlodnik-z-migdalow-i-czosnku/',
    # 'https://hpba.pl/nasze-ulubione-gofry/,
    # 'http://agnieszkamaciag.pl/ciasto-ze-sliwkami/',
    # 'https://przepisyjoli.com/2019/06/chlodnik-najlepsza-zupa-na-upaly-przepis-domowy/',
    # 'https://www.dorotakaminska.pl/ciasto-z-gruszkami/',
    # 'https://www.przepisownia.pl/przystawkisalatki-przepisy/hot-dogi/bmlglu10-1876a-218659-cfcd2-9qttgicb',
    # 'https://kuron.com.pl/artykuly/przepisy/salatki/salatka-z-tunczykiem-i-sosem-tysiaca-wysp/',
    # 'https://www.kamis.pl/przepisy/ciasta-desery-napoje/tosty-z-babki-z-malinami',

]

# scraper = Scraper()
#
# for page in pages:
#     meal = scraper.parse(page)
# print(meal.print())
#


# TODO nie moge znalezc skladnikow dla: name, prosze wklej te tutaj
# TODO background-image
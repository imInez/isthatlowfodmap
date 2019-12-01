""" Ingredients checker """
import json
import os
import re
import unicodedata


class IngredientsChecker():
    def __init__(self, ingredients):
        self.lfm = {}
        self.ingredients = ingredients
        self.token_pairs = {}
        self.results = []
        self.not_found = []

    def prepare_ingredients(self):
        if isinstance(self.ingredients, str):
            self.ingredients = re.sub(r'{(.*)}', '', self.ingredients, flags=re.DOTALL)
            self.ingredients = re.sub(r'\(.*?\)', '', self.ingredients, flags=re.DOTALL)
            self.ingredients = ''.join([unicodedata.normalize("NFKC", word) for word in self.ingredients])
        if isinstance(self.ingredients, list):
            self.ingredients = re.sub(r'{(.*)}', '', '\n'.join(self.ingredients)+'\n', flags=re.DOTALL)
            self.ingredients = re.sub(r'\(.*?\)', '', self.ingredients, flags=re.DOTALL)
            self.ingredients = ''.join([unicodedata.normalize("NFKC", word) for word in self.ingredients])

    def get_lowfodmap(self, language):
        # get list of low and high fodmap foods
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(BASE_DIR, 'static', f'json/lowfodmap_foods_{language}.json')
        with open(file_path, 'r') as file:
            lowfodmap_dict = json.load(file)
        return lowfodmap_dict

    def split_commas(self):
        self.ingredients = re.sub(r',', '\n', self.ingredients, flags=re.DOTALL)

    def stemm(self, text, language):
        # cut the endings to get to the base form of a word
        tokens = [re.sub("[,\[\]().|/:\'\"]?", '', t).lower() for t in text.split()]
        tokens = [t for t in tokens]
        if language == 'PL':
            endings = ['ków', 'nych', 'ego', 'iej', 'iem', 'ków', 'nej', 'owa', 'owe', 'owy', 'sia', 'wej', 'ych',
                       'ca', 'cy', 'ej', 'ek', 'ia', 'ie', 'ii', 'ka', 'kę', 'ki', 'ko', 'ku', 'na', 'ne', 'no', 'ny',
                       'ów', 'wa',
                       'a', 'e', 'i', 'o', 'u', 'y', 'ę', 'ń', 'ś']
        else:
            endings = ['ies', 'es', 's', 'y']
        for idx, token in enumerate(tokens):
            # to make sure only one change is applied, starting with the longest endings
            changed = False
            for ending in endings:
                if changed is False:
                    if token.endswith(ending) and token != ending:
                        if token[:-len(ending)] not in self.token_pairs:
                            self.token_pairs[token[:-len(ending)]] = [tokens[idx]]
                        else:
                            # in case there are repeated/similar ingredients, store pair for each case
                            self.token_pairs[token[:-len(ending)]].append(tokens[idx])
                        tokens[idx] = token[:-len(ending)]
                        changed = True
        return tokens

    def get_ngrams(self, stems_list, n):
        ngrams = []
        start, end = 0, n
        while end <= len(stems_list):
            ngrams.append(' '.join(stems_list[start:end]))
            start += 1
            end += 1
        return ngrams

    def translate(self, stem):
        # translate stems back to original form
        key_list = stem.split()
        for idx, word in enumerate(key_list):
            if word in self.token_pairs:
                key_list[idx] = self.token_pairs[word][0]
                if len(self.token_pairs[word]) > 1:
                    self.token_pairs[word].remove(self.token_pairs[word][0])
                else:
                    self.token_pairs.pop(word)
        new_key = ' '.join(key_list).strip()
        return new_key

    def analyze(self, stems_list, lfm):
        # analyze what ingredients are low fodmap
        analyzed_stems = dict()
        for ngrams in stems_list:
            for stem in ngrams:
                if stem in lfm:
                    new_key = self.translate(stem)
                    analyzed_stems[new_key] = lfm[stem]
                    analyzed_stems[new_key]['substitute'] = self.get_substitute(stem)
        return analyzed_stems

    def get_substitute(self, stem):
        if stem in self.lfm:
            if self.lfm[stem]['safety'] == 'blue':
                return self.lfm[stem]['comment']


    def get_results(self, analyzed_ngrams, ingredients):
        # gets results for original ingredients
        results = []
        real_ingredients = [ingr.lower() for ingr in ingredients.split('\n')]
        for ingr in real_ingredients:
            ingr_found = False
            for key in analyzed_ngrams:
                if ingr_found is False:
                    if key in ingr:
                        ingr_found = True
                        results.append((ingr.strip(), analyzed_ngrams[key]['amount'],
                                        analyzed_ngrams[key]['comment'], analyzed_ngrams[key]['safety'],
                                        analyzed_ngrams[key]['substitute']))
        not_found = [ingr.strip() for ingr in real_ingredients
                     if ingr.strip() not in [ingr[0] for ingr in results] and len(ingr)>1]
        for ingr in not_found:
            results.append((ingr, '', 'not found', 'grey', ''))
        return list(dict.fromkeys(results)), list(dict.fromkeys(not_found))

    def ingr_check(self, ingr):
        ommit_words = ['szt.', 'szt', 'szkl', 'szkl.', 'szklanka', 'szklanki',
                       'łyżka', 'łyżki', 'łyżeczka', 'łyżeczki', 'łyżeczek', 'łyż.', 'łyż',
                       'dużej łyż.', 'małej łyż.', 'duża łyż.', 'mała łyż.',
                       'kg', 'g', 'gram', 'mililitrów', 'ml', 'cm', 'gramów', 'kostka', 'opak', 'opak.', 'opakowanie',
                       'składniki', 'kalkulator jednostek', 'wybierz składnik', 'starty', 'świeży',
                       'glass', 'tablespoon', 'teaspoon', 'tbsp', 'tbsp.', 'tsp', 'tsp.',
                       ]
        return True if ingr not in ommit_words and len(ingr) > 2 and \
                       len(ingr.split()) < 8 and re.search('[a-zA-Z]', ingr) else False

    def check_ingredients(self, language):
        self.prepare_ingredients()
        self.lfm = self.get_lowfodmap(language)
        self.split_commas()
        stems = self.stemm(self.ingredients, language)
        ngrams = []
        ngrams.append(self.get_ngrams(stems, 3))
        ngrams.append(self.get_ngrams(stems, 2))
        ngrams.append(stems)
        analyzed_ngrams = self.analyze(ngrams, self.lfm)
        results, not_found = self.get_results(analyzed_ngrams, self.ingredients)
        ingredients_table = list(dict.fromkeys([i.strip().lower() for i in self.ingredients.splitlines() ]))
        return results, not_found, ingredients_table, stems

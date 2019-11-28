import re
import ast

# class Stemmer:
#     def __init__(self, ingredients, token_pairs):
#         self.ingredients = ingredients
#         self.token_pairs = token_pairs
#
#     def stemm_smol(self, ingredients, token_pairs):
#         tokens = [re.sub('[0-9(),.-:/*]', '', t).lower() for t in self.ingredients.split()]
#         tokens = [t for t in tokens if len(t) > 2]
#         three_letters_ending = ('iem', 'owe')
#         two_letters_ending = ('ka', 'ki', 'na', 'ny', 'ca', 'cy', 'ów', 'ek')
#         one_letter_ending = ('a', 'i', 'u', 'ś')
#         for idx, token in enumerate(tokens):
#             if token.endswith(three_letters_ending):
#                 self.token_pairs[token[:-3]] = tokens[idx]
#                 tokens[idx] = token[:-3]
#             elif token.endswith(two_letters_ending):
#                 self.token_pairs[token[:-2]] = tokens[idx]
#                 tokens[idx] = token[:-2]
#             elif token.endswith(one_letter_ending):
#                 self.token_pairs[token[:-1]] = tokens[idx]
#                 tokens[idx] = token[:-1]
#         return tokens

token_pairs = {}
def stemm(text):
    # cut the endings to get to the base form of a word
    try:
        text = ast.literal_eval(text)
    except SyntaxError:  # it's a string (space separated)
        text = text.split(' ')
    except ValueError:  # it's a string (one word)
        pass
    try:
        tokens = [re.sub("[,\[\]().|/:\-\'\"[0-9]]?", '', t).lower() for t in text.split()]
    except AttributeError:
        tokens = [re.sub("[,\[\]().|/:\-\'\"[0-9]]?'", '', t).lower() for t in text]
    tokens = [t.strip() for t in tokens]
    endings = ['ków', 'nych', 'ego', 'iej', 'iem', 'ków', 'nej', 'owa', 'owe', 'owy', 'sia', 'wej', 'ych', 'ca', 'cy', 'ej', 'ek', 'ia', 'ie', 'ii',
               'ka', 'kę', 'ki', 'ko', 'ku', 'na', 'ne', 'no', 'ny', 'ów', 'wa', 'a', 'e', 'i', 'o', 'u', 'y', 'ę', 'ń', 'ś']
    for idx, token in enumerate(tokens):
        # to make sure only one change is applied, starting with the longest endings
        changed = False
        for ending in endings:
            if changed is False:
                if token.endswith(ending) and token != ending:
                    tokens[idx] = token[:-len(ending)]
                    changed = True
    return tokens
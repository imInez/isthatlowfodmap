import re
import ast


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
        tokens = [re.sub("[,\[\]().|/:\-\'\"]?", '', t).lower() for t in text.split()]
    except AttributeError:
        tokens = [re.sub("[,\[\]().|/:\-\'\"]?", '', t).lower() for t in text]
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
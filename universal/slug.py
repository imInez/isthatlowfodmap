def slug(text, make_slug):
    if make_slug is True:
        return text.replace(' ', '---')
    else:
        return text.replace('---', ' ')
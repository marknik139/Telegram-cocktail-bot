from random import choice
from text_data import cocktail_dict, menu_messages


def get_random_key():
    result = choice(list(cocktail_dict.cocktail_name.keys()))

    return result


def get_menu_from_keys():
    menu = ''
    for key in cocktail_dict.cocktail_name:
        menu += cocktail_dict.cocktail_name[key] + ' ' + key + '\n'

    return menu
"""Module used to syntax highlight code files"""
import json
from typing import Dict, List, Tuple
import numpy as np
import constants as c
from itertools import product

# %%% Constants
default_array = np.ones(shape=(c.HEIGHT, c.WIDTH, c.CHANNELS), dtype=np.uint8)
default_array *= 255


# %%% Global Variables
with open(c.DICTIONARY, 'r', encoding='utf8') as color_dict:
    scope_dictionary: Dict[str, int] = json.load(color_dict)

variable_dictionary: Dict[str, int] = {}

# %%% Utils


def _get_empty_array() -> np.ndrray:
    return np.copy(default_array)


def _get_scope_code(scope: str) -> int:
    return scope_dictionary.get(scope, 255)


def _string_to_list(string: str) -> List[str]:
    return json.loads(string)


def _get_highlight(scopes: str) -> Tuple[int, int, int]:
    scope_list = _string_to_list(scopes)
    padded_scopes = [*c.PADDING, *scope_list]
    codes = tuple(map(_get_scope_code, padded_scopes[-3:]))
    return codes


def _calculate_ident(dataframe: np.ndarray) -> int:
    start = dataframe[dataframe['start'] == 0]
    first_lines = start[start['token'].apply(str.isspace)]
    return np.gcd.reduce(first_lines['end'])


def _get_color_code(dataframe):
    return dataframe['scopes'].apply(_get_highlight)


def _get_positions(dataframe):
    return dataframe.groupby('line').cumcount()


def _get_pixel_size(dataframe, ident):
    return dataframe[['start', 'token']].apply(lambda row: len(
        row['token'])//ident if row['start'] == 0 and row['token'].isspace() else 1, axis=1)
# %%% public functions


def syntax_highlight(dataframe: np.ndarray) -> np.ndarray:
    """ Devolve syntax highlight
    """
    array = _get_empty_array()
    ident = _calculate_ident(dataframe)
    dataframe['color_code'] = _get_color_code(dataframe)
    dataframe['position'] = _get_positions(dataframe)
    dataframe['pixel_size'] = _get_pixel_size(dataframe, ident)

    for i, j in product(range(c.HEIGHT), range(c.WIDTH)):
        array[i,j] = 

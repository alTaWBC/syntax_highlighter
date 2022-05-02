"""Module used to syntax highlight code files"""
import json
from typing import Dict, List, Tuple
from functools import partial
import numpy as np
import constants as c
import pandas as pd

# %%% Constants
default_array = np.ones(shape=(c.HEIGHT, c.WIDTH, c.CHANNELS), dtype=np.uint8)
default_array *= 255


# %%% Global Variables
with open(c.DICTIONARY, 'r', encoding='utf8') as color_dict:
    scope_dictionary: Dict[str, int] = json.load(color_dict)

variable_dictionary: Dict[str, int] = {}

# %%% Utils


def _get_empty_array() -> np.ndarray:
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
    return np.max([np.gcd.reduce(first_lines['end']), 1])


def _get_color_code(dataframe):
    return dataframe['scopes'].apply(_get_highlight)


def _identation(dataframe):
    empty_dataframe = np.logical_and(
        dataframe['start'] == 0, dataframe['token'].str.isspace())
    dataframe.loc[empty_dataframe, 'color_code'] = pd.Series(
        [(255, 255, 255)]*len(empty_dataframe))
    return dataframe['color_code']


def _get_positions(dataframe):
    return dataframe.groupby('line')['pixel_size'].cumsum() - dataframe['pixel_size']


def _remove_empty_lines(dataframe):
    return dataframe[dataframe["token"].str.len() > 0]


def _remove_spaces(dataframe):
    return dataframe[(dataframe["start"] == 0) | (~dataframe["token"].str.isspace())]


def _get_pixel_size(dataframe, ident):
    return dataframe[['start', 'token']].apply(lambda row: len(
        row['token'])//ident if row['start'] == 0 and row['token'].isspace() else 1, axis=1)


def _fill_array(row, array):
    array[row['line'], row['position']:row['position'] +
          row['pixel_size'], :] = row['color_code']
# %%% public functions


def syntax_highlight(dataframe):
    """ Returns syntax highlight
    """
    dataframe = _remove_empty_lines(dataframe)
    dataframe = _remove_spaces(dataframe)
    array = _get_empty_array()
    ident = _calculate_ident(dataframe)
    print(ident)
    dataframe['color_code'] = _get_color_code(dataframe)
    dataframe['pixel_size'] = _get_pixel_size(dataframe, ident)
    dataframe['position'] = _get_positions(dataframe)
    dataframe['color_code'] = _identation(dataframe)
    _fill_empty_array = partial(_fill_array, array=array)
    dataframe[np.logical_and(dataframe['line'] < c.HEIGHT, dataframe['position'] < c.WIDTH)].apply(
        _fill_empty_array, axis=1)
    return dataframe, array

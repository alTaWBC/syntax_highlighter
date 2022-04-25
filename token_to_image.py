"""This module is used to syntax highlight code"""
import json
from typing import Dict
from PIL import ImageFont, ImageDraw, Image, ImageColor
import numpy as np
import constants as c

# %%% Utils


def hexToRgb(color: str) -> tuple:
    return ImageColor.getcolor(color, "RGB")


def scopesToColor(scopes: list) -> tuple:

    keys = rgb_colors.keys()

    # the scopes go from least important to most important

    for scope in scopes[::-1]:
        for key in keys:
            if key in scope:
                return rgb_colors[key]
    return c.DEFAULT


def getDefaultImage():
    copy_array = np.copy(default_array)
    image = Image.fromarray(copy_array)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(c.FONT, 15)
    return draw, font, image


def getBaseImage():
    return np.zeros((10, 20, 3), dtype=np.uint8)


def _getColorCode(scope):
    return color_dictionary.get(scope, 255)


def getHighlight(scopes):
    # Pad the array to have at least 3 values
    pad_scopes = [*c.PADDING, *scopes]

    # Get last 3 scopes
    r_token, g_token, b_token = pad_scopes[-3:]

    return (_getColorCode(r_token), _getColorCode(g_token), _getColorCode(b_token))


def getYValue(scopes, token):
    if not any(['variable' in scope for scope in scopes]):
        return -1

    return variable_dictionary.setdefault(token, len(variable_dictionary))


# %%% global variables
with open(c.DICTIONARY, 'r') as color_dict:
    color_dictionary = json.load(color_dict)

variable_dictionary: Dict[str, int] = {}

# %%% Get color coding
with open(c.COLOR_CODING, 'r') as color_file:
    colors = json.loads(color_file.read())

rgb_colors = {k: hexToRgb(v) for k, v in colors.items()}

# %%% Default Image
default_array = np.ones(shape=(c.HEIGHT, c.WIDTH, 3), dtype=np.uint8)
default_array[:, :, 0], default_array[:, :, 1], default_array[:, :, 2] = c.RGB


# %%% public Functions
def reducedSyntaxHighlightText(dataframe):
    image = getBaseImage()
    i = cline = 0
    for _, row in dataframe.iterrows():
        line, start, _, _, scopes = row
        if line >= 10:
            break
        if line != cline:
            i = 0
            cline = line
        if i == 0 and start > 0:
            i = start // 4
            print(i, start)
        token_color = getHighlight(json.loads(scopes))
        image[line, i, :] = token_color
        i += 1
    return image


def syntaxHighlightText(dataframe):
    draw, font, image = getDefaultImage()
    for _, row in dataframe.iterrows():
        line, start, __, token, scopes = row
        if line >= 10:
            break
        token_color = scopesToColor(json.loads(scopes))
        draw.text((5+10*int(start), 5+20*int(line)),
                  str(token), font=font, fill=token_color)
    return image


def syntax_highlight_reduced(dataframe):
    image = getBaseImage()
    i = current_line = 0

    for row in dataframe['line' < 10].itterows():
        line, start, _, _, scopes = row

        if line != current_line:
            i = start // 4
            current_line = line

        token_color = getHighlight(json.loads(scopes))
        image[line, i, :] = token_color
        i += 1
    return image

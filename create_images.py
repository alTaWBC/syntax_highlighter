# %%% Imports
import json
from os import listdir
from os.path import join
import subprocess
import constants as c
import pandas as pd
import numpy as np
import token_to_image as ti
import matplotlib.pyplot as plt
import cv2 as cv


# %%% Get Matlab filenames
mfilenames = [f for f in listdir(c.MATLAB_FILES)]

# %%% Create Token Files using a javascript script
for filename in mfilenames:
    input_location = join(c.MATLAB_FILES, filename)
    output_location = join(c.TOKEN_FILES, filename[:-1] + "csv")
    process = subprocess.Popen([c.NODE, c.TEXTMATE_SCRIPT, input_location,
                                output_location], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


# %% Get token filenames
tfilenames = [f for f in listdir(c.TOKEN_FILES)]

for filename in tfilenames:
    input_location = join(c.TOKEN_FILES, filename)
    output_location = join(c.IMAGE_FILES, filename)
    reduced_output_location = join(c.REDUCED_IMAGE_FILES, filename)
    sorted_toke_location = join(c.SORTED_TOKEN_FILES, filename)

    dataframe = pd.read_csv(input_location, sep=str("_,_")).fillna("")
    dataframe = dataframe.sort_values(by=["line", "start"])
    dataframe.to_csv(sorted_toke_location, index=False)
    image = ti.syntaxHighlightText(dataframe)
    reduced_image = ti.reducedSyntaxHighlightText(dataframe)
    image.save(output_location[:-3] + 'png',)
    cv.imwrite(reduced_output_location[:-3] + 'png', reduced_image)

from os import getcwd
from os.path import join

BASE_DIR = getcwd()
MATLAB_FILES = join(BASE_DIR, "matlab_files")
TOKEN_FILES = join(BASE_DIR, "token_files")
SORTED_TOKEN_FILES = join(BASE_DIR, "sorted_token_files")
IMAGE_FILES = join(BASE_DIR, "image_files")
REDUCED_IMAGE_FILES = join(BASE_DIR, "reduced_image_files")
ASSET_FILES = join(BASE_DIR, "assets")

TEXTMATE_SCRIPT = join(BASE_DIR, "index.js")
COLOR_CODING = join(ASSET_FILES, "colors.json")
FONT = join(ASSET_FILES, "RobotoMono-VariableFont_wght.ttf")
DICTIONARY = join(ASSET_FILES, "dictionary.json")
MATLAB_TMLANGUAGE = join(ASSET_FILES, "m.tmLanguage")
SCOPE_DICTIONARY = join(ASSET_FILES, "scope_dictionary.json")
DATABASE = r"C:\Users\WilliamCosta\Documents\bolsas\server\mainDB.db"

# If node is installed in the system variables no path will be needed
# Otherwise you need to change this variable to the node path
NODE = 'node'
WIDTH = 20
HEIGHT = 10
CHANNELS = 3
RGB = (45, 4, 85)
DEFAULT = (0, 255, 0)
PADDING = ['source.matlab', 'source.matlab', 'source.matlab']

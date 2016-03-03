__author__ = 'Bat Cave'

import glob
import os
import zipfile

zip_files = glob.glob('*.zip')

for zip_filename in zip_files:
    dir_name = os.path.splitext(zip_filename)[0]
    os.mkdir(dir_name)
    zip_handler = zipfile.ZipFile(zip_filename, "r")
    zip_handler.extractall(dir_name)
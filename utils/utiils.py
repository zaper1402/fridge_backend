import os
from typing import JSON
import re

def parse_array(array : str):
    array.replace('[', '')
    array.replace(']', '')
    #return JSONArray
    return array.split(',')


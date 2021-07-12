import pandas as pd
from IPython.core.display import HTML
import json

def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'

f = open('resjson.json', 'r')

valarray = json.load(f)

f.close()

print(valarray)

df = pd.DataFrame(valarray)

df.to_html('res.HTML', escape=False, formatters=dict(iconpath=path_to_image_html))

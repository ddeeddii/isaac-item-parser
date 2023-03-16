import xml.etree.ElementTree as et
from tqdm import tqdm
import json

# inputs  
item_in = 'items.xml'
translations_in = 'stringtable.sta'

# outputs
item_out = 'items.json'
trinket_out = 'trinkets.json'

# parsing xml
string_tree = et.parse(translations_in)
string_root = string_tree.getroot()

i_tree = et.parse(item_in)
i_root = i_tree.getroot()

def create_xpath_for_item(name: str):
  return f"category[@name='Items']/key[@name='{name}']/string[1]"

# extraction code
def extract_data(type: str):
  allowed_tags = []
  output_file = ''

  item_data = {}

  if type == 'item':
    allowed_tags = ['active', 'passive', 'familar']
    output_file = item_out
  elif type == 'trinket':
    allowed_tags = ['trinket']
    output_file = trinket_out

  print(f'Extracting {type} data...')
  for child in tqdm(i_root):
    if child.tag not in allowed_tags: continue 
    item = string_tree.findtext(create_xpath_for_item(child.attrib['name'][1:]))

    item_data[child.attrib['id']] = {
      'name': item,
      'gfx': child.attrib['gfx']
    }

  with open(output_file, 'w') as out:
    json.dump(item_data, out)

  print(f'Saved {type} data into', output_file)

extract_data('item')
extract_data('trinket')
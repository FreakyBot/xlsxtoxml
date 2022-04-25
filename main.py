import ftplib
import os
import sys
from functools import wraps
from pathlib import Path

import et as et
import lxml
import pandas
import pandas as pd
import requests as requests
from lxml import etree as et
from lxml.etree import CDATA
import xlrd
from ftplib import FTP

url = 'https://drive.google.com/uc?export=download&id=1ZyE-VPoYQZgIlbQIoVkFD4VVXC-NpUbO'
r = requests.get(url)
open('temp.xlsx', 'wb').write(r.content)

try:
    raw_data = pd.read_excel('temp.xlsx')
except KeyError as e:
    sys.exit(1)
except TypeError as e:
    sys.exit(1)
except FileNotFoundError as e:
    sys.exit(1)

root = et.Element('document')

for row in raw_data.iterrows():
    root_tags = et.SubElement(root, 'root')  # === > Root name
    # These are the tag names for each row (SECTION 1)
    Column_heading_1 = et.SubElement(root_tags, 'sku')
    Column_heading_2 = et.SubElement(root_tags, 'product_url')
    Column_heading_3 = et.SubElement(root_tags, 'name_ar')
    Column_heading_4 = et.SubElement(root_tags, 'image_url')
    Column_heading_5 = et.SubElement(root_tags, 'price')
    Column_heading_6 = et.SubElement(root_tags, 'color')
    Column_heading_7 = et.SubElement(root_tags, 'size')
    Column_heading_8 = et.SubElement(root_tags, 'age')
    Column_heading_9 = et.SubElement(root_tags, 'design')
    Column_heading_10 = et.SubElement(root_tags, 'numberofpaces')
    Column_heading_11 = et.SubElement(root_tags, 'package')
    Column_heading_12 = et.SubElement(root_tags, 'description_ar')
    Column_heading_13 = et.SubElement(root_tags, 'categories')

    # The values inside the [] are the raw file column headings.(SECTION 2)
    Column_heading_1.text = CDATA(str(row[1]['sku']).replace(r'nan', ''))
    Column_heading_2.text = CDATA(str(row[1]['product_url']).replace(r'nan', ''))
    Column_heading_3.text = CDATA(str(row[1]['name_ar']).replace(r'nan', ''))
    Column_heading_4.text = CDATA(str(row[1]['image_url']).replace(r'nan', ''))
    Column_heading_5.text = CDATA(str(row[1]['price']).replace(r'nan', ''))
    Column_heading_6.text = CDATA(str(row[1]['color']).replace(r'nan', ''))
    Column_heading_7.text = CDATA(str(row[1]['size']).replace(r'nan', ''))
    Column_heading_8.text = CDATA(str(row[1]['age']).replace(r'nan', ''))
    Column_heading_9.text = CDATA(str(row[1]['design']).replace(r'nan', ''))
    Column_heading_10.text = CDATA(str(row[1]['number of paces']).replace(r'nan', ''))
    Column_heading_11.text = CDATA(str(row[1]['Package']).replace(r'nan', ''))
    Column_heading_12.text = CDATA(str(row[1]['description_ar']).replace(r'nan', ''))
    Column_heading_13.text = CDATA(str(row[1]['categories']).replace(r'nan', ''))

tree = et.ElementTree(root)
et.indent(tree, space="\t", level=0)
tree.write('output.xml', encoding="utf-8")
file_path = Path('output.xml')

with FTP('s0.small.pl', 'f1512_test', '#Sales123') as ftp, open(file_path, 'rb') as file:
    ftp.storbinary(f'STOR {file_path.name}', file)

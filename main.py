import sys
import tempfile
import et as et
import pandas as pd
import requests as requests
from lxml import etree as et
from lxml.etree import CDATA
from ftplib import FTP


def main():
    url = "https://drive.google.com/uc?export=download&id=1ZyE-VPoYQZgIlbQIoVkFD4VVXC-NpUbO"
    r = requests.get(url)
    open("temp.xlsx", "wb").write(r.content)

    try:
        raw_data = pd.read_excel("temp.xlsx")
    except KeyError as e:
        # dodac logi
        sys.exit(1)
    except TypeError as e:
        sys.exit(1)
    except FileNotFoundError as e:
        sys.exit(1)

    root = et.Element('document')

    for row in raw_data.iterrows():
        root_tags = et.SubElement(root, 'root')  # === > Root name
        # These are the tag names for each row (SECTION 1)
        column_heading_1 = et.SubElement(root_tags, 'sku')
        column_heading_2 = et.SubElement(root_tags, 'product_url')
        column_heading_3 = et.SubElement(root_tags, 'name_ar')
        column_heading_4 = et.SubElement(root_tags, 'image_url')
        column_heading_5 = et.SubElement(root_tags, 'price')
        column_heading_6 = et.SubElement(root_tags, 'color')
        column_heading_7 = et.SubElement(root_tags, 'size')
        column_heading_8 = et.SubElement(root_tags, 'age')
        column_heading_9 = et.SubElement(root_tags, 'design')
        column_heading_10 = et.SubElement(root_tags, 'numberofpaces')
        column_heading_11 = et.SubElement(root_tags, 'package')
        column_heading_12 = et.SubElement(root_tags, 'description_ar')
        column_heading_13 = et.SubElement(root_tags, 'categories')

        # The values inside the [] are the raw file column headings.(SECTION 2)
        column_heading_1.text = CDATA(str(row[1]['sku']).replace(r'nan', ''))
        column_heading_2.text = CDATA(str(row[1]['product_url']).replace(r'nan', ''))
        column_heading_3.text = CDATA(str(row[1]['name_ar']).replace(r'nan', ''))
        column_heading_4.text = CDATA(str(row[1]['image_url']).replace(r'nan', ''))
        column_heading_5.text = CDATA(str(row[1]['price']).replace(r'nan', ''))
        column_heading_6.text = CDATA(str(row[1]['color']).replace(r'nan', ''))
        column_heading_7.text = CDATA(str(row[1]['size']).replace(r'nan', ''))
        column_heading_8.text = CDATA(str(row[1]['age']).replace(r'nan', ''))
        column_heading_9.text = CDATA(str(row[1]['design']).replace(r'nan', ''))
        column_heading_10.text = CDATA(str(row[1]['number of paces']).replace(r'nan', ''))
        column_heading_11.text = CDATA(str(row[1]['Package']).replace(r'nan', ''))
        column_heading_12.text = CDATA(str(row[1]['description_ar']).replace(r'nan', '').replace(r'&nbsp', ''))
        column_heading_13.text = CDATA(str(row[1]['categories']).replace(r'nan', ''))

    tree = et.ElementTree(root)
    et.indent(tree, space="\t", level=0)
    
    # creating tmp file
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.name = "feed.xml"

    # writing to tmp
    tree.write(tmp.name, encoding="utf-8")

    with FTP("s0.small.pl", "f1512_test", "#Sales123") as ftp, open("feed.xml", "rb") as file:
        ftp.storbinary(f"STOR {file.name}", file)


main()

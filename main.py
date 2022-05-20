import sys
import tempfile
from datetime import datetime
from ftplib import FTP

import et as et
import pandas as pd
import requests as requests
from lxml import etree as et
from lxml.etree import CDATA
from pandas.errors import EmptyDataError


def main():
    url = "link"
    try:
        print(datetime.now(), 'Start downloading file')
        r = requests.get(url)
        print(datetime.now(), 'Downloading file complete')
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    try:
        print(datetime.now(), 'Open xlsx file')
        open("temp.xlsx", "wb").write(r.content)
    except Exception as e:
        print(e)
        sys.exit(1)

    try:
        print(datetime.now(), 'Pandas read')
        raw_data = pd.read_excel("temp.xlsx")
    except KeyError as e:
        print(e)
        sys.exit(1)
    except TypeError as e:
        print(e)
        sys.exit(1)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except EmptyDataError as e:
        print(e)
        sys.exit(1)
    try:
        raw_data['First Link'] = raw_data['image_url'].str.split(',', expand=True)[0]
        raw_data['Second Link'] = raw_data['image_url'].str.split(',', expand=True)[1]
        raw_data['Third Link'] = raw_data['image_url'].str.split(',', expand=True)[2]
        print(datetime.now(), 'Splitting img_url')
    except Exception as e:
        print(e)

    root = et.Element('document')

    try:
        for row in raw_data.iterrows():
            root_tags = et.SubElement(root, 'root')  # === > Root name
            # These are the tag names for each row (SECTION 1)
            column_heading_1 = et.SubElement(root_tags, 'sku')
            column_heading_2 = et.SubElement(root_tags, 'product_url')
            column_heading_3 = et.SubElement(root_tags, 'name_ar')
            column_heading_4 = et.SubElement(root_tags, 'image_url')
            column_heading_14 = et.SubElement(root_tags, 'image_url2')
            column_heading_15 = et.SubElement(root_tags, 'image_url3')
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
            column_heading_4.text = CDATA(str(row[1]['First Link']).replace(r'nan', ''))
            column_heading_14.text = CDATA(str(row[1]['Second Link']).replace(r'nan', ''))
            column_heading_15.text = CDATA(str(row[1]['Third Link']).replace(r'nan', ''))
            column_heading_5.text = CDATA(str(row[1]['price']).replace(r'nan', ''))
            column_heading_6.text = CDATA(str(row[1]['color']).replace(r'nan', ''))
            column_heading_7.text = CDATA(str(row[1]['size']).replace(r'nan', ''))
            column_heading_8.text = CDATA(str(row[1]['age']).replace(r'nan', ''))
            column_heading_9.text = CDATA(str(row[1]['design']).replace(r'nan', ''))
            column_heading_10.text = CDATA(str(row[1]['number of paces']).replace(r'nan', ''))
            column_heading_11.text = CDATA(str(row[1]['Package']).replace(r'nan', ''))
            column_heading_12.text = CDATA(str(row[1]['description_ar']).replace(r'nan', '').replace(r'&nbsp', ' '))
            column_heading_13.text = CDATA(str(row[1]['categories']).replace(r'🔥', '').replace(r'nan', ''))
        print(datetime.now(), 'Finished creating xml fields')
    except IOError as e:
        print("I/O error: {0}".format(e))
    except ValueError:
        print("Could not convert data to an integer.")
    except Exception as e:
        print("Unexpected error: {0}".format(e))

    tree = et.ElementTree(root)
    et.indent(tree, space="\t", level=0)

    # creating tmp file
    try:
        print(datetime.now(), 'Creating tmp file')
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.name = "feed.xml"
    except Exception as e:
        print('Cannot create tmp file', str(e))

    print(datetime.now(), 'Writing to tmp file')
    # writing to tmp
    tree.write(tmp.name, encoding="utf-8")

    print(datetime.now(), 'Uploading tmp file to ftp')
    try:
        with FTP("host", "user", "pass") as ftp, open(tmp.name, "rb") as file:
            ftp.storbinary(f"STOR {file.name}", file)
            print(datetime.now(), "Uploading done")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()

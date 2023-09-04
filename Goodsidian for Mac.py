#!/usr/bin/env python3

import urllib.request
import os
import subprocess
import xml.etree.ElementTree as ET

# URL for "Currently reading":
url = "https://www.goodreads.com/review/list_rss/56197581?key=nWY09T6mRBlqowTLnFbs3DP0WqroPuPiNsO_cjgCw9sa1wQ2&shelf=tech"

# Enter the path to your Vault
vaultpath = "/Users/SFL/Library/Mobile Documents/iCloud~md~obsidian/Documents/Notes/BOOKS"

# Fetch the data from rss feed and decode
response = urllib.request.urlopen(url)
feed = response.read().decode("utf-8")
info = ET.fromstring(feed)

# Define a list of element names you want to extract
#element_names = ['id', 'title', 'image', 'author', 'year', 'pages', 'rating', 'des']

bookamount = 0
id = ""
title = ""
shorttitle = ""
image = ""
author = ""
year = ""
pages = ""
rating = ""
shelf = ""
des = ""

# Extract and display content for each element
for root in info.findall(".//item"):  # This will find all <item> elements at any level

    id_element = root.find(".//book_id")
    if id_element is not None:
        id = id_element.text.strip()

    title_element = root.find(".//title")
    if title_element is not None:
        title = title_element.text.strip()
        shorttitle = title

        # Find title up to the first colon as note name
        colon_index = title.find(":")
        if colon_index != -1:
            shorttitle = title[:colon_index].strip()

    if os.path.exists(f"{vaultpath}/{shorttitle}.md"):
        continue
    bookamount = bookamount + 1

    image_element = root.find(".//book_large_image_url")
    if image_element is not None:
        image = image_element.text.strip()

    author_element = root.find(".//author_name")
    if author_element is not None:
        author = author_element.text.strip()

    year_element = root.find(".//book_published")
    if year_element is not None:
        if year_element.text is not None:
            year = year_element.text.strip()

    pages_element = root.find(".//num_pages")
    if pages_element is not None:
        pages = pages_element.text.strip()

    rating_element = root.find(".//average_rating")
    if rating_element is not None:
        rating = rating_element.text.strip()

    shelf_element = root.find(".//user_shelves")
    if shelf_element is not None:
        shelf = shelf_element.text.strip()
    list = [tag.strip() for tag in shelf.split(',')]
    front = []
    back = []
    for tag in list:
        if tag in ["to-read", "read", "currently-reading"]:
            back.append(f"#{tag}")
        else:
            front.append(f"#{tag}")
        combined = front + back
        shelf = ' '.join(combined)

    des_element = root.find(".//book_description")
    if des_element is not None:
        des = des_element.text.strip()

    note_content = f'''![]({image})

**Title:** {title}
**Author:** {author}
**Year:** {year}
**Page Count:** {pages}
**Avg Rating:** {rating}
**Shelf:** {shelf}

**Description:**
{des}'''

    note_path = os.path.join(vaultpath, f'{shorttitle}.md')
    with open(note_path, 'w') as note_file:
        note_file.write(note_content)

if bookamount == 0:
    subprocess.run(["osascript", "-e", 'display notification "No new books found." with title "Currently-reading: No update"'])

else:
    subprocess.run(["osascript", "-e", f'display notification "{bookamount} Booknote(s) created!" with title "{title}"'])

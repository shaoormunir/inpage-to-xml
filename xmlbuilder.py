import xml.etree.ElementTree as xml
from xml.etree.ElementTree import tostring

filename = "test.xml"
root = xml.Element("document")
meta = xml.Element("meta")

# Meta subelements
title = xml.SubElement(meta, "title")
title.text = "Title of the document goes here"
meta.append(title)

author = xml.Element("author")
name = xml.SubElement(author, "name")
name.text = "Name of author goes here"
gender = xml.SubElement(author, "gender")
gender.text = "Gender of the author goes here"
meta.append(author)

publication = xml.Element("publication")
pub_name = xml.SubElement(publication, "name")
pub_name.text = "Name of publication"
pub_year = xml.SubElement(publication, "year")
pub_year.text = "Year it was published"
pub_city = xml.SubElement(publication, "city")
pub_city.text = "City in which it was published"
pub_link = xml.SubElement(publication, "link")
pub_link.text = "Link to online resource"
pub_copyrights = xml.SubElement(publication, "copyright-holder")
meta.append(publication)

num_words = xml.SubElement(meta, "num-words")
num_words.text = "Number of words in the document"

non_urdu_langs = xml.SubElement(meta, "contains-non-languages")
non_urdu_langs.text = "Specify if the document contains languages other than urdu"

body = xml.Element("body")
section = xml.Element("section")
para = xml.SubElement(section, "p")
para.text = "A para will go here."
blockquote = xml.SubElement(section, "blockquote")
blockquote.text = "A blockquote should go here."
body.append(section)
# body subelements
root.append(meta)
root.append(body)

tree = xml.ElementTree(root)

with open(filename, "w") as f:
    f.write(tostring(root, encoding='unicode'))
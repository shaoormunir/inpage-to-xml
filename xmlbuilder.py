import xml.etree.ElementTree as xml
from xml.etree.ElementTree import tostring
import os
import string
from xml.sax.saxutils import unescape

def add_section (section):
    children = section.getchildren()
    if (len(children)) == 1:
        child = children[0]
        if child.tag == "p" and child.text == "":
            return False
        else:
            return True
    else:
        return True

def check_if_eng_alphabet(symbol):
    if (symbol >= 'a' and symbol <= 'z') or (symbol >= 'A' and symbol <= 'Z'):
        return True
    else:
        return False

def generate_xml (filepath):
    output_filepath = filepath.replace(".txt", ".xml")
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
    pub_copyrights.text = "Copyright information for the publication will go here"
    meta.append(publication)

    num_words = xml.SubElement(meta, "num-words")
    num_words.text = "Number of words in the document"

    non_urdu_langs = xml.SubElement(meta, "contains-non-languages")
    non_urdu_langs.text = "Specify if the document contains languages other than urdu"

    body = xml.Element("body")

    # This section will parse the text document and find sections/blocquotes etc
    with open(filepath, "r") as f:
        text_data = f.read()

    blockquote_running = False
    para_running = True
    annotation_running = False
    previous_symbol = ""

    section  = xml.Element("section")
    blockquote = xml.Element("blockquote")
    para = xml.Element("p")
    para.text = ""
    annotation = xml.Element("annotation")
    annotation.text = ""

    for symbol in text_data:
        if previous_symbol == ":" and symbol == "\n":
            if blockquote_running:
                blockquote_running = False
                if len(blockquote.getchildren()) > 0:
                    section.append(blockquote)
                blockquote.append(para)
            else:
                section.append(para)

            para = xml.Element("p")
            para.text = ""
            para_running = True
            blockquote_running = True
            blockquote = xml.Element("blockquote")
        elif symbol == previous_symbol == "\n":
            if len(section.getchildren()) > 0 and add_section(section):
                body.append(section)
            section = xml.Element("section")
        elif symbol == "\n":
            para_running = False

        if check_if_eng_alphabet(symbol):
            if not annotation_running:
                annotation_running = True
                annotation = xml.Element("annotation")
                annotation.set("lang", "en")
                annotation.text = symbol
            else:
                annotation.text+=symbol
        else:
            if annotation_running:
                punctuation = string.punctuation
                punctuation = punctuation.replace(")", "")
                punctuation = punctuation.replace("(", "")
                punctuation = punctuation.replace("]", "")
                punctuation = punctuation.replace("[", "")
                punctuation+=" "
                if symbol in punctuation:
                    annotation.text+=symbol
                else:
                    para.text += unescape(tostring(annotation, encoding='unicode'))
                    annotation_running = False
                    para.text+=symbol

            elif para_running:
                para.text += symbol
            else:
                if blockquote_running:
                    blockquote_running = False
                    blockquote.append(para)
                    section.append(blockquote)
                else:
                    section.append(para)
                para = xml.Element("p")
                para.text = ""
                para_running = True
        previous_symbol = symbol

    body.append(section)
    # body subelements
    root.append(meta)
    root.append(body)

    with open(output_filepath, "w") as f:
        f.write(unescape(tostring(root, encoding='unicode')))


def pre_process(filename):
    with open(filename, encoding='utf-8') as f:
        data = f.read()
    print (data)
    remove_leading_space_regex = "\s[۔،:\(\[“‘]"
    remove_trailing_space_regex = "[\)\]”’]\s"
    add_trailing_space_regex = "[۔،:\(\[“‘][^\s]"
    add_leading_space_regex = "[^\s][\)\]”’]"
    double_space_regex = "/\s\s/"

pre_process("test-utf.txt")
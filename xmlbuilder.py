import xml.etree.ElementTree as xml
from xml.etree.ElementTree import tostring
import os
import string
from xml.sax.saxutils import unescape
import regex as re

remove_leading_space_regex = r"(?r)\s[۔،:\(\[“‘]"
remove_trailing_space_regex = r"(?r)[\)\]”’]\s"
add_trailing_space_regex = r"(?r)[۔،:\(\[“‘][^\s]"
add_leading_space_regex = r"(?r)[^\s][\)\]”’]"
double_space_regex = r"(?r)[ ]{2,}"
floating_character_regex = r"(?r)[^و]"
zer_regex = r"(?r) ِ"
footnote_regex = r"(?r)حوالہ جات|مآخذ"
double_quotes_regex = r"(?r)’’"
inverted_double_quotes_regex = r"(?r)‘‘"
floating_number_regex = r"(?)[٠-٩]|$[٠-٩]{2}$"

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

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

def create_attention_text(original_text, attention_type):
    attention = xml.Element(attention_type)
    attention.text = original_text
    return unescape(tostring(attention, encoding='unicode'))

def check_if_para_needs_attention(para):
    para_text = para.text

    # Floating letter is disabled because it is tagging each and every letter in its current form   
    # para_text = re.sub(floating_character_regex, lambda m: create_attention_text(para_text[m.start():m.end()], "attention-floating-letter") , para_text)

    para_text = re.sub(zer_regex, lambda m: create_attention_text(para_text[m.start():m.end()], "attention-zer"), para_text)

    para_text = re.sub(floating_number_regex, lambda m: create_attention_text(para_text[m.start():m.end()], "attention-number"), para_text)

    para.text = para_text
    return para

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
            para = check_if_para_needs_attention(para)
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
                para = check_if_para_needs_attention(para)
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
    root.append(meta)
    root.append(body)

    with open(output_filepath, "w") as f:
        f.write(unescape(tostring(root, encoding='unicode')))

# [٠١٢٣٥٦٧٨٩]
def pre_process(filename):
    with open(filename, encoding='utf-8') as f:
        data = f.read()
        
    # remove footnote from the text
    p = re.compile(footnote_regex)

    while p.search(data) != None:
        match = p.search(data)
        data = data[:match.start()]

    # removing leading spaces
    p = re.compile(remove_leading_space_regex)
    for m in p.finditer(data):
        data = replace_str_index(data, m.start(), '')
    
    # removing trailing spaces
    p = re.compile(remove_trailing_space_regex)
    for m in p.finditer(data):
        data = replace_str_index(data, m.end(), '')
    
    # adding a leading space
    p = re.compile(add_leading_space_regex)
    for m in p.finditer(data):
        first_character = data[m.start()+1]
        data = replace_str_index(data, m.start()+1, first_character + " ")
    
    # adding a trailing space
    p = re.compile(add_trailing_space_regex)
    for m in p.finditer(data):
        last_character = data[m.end()-2]
        data = replace_str_index(data, m.end()-2," " +  last_character )

    # Removing double spaces
    p = re.compile(double_space_regex)

    while p.search(data) != None:
        for m in p.finditer(data):
            data = replace_str_index(data, m.start(), "")

    # Remvoing double quotes
    data = re.sub(double_quotes_regex, '”', data)
    data = re.sub(inverted_double_quotes_regex, '“', data)

   
    with open("processed.txt", "w", encoding='utf-8') as f:
        f.write(data)


pre_process("test2.txt")
generate_xml("processed.txt")
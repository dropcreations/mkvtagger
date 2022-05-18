import os
import sys
import subprocess
from xml.etree.ElementTree import Element, tostring

file_path = sys.argv[1]
file_name = os.path.basename(os.path.abspath(file_path))
file_name = os.path.splitext(file_name)
file_name = file_name[0]
xml_name = file_name + "_tags.xml"
tags_dict = {}

print("Matroska/WebM Tags")
print("|")
title_name = input("|--Title: ")
print("|")
print("|--Add Tags from a Text file")
tags_text_add = input("|--Type 'Yes' or 'No': ")
if tags_text_add.lower() == "yes":
    print("|")
    print("|--Text file's content format must be as below.")
    print("|-----------------------------------------")
    print("|-- Tag_Name_1: Tag_Value_1, Tag_Value_2")
    print("|-- Tag_Name_2: Tag_Value_1, Tag_Value_2")
    print("|-----------------------------------------")
    tags_text = input("|--Enter Text file's Path: ")
    print("|")
    txt_folder = os.path.dirname(os.path.abspath(tags_text))
    txt_file = os.path.basename(os.path.abspath(tags_text))
    os.chdir(txt_folder)
    with open(txt_file) as txt_tags:
        for custom_tags in txt_tags:
            custom_tags = custom_tags.strip()
            print("|--" + custom_tags)
            tag_name_add = custom_tags.split(': ')
            contributor = tag_name_add[-1].split(', ')
            tag_values = ' / '.join(contributor)
            tags_dict[tag_name_add[0]] = tag_values
else:
    print("|")
    print("|--Enter Tag Name first and Enter Tag Value second.")
    print("|--When finished, Type 'done' in Tag Name.")

    while True:
        enter_tag_name = input("|--Enter Tag Name: ")
        if enter_tag_name.lower() == "done":
            break
        else:
            tag_value = input("|--" + enter_tag_name + ": ")
            contributor = tag_value.split(', ')
            tag_values = ' / '.join(contributor)
            tags_dict[enter_tag_name] = tag_values

tags_node = Element('Tags')
tag_node = Element('Tag')
for key, values in tags_dict.items():
    simple_node = Element('Simple')
    name_node = Element('Name')
    name_node.text = key
    simple_node.append(name_node)
    string_node = Element('String')
    string_node.text = values
    simple_node.append(string_node)
    tag_node.append(simple_node)

tags_node.append(tag_node)
xml_data = tostring(tags_node)

def execute_propedit():
    cmd_line = '"' + os.path.abspath(file_path) + '" --tags all:' + xml_name + ' --edit info '
    if title_name.lower() == "delete":
        cmd_line = cmd_line + "--delete title "
    else:
        cmd_line = cmd_line + '--set title="' + title_name + '" '
    print("|")
    print("|--Do you want to remove 'Encoded date'?")
    delete_encoded_date = input("|--Type 'Yes' or 'No': ")
    print("|")
    print("|--Do you want to remove 'Writing application'?")
    delete_writing_application = input("|--Type 'Yes' or 'No': ")
    print("|")
    print("|--Do you want to remove 'Writing library'?")
    delete_writing_library = input("|--Type 'Yes' or 'No': ")
    if delete_encoded_date.lower() == "yes":
        cmd_line = cmd_line + "--delete date "
    if delete_writing_application.lower() == "yes":
        cmd_line = cmd_line + '--set writing-application="" '
    if delete_writing_library.lower() == "yes":
        cmd_line = cmd_line + '--set muxing-application="" '
    command = f'mkvpropedit {cmd_line}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('\n')
    print(process.stdout.decode())

print("|")
print("|--Do you want to save tags as a XML file?")
save_xml = input("|--Type 'Yes' or 'No': ")
if save_xml.lower() == "yes":
    save_location = os.path.abspath(input("|--Enter folder path to save XML file: "))
    os.chdir(save_location)    
    with open(xml_name, 'wb') as xml_file:
        xml_file.write(xml_data)
    execute_propedit()
else:
    with open(xml_name, 'wb') as xml_file:
        xml_file.write(xml_data)
    execute_propedit()
    os.remove(xml_name)

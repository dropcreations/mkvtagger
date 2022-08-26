import os
import sys
import subprocess
from xml.etree.ElementTree import Element, tostring

tagsDict = {}
inputList = []
inputCount = len(sys.argv)

# Collects tag names and tag values to a dictionary

def get_tags(inputFile):
    
    """ Collecting tag data """

    print(
        f"\nMatroska/WebM Tags : {os.path.basename(inputFile)}\
        \n|"
    )
    global Title; Title = input("|--Title: ")
    tagsText = input(
        "|\
        \n|--Do you want to add tags from a text document? [y/n] "
    )
    if (tagsText.lower() == "y") or (tagsText.lower() == "yes"):
        tagsTextPath = input("|--Text document's path: ")
        if tagsTextPath.startswith('"') and tagsTextPath.endswith('"'):
                tagsTextPath = tagsTextPath[1:-1]
        print("|")
        textFolder = os.path.dirname(tagsTextPath)
        textFile = os.path.basename(tagsTextPath)
        os.chdir(textFolder)
        with open(textFile) as txtDoc:
            for customTag in txtDoc:
                customTag = customTag.strip()
                print("|--" + customTag)
                tagName = customTag.split(': ')
                tagValue = tagName[1].split(', ')
                tagValue = ', '.join(tagValue)
                tagsDict[tagName[0]] = tagValue
    elif (tagsText.lower() == "n") or (tagsText.lower() == "no"):
        print("|")
        print("|--Type [tag name] first and [tag value] second.")
        print("|--When finished, Type 'done' in [tag name].")
        print("|")
        while True:
            tagName = input("|--Tag name: ")
            if tagName.lower() == "done":
                break
            else:
                tagValue = input(f'|--{tagName}: ')
                tagValue = tagValue.split(', ')
                tagValue = ', '.join(tagValue)
                tagsDict[tagName] = tagValue
    else:
        print('\nInput is invalid.\nTry again...')
        exit()

# Generates a xml file with the tag data in the dictionary

def generate_xml(inputFile, xmlPath):
    get_tags(inputFile)
    nodeTags = Element('Tags')
    nodeTag = Element('Tag')
    for name, value in tagsDict.items():
        nodeSimple = Element('Simple')
        nodeName = Element('Name')
        nodeName.text = name
        nodeSimple.append(nodeName)
        nodeString = Element('String')
        nodeString.text = value
        nodeSimple.append(nodeString)
        nodeTagLanguageIETF = Element('TagLanguageIETF')
        nodeTagLanguageIETF.text = 'und'
        nodeSimple.append(nodeTagLanguageIETF)
        nodeTag.append(nodeSimple)
    nodeTags.append(nodeTag)
    xmlFile = tostring(nodeTags)
    xmlFile = b'<?xml version="1.0" encoding="UTF-8"?>' + xmlFile

    with open(xmlPath, 'wb') as xmlDoc:
        xmlDoc.write(xmlFile)

# process the xml file with mkvpropedit.

def process_mkvpropedit(inputFile, xmlPath):
    generate_xml(inputFile, xmlPath)

    commandLine = f'"{os.path.abspath(inputFile)}" --tags all:"{xmlPath}" '
    if Title.lower() == "delete":
        commandLine = commandLine + f'--edit info --delete title '
    elif Title:
        commandLine = commandLine + f'--edit info --set title="{Title}" '
    elif not Title:
        commandLine = commandLine

    encodedDate = input('\nDo you want to remove encoded date? [y/n] ')
    writingApplication = input('Do you want to remove writing application? [y/n] ')
    writingLibrary = input('Do you want to remove writing library? [y/n] ')

    if (encodedDate == "y") or (encodedDate == "yes"):
        commandLine = commandLine + f'--delete date '
    if (writingApplication == "y") or (writingApplication == "yes"):
        commandLine = commandLine + f'--set writing-application="" '
    if (writingLibrary == "y") or (writingLibrary == "yes"):
        commandLine = commandLine + f'--set muxing-application="" '

    command = f'mkvpropedit {commandLine}'
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print('\n' + process.stdout.decode())

    saveXML = input(f'Do you want to keep "{xmlPath}"? [y/n] ')
    if (saveXML.lower() == 'y') or (saveXML.lower() == 'yes'):
        subprocess.run(f'xmlformat --overwrite {xmlPath}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        os.remove(xmlPath)

def main():
    if inputCount == 2:
        if os.path.isfile(sys.argv[1]) is False:
            for inputFile in os.listdir(sys.argv[1]):
                if os.path.splitext(inputFile)[1] in ['.mkv', '.webm']:
                    inputList.append(inputFile)
            os.chdir(sys.argv[1])
        else:
            inputList.append(sys.argv[1])
    elif inputCount > 2:
        for inputID in range(1, inputCount):
            inputList.append(sys.argv[inputID])
    else:
        print(f'Please provide inputs...')

    for file in inputList:
        sourceFolder = os.path.dirname(file)
        sourceName = os.path.splitext(file)[0]
        xml = os.path.join(sourceFolder, (f'{sourceName}_tags.xml'))
        process_mkvpropedit(file, xml)

if __name__ == "__main__":
    main()

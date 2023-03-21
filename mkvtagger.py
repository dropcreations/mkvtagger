import os
import argparse
import subprocess
from log import Logger
from xml.etree.ElementTree import Element, tostring

logger = Logger()

class MKVTagger(object):
    def __init__(self, _input: list):
        inputs = []
        logger.info("Proccessing user inputs...")

        for input_ in _input:
            self.input_file = os.path.abspath(input_)
            if not os.path.isfile(self.input_file): inputs.extend(self.__process_dir())
            else: inputs.append(self.input_file)
        
        if len(inputs) > 0: self.input_file = inputs
        else: logger.error("Failed to find inputs!", 1)

    def __process_dir(self):
        content = os.listdir(self.input_file)
        content = [os.path.join(self.input_file, file) for file in content if os.path.splitext(file)[-1] in [".mkv", ".webm"]]
        if len(content) > 0: return content
        else: return []

    def __process_value(self, value):
        value = value.strip()
        value = value.split(',')
        return [_value.strip() for _value in value]

    def __get_tags(self, tags_text):
        __tags = {}

        if tags_text:
            logger.info("Fetching tags from text file...")
            with open(tags_text) as t:
                print()
                for tag_line in t:
                    tag_line = tag_line.strip()
                    tag_name = tag_line.split(':')
                    tag_value = self.__process_value(tag_name[1].strip())
                    tag_name = tag_name[0].strip()
                    tag_name = tag_name.replace(" ", "_")
                    tag_name = tag_name.replace("-", "")
                    print(f"{tag_name.upper(): <28}: {', '.join(tag_value)}")
                    __tags[tag_name.upper()] = tag_value
                    if tag_name.upper() == "TITLE": self.is_title = True
                    else: self.is_title = False
                print()
        else:
            logger.info("Getting tags from user...")

            __tags["TITLE"] = self.__process_value(input("\nTITLE: "))
            if __tags["TITLE"] != "": self.is_title = True
            else: self.is_title = False
            __tags["SUBTITLE"] = self.__process_value(input("SUBTITLE: "))
            __tags["ARTIST"] = self.__process_value(input("ARTIST: "))
            __tags["LEAD_PERFORMER"] = self.__process_value(input("LEAD_PERFORMER: "))
            __tags["ACCOMPANIMENT"] = self.__process_value(input("ACCOMPANIMENT: "))
            __tags["COMPOSER"] = self.__process_value(input("COMPOSER: "))
            __tags["ARRANGER"] = self.__process_value(input("ARRANGER: "))
            __tags["LYRICS"] = self.__process_value(input("LYRICS: "))
            __tags["LYRICIST"] = self.__process_value(input("LYRICIST: "))
            __tags["CONDUCTOR"] = self.__process_value(input("CONDUCTOR: "))
            __tags["DIRECTOR"] = self.__process_value(input("DIRECTOR: "))
            __tags["ASSISTANT_DIRECTOR"] = self.__process_value(input("ASSISTANT_DIRECTOR: "))
            __tags["DIRECTOR_OF_PHOTOGRAPHY"] = self.__process_value(input("DIRECTOR_OF_PHOTOGRAPHY: "))
            __tags["SOUND_ENGINEER"] = self.__process_value(input("SOUND_ENGINEER: "))
            __tags["ART_DIRECTOR"] = self.__process_value(input("ART_DIRECTOR: "))
            __tags["PRODUCTION_DESIGNER"] = self.__process_value(input("PRODUCTION_DESIGNER: "))
            __tags["CHOREGRAPHER"] = self.__process_value(input("CHOREGRAPHER: "))
            __tags["COSTUME_DESIGNER"] = self.__process_value(input("COSTUME_DESIGNER: "))
            __tags["ACTOR"] = self.__process_value(input("ACTOR: "))
            __tags["WRITTEN_BY"] = self.__process_value(input("WRITTEN_BY: "))
            __tags["SCREENPLAY_BY"] = self.__process_value(input("SCREENPLAY_BY: "))
            __tags["EDITED_BY"] = self.__process_value(input("EDITED_BY: "))
            __tags["PRODUCER"] = self.__process_value(input("PRODUCER: "))
            __tags["COPRODUCER"] = self.__process_value(input("COPRODUCER: "))
            __tags["EXECUTIVE_PRODUCER"] = self.__process_value(input("EXECUTIVE_PRODUCER: "))
            __tags["DISTRIBUTED_BY"] = self.__process_value(input("DISTRIBUTED_BY: "))
            __tags["PRODUCTION_STUDIO"] = self.__process_value(input("PRODUCTION_STUDIO: "))
            __tags["PUBLISHER"] = self.__process_value(input("PUBLISHER: "))
            __tags["LABEL"] = self.__process_value(input("RECORD_LABEL: "))
            __tags["GENRE"] = self.__process_value(input("GENRE: "))
            __tags["CONTENT_TYPE"] = self.__process_value(input("CONTENT_TYPE: "))
            __tags["LAW_RATING"] = self.__process_value(input("LAW_RATING: "))
            __tags["DATE_RELEASED"] = self.__process_value(input("DATE_RELEASED: "))
            __tags["DESCRIPTION"] = self.__process_value(input("DESCRIPTION: "))
            __tags["COMMENT"] = self.__process_value(input("COMMENT: "))
            __tags["LAW_RATING"] = self.__process_value(input("LAW_RATING: "))
            __tags["ISRC"] = self.__process_value(input("ISRC: "))
            __tags["BARCODE"] = self.__process_value(input("BARCODE: "))
            __tags["IMDB"] = self.__process_value(input("IMDB_ID: "))
            __tags["TMDB"] = self.__process_value(input("TMDB_ID: "))
            __tags["COPYRIGHT"] = self.__process_value(input("COPYRIGHT: "))
            __tags["LICENSE"] = self.__process_value(input("LICENSE: "))

            _more = input("\nDo you want to add more custom tags? [y/n] ")
            if _more.lower() == "y":
                print("\nType [tag name] first and [tag value] second.")
                print("When finished, leave [tag name] as blank.\n")
                while True:
                    tag_name = input("Tag name: ")
                    if tag_name == "":
                        break
                    else:
                        tag_value = self.__process_value(input(f'{tag_name.upper()}: '))
                        __tags[tag_name.upper()] = tag_value
            print()

        return __tags

    def __generate_xml(self, tags: dict, multi):
        node_tags = Element('Tags')
        node_tag = Element('Tag')

        for name, value in tags.items():
            if value != [""]:
                node_simple = Element('Simple')
                node_name = Element('Name')
                node_name.text = name
                node_simple.append(node_name)
                node_string = Element('String')
                if multi: node_string.text = "\n".join(value)
                else: node_string.text = ", ".join(value)
                node_simple.append(node_string)
                node_tagLanguageIETF = Element('TagLanguageIETF')
                node_tagLanguageIETF.text = 'und'
                node_simple.append(node_tagLanguageIETF)
                node_tag.append(node_simple)

        node_tags.append(node_tag)
        
        __xml = tostring(node_tags)
        __xml = b'<?xml version="1.0" encoding="UTF-8"?>' + __xml
        logger.info("Creating temporary xml...")
        with open("tags_temp.xml", "wb") as x: x.write(__xml)
    
    def process(self, tags_text, multi, enc_date, wrt_app, wrt_lib):
        self.__generate_xml(self.__get_tags(tags_text), multi)

        cmd_args = '"{input_file}" --tags all:"tags_temp.xml" '
        if self.is_title: cmd_args += "--edit info --delete title "
        if enc_date: cmd_args += "--delete date "
        if wrt_app: cmd_args += '--set writing-application="" '
        if wrt_lib: cmd_args += '--set muxing-application="" '

        for i in self.input_file:
            cmd = f'mkvpropedit {cmd_args.format(input_file=i)}'
            logger.info("Tagging file...")
            process = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            cmd = ""
            logger.info(f'File: {i}')
            print(f"\n{process.stdout.decode()}")
        
        os.remove("tags_temp.xml")
    
def main():
    parser = argparse.ArgumentParser(description="Tag MKV/WebM files with OFFICIAL or UNOFFICIAL tags with multiple tag value support.")
    parser.add_argument("-t", "--tags", dest="tags", default=None, type=str, help="Add tags from a text file")
    parser.add_argument("-m", "--multi", dest="multi", action="store_true", help="Use multiple tag values")
    parser.add_argument("--no-encoded-date", dest="enc_date", action="store_true", help="Remove encoded date")
    parser.add_argument("--no-writing-application", dest="wrt_app", action="store_true", help="Remove writing application")
    parser.add_argument("--no-writing-library", dest="wrt_lib", action="store_true", help="Remove writing library")
    parser.add_argument("inputs", nargs="*", type=str, help="Add input files or folders")
    args = parser.parse_args()
    
    tagger = MKVTagger(args.inputs)
    tagger.process(args.tags, args.multi, args.enc_date, args.wrt_app, args.wrt_lib)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
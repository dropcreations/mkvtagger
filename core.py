import os
import subprocess
from xml.etree.ElementTree import Element, tostring

from utils import logger

class MKVTagger(object):
    def __init__(self, _input: list) -> None:
        inputs = []
        logger.info("Processing inputs...")

        for input_ in _input:
            self.input_file = os.path.abspath(input_)
            if not os.path.isfile(self.input_file): inputs.extend(self.__process_dir())
            else: inputs.append(self.input_file)
        
        if len(inputs) > 0: self.input_file = inputs
        else: logger.error("Failed to find inputs!", 1)

    def __process_dir(self) -> list:
        content = os.listdir(self.input_file)
        content = [os.path.join(self.input_file, file) for file in content if os.path.splitext(file)[-1] in [".mkv", ".webm"]]

        if len(content) > 0:
            return content
        else:
            return []

    def __process_value(self, value: str) -> list:
        value = value.strip()
        value = value.split(',')

        return [_value.strip() for _value in value]

    def __get_tags(self, tags_text) -> dict:
        __tags = {}

        if tags_text:
            logger.info("Fetching tags from text file...")
            with open(tags_text) as t:
                print()
                for tag_line in t:
                    tag_line = tag_line.strip()
                    tag_name = tag_line.split(':')

                    tag_value = self.__process_value(
                        tag_name[1].strip()
                    )

                    tag_name = tag_name[0].strip()
                    tag_name = tag_name.replace(" ", "_")
                    tag_name = tag_name.replace("-", "")

                    print(f"{tag_name.upper(): <28}: {', '.join(tag_value)}")

                    __tags[tag_name.upper()] = tag_value

                    if tag_name.upper() == "TITLE":
                        self.is_title = True
                    else:
                        self.is_title = False
                print()
        else:
            logger.info("Getting tags from user...")

            __tags["TITLE"] = self.__process_value(input("\n\tTITLE: "))

            if __tags["TITLE"] != "":
                self.is_title = True
            else:
                self.is_title = False

            __tags["SUBTITLE"] = self.__process_value(input("\tSUBTITLE: "))
            __tags["ARTIST"] = self.__process_value(input("\tARTIST: "))
            __tags["LEAD_PERFORMER"] = self.__process_value(input("\tLEAD_PERFORMER: "))
            __tags["ACCOMPANIMENT"] = self.__process_value(input("\tACCOMPANIMENT: "))
            __tags["COMPOSER"] = self.__process_value(input("\tCOMPOSER: "))
            __tags["ARRANGER"] = self.__process_value(input("\tARRANGER: "))
            __tags["LYRICS"] = self.__process_value(input("\tLYRICS: "))
            __tags["LYRICIST"] = self.__process_value(input("\tLYRICIST: "))
            __tags["CONDUCTOR"] = self.__process_value(input("\tCONDUCTOR: "))
            __tags["DIRECTOR"] = self.__process_value(input("\tDIRECTOR: "))
            __tags["ASSISTANT_DIRECTOR"] = self.__process_value(input("\tASSISTANT_DIRECTOR: "))
            __tags["DIRECTOR_OF_PHOTOGRAPHY"] = self.__process_value(input("\tDIRECTOR_OF_PHOTOGRAPHY: "))
            __tags["SOUND_ENGINEER"] = self.__process_value(input("\tSOUND_ENGINEER: "))
            __tags["ART_DIRECTOR"] = self.__process_value(input("\tART_DIRECTOR: "))
            __tags["PRODUCTION_DESIGNER"] = self.__process_value(input("\tPRODUCTION_DESIGNER: "))
            __tags["CHOREGRAPHER"] = self.__process_value(input("\tCHOREGRAPHER: "))
            __tags["COSTUME_DESIGNER"] = self.__process_value(input("\tCOSTUME_DESIGNER: "))
            __tags["ACTOR"] = self.__process_value(input("\tACTOR: "))
            __tags["WRITTEN_BY"] = self.__process_value(input("\tWRITTEN_BY: "))
            __tags["SCREENPLAY_BY"] = self.__process_value(input("\tSCREENPLAY_BY: "))
            __tags["EDITED_BY"] = self.__process_value(input("\tEDITED_BY: "))
            __tags["PRODUCER"] = self.__process_value(input("\tPRODUCER: "))
            __tags["COPRODUCER"] = self.__process_value(input("\tCOPRODUCER: "))
            __tags["EXECUTIVE_PRODUCER"] = self.__process_value(input("\tEXECUTIVE_PRODUCER: "))
            __tags["DISTRIBUTED_BY"] = self.__process_value(input("\tDISTRIBUTED_BY: "))
            __tags["PRODUCTION_STUDIO"] = self.__process_value(input("\tPRODUCTION_STUDIO: "))
            __tags["PUBLISHER"] = self.__process_value(input("\tPUBLISHER: "))
            __tags["LABEL"] = self.__process_value(input("\tRECORD_LABEL: "))
            __tags["GENRE"] = self.__process_value(input("\tGENRE: "))
            __tags["CONTENT_TYPE"] = self.__process_value(input("\tCONTENT_TYPE: "))
            __tags["LAW_RATING"] = self.__process_value(input("\tLAW_RATING: "))
            __tags["DATE_RELEASED"] = self.__process_value(input("\tDATE_RELEASED: "))
            __tags["DESCRIPTION"] = self.__process_value(input("\tDESCRIPTION: "))
            __tags["COMMENT"] = self.__process_value(input("\tCOMMENT: "))
            __tags["LAW_RATING"] = self.__process_value(input("\tLAW_RATING: "))
            __tags["ISRC"] = self.__process_value(input("\tISRC: "))
            __tags["BARCODE"] = self.__process_value(input("\tBARCODE: "))
            __tags["IMDB"] = self.__process_value(input("\tIMDB_ID: "))
            __tags["TMDB"] = self.__process_value(input("\tTMDB_ID: "))
            __tags["COPYRIGHT"] = self.__process_value(input("\tCOPYRIGHT: "))
            __tags["LICENSE"] = self.__process_value(input("\tLICENSE: "))

            _more = input("\n\tDo you want to add more custom tags? [y/n] ")
            if _more.lower() == "y":
                print("\n\tType [tag name] first and [tag value] second.")
                print("\tWhen finished, leave [tag name] as blank.\n")

                while True:
                    tag_name = input("\tTag name: ")

                    if tag_name == "":
                        break
                    else:
                        tag_value = self.__process_value(input(f'\t{tag_name.upper()}: '))
                        __tags[tag_name.upper()] = tag_value
            print()

        return __tags

    def __generate_xml(self, tags: dict, multi) -> None:
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
        with open("tags_temp.xml", "wb") as x:
            x.write(__xml)
    
    def process(self, tags_text, multi, enc_date, wrt_app, wrt_lib) -> None:
        self.__generate_xml(
            self.__get_tags(
                tags_text
            ),
            multi
        )

        cmd_args = '"{}" --tags all:"tags_temp.xml" '

        if self.is_title: cmd_args += "--edit info --delete title "
        if enc_date: cmd_args += "--delete date "
        if wrt_app: cmd_args += '--set writing-application="" '
        if wrt_lib: cmd_args += '--set muxing-application="" '

        for i in self.input_file:
            cmd = f'mkvpropedit {cmd_args.format(i)}'
            logger.info(f'Tagging "{os.path.basename(i)}"...')

            subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            ).wait()

            cmd = ""
        
        if os.path.exists("tags_temp.xml"):
            os.remove("tags_temp.xml")
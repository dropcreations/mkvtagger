# __mkvtagger__

A python program to tag __MKV & WebM__ media files using __mkvpropedit__ from MKVToolNix.

<p align="center">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/dropcreations/MKV-Tagger/main/assets/logo-for-dark.png">
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/dropcreations/MKV-Tagger/main/assets/logo-for-light.png">
        <img alt="Matroska" src="https://raw.githubusercontent.com/dropcreations/MKV-Tagger/main/assets/logo-for-light.png">
    </picture>
</p>

## __Features__

- Adds official Matroska tags as well as unofficial custom tags.
- Can add tag values as a single tag value or multiple tag values.
- Removes encoded date, writing application, writing library tags if you need.
- Refer [here](https://www.matroska.org/technical/tagging.html) for official tag names.

## __How to use?__

First of all clone this project or download the project as a zip file and extract it to your pc (Windows users can see [Releases](https://github.com/dropcreations/mkvtagger/releases). Make sure you have __mkvpropedit__ in your system `PATH`.

```
git clone https://github.com/dropcreations/mkvtagger.git && cd mkvtagger
```

Install required modules for python (use `pip3` if `pip` doesn't work for you), This program uses only one module from outside.

```
pip install rich
```

You can add tags by a text file `.txt`. If you don't need a text file to add tags, you can simply add tags when console asked.
If you're using a text file, text file's content must be formatted as below.

```
TAG NAME: TAG VALUE
TAG NAME: TAG VALUE, TAG VALUE
.
.
```

and use `-t` or `--tags` argument as below.

```
python mkvtagger.py -t [text_file.txt] [inputs]
```

If you want to add tag values as multiple tags, use `-m` or `--multi` parameter as below.

```
python mkvtagger.py -m [input]
```

You can tag bulk files at once with the same tag-value pairs. Folder input is also support as wells as file input.
If you have a folder containing `.mkv` and `.webm` files that you want to tag each as same. Put the folder path as the input.
That folder can contain any other files. no matter. this script filters the `.mkv` and `.webm` files.
You can add multiple inputs as below.

```
python mkvtagger.py [input-file] [input-file] [input-folder] [input-folder]
```

Get help using `-h` or `--help` parameter

```
usage: mkvtagger.py [-h] [-v] [-m] [-t TAGS] [--no-encoded-date] [--no-writing-application] [--no-writing-library] [inputs ...]

Tag MKV/WebM files with OFFICIAL or UNOFFICIAL tags with multiple tag value support.

positional arguments:
  inputs                        Add input files or folders

optional arguments:
  -h, --help                    show this help message and exit
  -v, --version                 show program's version number and exit
  -m, --multi                   Use multiple tag values
  -t TAGS, --tags TAGS          Add tags from a text file
  --no-encoded-date             Remove encoded date
  --no-writing-application      Remove writing application
  --no-writing-library          Remove writing library
```

## About me

Hi, You might recognize me as GitHub's [dropcreations](https://github.com/dropcreations).

__Other useful python scripts done by me__

| Project            | Github location                                      |
|--------------------|------------------------------------------------------|
| MKVExtractor       | https://github.com/dropcreations/MKVExtractor        |
| FLAC-Tagger        | https://github.com/dropcreations/FLAC-Tagger         |
| MP4/M4A-Tagger     | https://github.com/dropcreations/MP4-Tagger          |
| Apple-Music-Tagger | https://github.com/dropcreations/Apple-Music-Tagger  |

<br>

- __NOTE: If you found any issue using this script mention in issues section__

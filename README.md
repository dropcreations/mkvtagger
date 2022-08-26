<!-- PROJECT INTRO -->

# __MKV/WebM Tagger__

- This program is to tag __MKV / WebM__ media files using __mkvpropedit__ from MKVToolNix.
- Make sure you have installed __mkvpropedit__.

## __Installation__

1) First clone the repo.
```shell
git clone https://github.com/dropcreations/MKV_Tagger.git && cd MKV_Tagger
```
2) Install `mkvtagger`.
```shell
pip install --editable .
```

## __Usage__

- You can add one or more files at once.
```shell
mkvtagger [file_01] [file_02] [file_03]...
```
- You can also add a folder that includes MKV and WebM files.
- Don't add more than one folder.
```shell
mkvtagger [folder_path]
```

## __Explanation__

- You can add multiple values to a tag by seperating it with a comma and a space (', ').

    `eg : Tag_Value_01, Tag_Value_02, Tag_Value_03,...`

- Save all tags to a text file or type one by one while running.
- If you are using a text file to add tags, text file's format must be as below.

    `Tag_Name_01: Tag_Value_01, Tag_Value_02, Tag_Value_03,...`<br>
    `Tag_Name_02: Tag_Value_01, Tag_Value_02, Tag_Value_03,...`

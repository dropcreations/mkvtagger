# **MKV/MKA/MKS Tagger**

- This **python script** is to tag **MKV/MKA/MKS** media files using **mkvpropedit** in MKVToolNix.
- Make sure you have installed **mkvpropedit** in **MKVToolNix**.

## **Usage**

- If you want, add **`mkvtagger.py`** file to **System Variables**.
- Open **Terminal** and type below command.
- You can add one MKV/MKA/MKS media file at once.

**`python mkvtagger.py [mkv_or_mka_or_mks_file_path]`**

## **Explanation**

- You can add multiple values to a tag by seperating it with a comma and a space (', ').
  <br>
  `eg : tag value 1, tag value 2, tag value 3,......`
  <br>
- Save all custom tags to text file or type one by one while running the script.
- If you are using a text file to add custom tags, text file's format must be as below.<br>
  <br>
  `Tag name: tag value, tag value, tag value,....`<br>
  `Tag name: tag value, tag value, tag value,....`<br>
  <br>
 eg:<br>
 `Director: Jon Watts`<br>
 `Original Music Composer: Michael Giacchino`<br>
 `Distribution: Columbia Pictures, Sony Pictures Releasing`<br>
 `Cast: Tom Holland, Zendaya, Andrew Garfield, Tobey Maguire, Marisa Tomei`<br>
 <br>

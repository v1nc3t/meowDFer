# meowDFer
### Extract, Convert, Merge
This is a tool made to simplify the processes mentioned above.

## How to use 

##### Example commands:

- `py -m src extract --src "s_name" --dest "d_name"`
- `py -m src convert --src "s_name" --dest "d_name"`
- `py -m src merge --src "s_name" --dest "d_name" --vol "v_name.txt"`
- `py -m src all --src "s_name" --dest "d_name" --vol "v_name.txt"`
- `py -m src cm --src "s_name" --dest "d_name" --vol "v_name.txt"`

## `extract`

Extracts multiple zip files into one folder.

1. Create a folder in root, put all .zip files inside. 
2. In the root of the directory, open the terminal and run:

```py -m src extract --src "s_name" --dest "d_name"```
- s_name: name of folder with zip files
- d_name: name of folder where files to be extracted in

3. Folder with d_name will be created in root with extracted zip files

## `convert`

Converts folder with images (chapters) into PDFs. Folders with images must contain 'chapter', 'ch.', or 'c' with a number. Decimal number chapters get skipped.

1. Create a folder containing folders of images with chapter and number in name. Or have the folders from 'extract'.
2. In the root of the directory, open terminal and run:

```py -m src convert --src "s_name" --dest "d_name"```
- s_name: name of folder with image folders
- d_name: name of folder where chapter PDFs to be extracted in

3. Folder with d_name will be created in root with PDFs of chapters.

## `merge`

Merge many PDF s (chapters) into volumes, using a .txt file. In the .txt file write the upper limit chapter number of a volume separated by a comma. (e.g. "3, 5, 7, 9")

1. Create a folder containing PDF chapters, or get them from step above.
2. Create a .txt file with comma separated values, which are upper limit chapter numbers.
3. In the root directory, open terminal and run:

```py -m src merge --src "s_name" --dest "d_name" --vols "v_name.txt"```
- s_name: name of folder with chapter PDFs  
- d_name: name of folder where volumes to be extracted in
- v_name.txt: name of .txt files containing all limit chapter numbers

4. Folder with d_name will be created in root with volumes.

## `all`

This combines all three commands: extract, convert, and merge. They will run one after another.

1. Create a folder in root, put all .zip files inside.
2. Create a .txt file with comma separated values, which are upper limit chapter numbers.
3. In the root directory, open terminal and run:

```py -m src all --src "s_name" --dest "d_name" --vols "v_name.txt"```
- s_name: name of folder with .zip files  
- d_name: name of folder where volumes to be extracted in
- v_name.txt: name of .txt files containing all limit chapter numbers

4. Folder with d_name will be created in root with volumes.

## `cm`

This combines two commands: convert, and merge. They will run one after another.

1. Create a folder containing folders of images with chapter and number in name. Or have the folders from 'extract'.
2. Create a .txt file with comma separated values, which are upper limit chapter numbers.
3. In the root directory, open terminal and run:

```py -m src cm --src "s_name" --dest "d_name" --vols "v_name.txt"```
- s_name: name of folder with image folders
- d_name: name of folder where volumes to be extracted in
- v_name.txt: name of .txt files containing all limit chapter numbers

4. Folder with d_name will be created in root with volumes.
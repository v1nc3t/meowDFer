# meowDFer

Compile images into PDF files. From either zip or folders, convert into chapters or volumes.

## features
- extract zip files
- convert image folders into PDF files
- merge chapter PDF file into volume PDF files


## installation & setup

### linux

1. open terminal & clone repository into desirred folder
```sh
$ git clone https://github.com/v1nc3t/meowDFer.git
$ cd meowDFer-cli
```

2. create virtual enviroment
``` sh
$ python3 -m venv .venv
```

3. activate envirometn
```sh
$ source .venv/bin/activate
```

4. install dependacies
```sh
$ pip install .
```


## usage

#### return to existing enviroment
```sh
$ source .venv/bin/activate
```

### basic syntax
for more information

```sh
$ python3 meowdfer.py -h
```

#### extract
```sh
$ python3 meowdfer.py --extract --src zips_folder --dest out_folder
```

#### convert
```sh
$ python3 meowdfer.py --convert --src img_folder --dest out_folder --name example
```

#### merge
```sh
$ python3 meowdfer.py --merge --src pdf_folder --dest out_folder --vols ./vols.txt --name example
```

#### pipelines
```sh
$ python3 meowdfer.py --convert-merge --src zips_folder --dest out_folder --vols ./vols.txt --name example
```
or
```sh
$ python3 meowdfer.py --all --src zips_folder --dest out_folder --vols ./vols.txt --name example
```

## cli options

| command flags          | description                                                                  |
|------------------------|------------------------------------------------------------------------------|
| '-e, --extract'        | extracts many .zip files from an input directory                             |
| '-c, --convert'        | converts folders with img files into PDF files (img folders -> chapters)     |
| '-m, --merge'          | merges PDF files based on a vols.txt file (chapters -> volumes)              |
| '-cm, --convert-merge' | pipelines convert, and merge                                                 |
| '-a, --all'            | pipelines extract, convert, and merge                                        |

| data flags             | description                                                                  |
|------------------------|------------------------------------------------------------------------------|
| '-s, --src'            | source folder for input                                                      |
| '-d, --dest'           | destination folder of output (if not exists, will be created)                |
| '-v, --vols'           | file with increasing numbers separated by ',' to delimit chapters in a volume|
| '-n, --name'           | name PDF files (otherwise they inherit dest folder name)                     |


## running tests
1.
```sh
$ pip install .[dev]
```

2.
```sh
$ python3 -m pytest -v
```

## dependencies

- Pillow
- pypdf
- rich
- pytest

install manually:
```sh
$ pip install <dependancy>
``` 


## contributing

1. fork the repository
2. create feature branch
3. commit changes
4. open a pull request

## licence

GNU General Public License v3
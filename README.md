# meowDFer

Compile image collections into PDF chapters and volumes.

## Features

- Extract `.zip` archives.
- Convert image folders into chapter PDFs.
- Merge chapter PDFs into volume PDFs using `vols.txt`.
- Run end-to-end pipelines:
  - convert -> merge
  - extract -> convert -> merge
- Transactional output behavior: results are staged first and moved to the destination only on success.
- Skip flag: if an error occurs during processing (e.g., invalid file format), log the error and continue to the next item instead of aborting.
- Verbose flag: enables detailed output after scraping. (source)

## Installation

! make sure to use python 3.10 or higher installed on your system

1. Clone the repository:
```sh
git clone https://github.com/v1nc3t/meowDFer.git
cd meowDFer
```

2. Create and activate a virtual environment:

```sh
python -m venv .venv
```

3. Activate the virtual environment:

### Linux
```sh
source .venv/bin/activate
```

### Windows
- powershell
```powershell
.venv\Scripts\Activate.ps1
```
- cmd
```cmd
.venv\Scripts\activate.bat
```

3. Install the package:
```sh
pip install -e .
```

Alternatively:

### Linux

2. Make script executable:
```sh
chmod +x meowdfer.py
```

3. Run it as executable:
```sh
./meowdfer.py -h
```

## Usage

Show help:
```sh
python meowdfer.py -h
```

CLI syntax:
```sh
python meowdfer.py (-e SRC DEST | -c SRC DEST | -m SRC DEST | -cm SRC DEST | -a SRC DEST | -sc NAME DEST) [-f FILE] [-n NAME] [-s] [-v]
```

Notes:

- `DEST` is created if it does not exist.
- `--name` is optional and controls output PDF names.
- `--file` is required for `--merge`, `--convert-merge`, and `--all`.
- `--skip` continues to the next item instead of aborting on error. (extract, convert, merge, pipelines)
- `--verbose` enables detailed output after scraping. (scrape)

### Extract

```sh
python meowdfer.py --extract <zips_folder> <out_folder>
```

### Convert

Input folder: 
- names should contain a chapter identifier, for example:
`c 1`, `ch 1`, `chapter 1`.
- should contain numberd images, for example:
`1.jpg`, `13.png`, `21.jpeg`

```sh
python meowdfer.py --convert <img_folders> <out_folder> --name example
```

### Merge

`vols.txt` contains increasing chapter cutoffs, for example:
```txt
1, 7, 12, 19
```

```sh
python meowdfer.py --merge <pdf_folder> <out_folder> --file ./vols.txt --name example
```

### Pipelines

Convert -> Merge:
```sh
python meowdfer.py --convert-merge <img_folders> <out_folder> --file ./vols.txt --name example
```

Extract -> Convert -> Merge:
```sh
python meowdfer.py --all <zips_folder> <out_folder> --file ./vols.txt --name example
```

### Scrape 
scrapes wikipedia for finding the chapters intervals of a manga.

```sh
python meowdfer.py --scrape <name> <out_file>
```

## CLI Options

| Command flag | Description |
|---|---|
| `-e`, `--extract SRC DEST` | Extract many `.zip` files from `SRC` into `DEST`. |
| `-c`, `--convert SRC DEST` | Convert image folders into chapter PDFs. |
| `-m`, `--merge SRC DEST` | Merge chapter PDFs into volumes based on volume interval file. |
| `-cm`, `--convert-merge SRC DEST` | Pipeline: convert and merge. |
| `-a`, `--all SRC DEST` | Pipeline: extract, convert, and merge. |
| `-sc`, `--scrape NAME DEST` | Scrape wikipedia for finding the chapters intervals of a manga. |

| Data flag | Description |
|---|---|
| `-f`, `--file FILE` | File with increasing chapter cutoffs (required for merge pipelines). |
| `-n`, `--name NAME` | Override base output name (otherwise uses destination folder name). |
| `-s`, `--skip` | On error during processing, log continue to the next item instead of aborting. | 
| `-v`, `--verbose` | Enable detailed output after scraping. |

## Running Tests

Install dev dependencies:
```sh
pip install -e ".[dev]"
```

Run tests:
```sh
pytest tests/ -v
```

## CI

GitHub Actions runs tests on:

- Pull requests
- Pushes to `main` and `master`

Workflow file: `.github/workflows/ci.yml`

## Dependencies

- Pillow
- pypdf
- rich
- requests
- beautifulsoup4
- pytest (dev)

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.

## License

GNU General Public License v3
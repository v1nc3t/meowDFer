# meowDFer

Compile image collections into PDF chapters and volumes.

## Features
- Extraxct formats: ".zip", ".tar", ".tar.gz", ".tar.bz2", ".tar.xz", ".tgz"
- Multiple commands, for each process towards making PDF (extract, convert, merge).
- Pipelines, running commangs one afte another (convert them merge, or all).
- Transactional output behavior: results are staged first and moved to the destination only on success.
- Skip flag: if an error occurs during processing (e.g., invalid file format), log the error and continue to the next item instead of aborting.
- Scrape a wikipedia or a fandom page and extract the ranges of chapters in a volume into a file (must have a table with volumes and list of chapters it contains).
- Verbose flag, for scrape, where file created has more information.

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

4. Install the package:
```sh
pip install meowdfer
```

Alternatively:

### Linux (alternatively)

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
python meowdfer.py (-e SRC DEST | -c SRC DEST | -m SRC DEST | -cm SRC DEST | -a SRC DEST | -sc URL DEST) [-t {chapter, volume}] [-f FILE] [-n NAME] [-s] [-d] [-v]
```

Notes:

- `DEST` is created if it does not exist.
- `--name` is optional and controls output PDF names.
- `--file` file containing chapter intervals for merging (required for `--merge`, `--convert-merge`, and `--all`).
- `--skip` continues to the next item instead of aborting on error. (extract, convert, merge, pipelines)
- `--verbose` enables detailed output after scraping. (scrape)
- `--type` choose conversion type, chapter of volume
- `--decimal` convert also decimal chapters (e.g. 10.5 will be added to volume of 10)

### Extract
- extract `.zip` archives.
- formats: ".zip", ".tar", ".tar.gz", ".tar.bz2", ".tar.xz", ".tgz"

```sh
python meowdfer.py --extract <zips_folder> <out_folder>
```

### Convert
- convert image folders into chapter PDFs.
- type flag: choose between 'chapter' and 'volume' depending on the type of conversion wanted.


Input folder: 
- volume identifier, for example:
`v001`, `volume 1`, `vol 1`
- chapter identifier, for example:
`c 1`, `ch 1`, `chapter 1`, `001`
- page identifier, for example: numbered images
`1.jpg`, `13.png`, `21.jpeg`


```sh
python meowdfer.py --convert <img_folders> <out_folder> --type chapter (optional: --name example --decimal --skip)
```

### Merge
- merge chapter PDFs into volume PDFs using a chapter range file (e.g., "1, 5, 7").
- with decimal flag (v10.5 will be merged into volume of v10)
- volume range file (e.g. `vols.txt`) contains increasing chapter cutoffs, for example:
```txt
1, 7, 12, 19
```

```sh
python meowdfer.py --merge <pdf_folder> <out_folder> --file ./vols.txt (optinal: --name example --decimal --skip)
```

### Pipelines

Convert -> Merge:
```sh
python meowdfer.py --convert-merge <img_folders> <out_folder> --file ./vols.txt  --type chapter (optional: --name example --decimal --skip)
```

Extract -> Convert -> Merge:
```sh
python meowdfer.py --all <zips_folder> <out_folder> --file ./vols.txt  --type volume (optional: --name example --decimal --skip)
```

### Scrape 
- scrape website, given link to a wikipedia or fandom page containing a table of volumes. Result is a list of chapter ranges for each volume.
- verbose flag: enables detailed output after scraping.
- outputs into a '.txt' file

```sh
python meowdfer.py --scrape <url> <out_file> (optional: --verbose)
```

## CLI Options

| Command flag | Description |
|---|---|
| `-e`, `--extract SRC DEST` | Extract many `.zip` files from `SRC` into `DEST`. |
| `-c`, `--convert SRC DEST` | Convert image folders into chapter PDFs. |
| `-m`, `--merge SRC DEST` | Merge chapter PDFs into volumes based on volume interval file. |
| `-cm`, `--convert-merge SRC DEST` | Pipeline: convert and merge. |
| `-a`, `--all SRC DEST` | Full pipeline: extract, convert, and merge. |
| `-sc`, `--scrape URL DEST` | Scrape wikipedia or fandom page, finding the chapters intervals of a manga. |

| Data flag | Description |
|---|---|
| `-f`, `--file FILE` | File with increasing chapter cutoffs (required for merge pipelines). |
| `-n`, `--name NAME` | Override base output name (otherwise uses destination folder name). |
| `-s`, `--skip` | Fault Tolerance: Skip files that fail instead of crashing. | 
| `-v`, `--verbose` | Enable detailed output after scraping. |
| `-t`, `--type` | processing mode for converting, either chapter or volume format (requred for convert, and pipelines). |
| `-d`, `--decimal` | Allow conversions and merge of decimal chapters, default does not. |

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
- urllib3
- pytest (dev)

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.

## License

GNU General Public License v3
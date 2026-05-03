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

## Installation

### Linux

1. Clone the repository:
```sh
git clone https://github.com/v1nc3t/meowDFer.git
cd meowDFer
```

2. Create and activate a virtual environment:
```sh
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the package:
```sh
pip install -e .
```

## Usage

Show help:
```sh
python3 meowdfer.py -h
```

CLI syntax:
```sh
python3 meowdfer.py (-e SRC DEST | -c SRC DEST | -m SRC DEST | -a SRC DEST | -cm SRC DEST) [-v VOLS] [-n NAME]
```

Notes:

- `DEST` is created if it does not exist.
- `--name` is optional and controls output PDF names.
- `--vols` is required for `--merge`, `--convert-merge`, and `--all`.

### Extract

```sh
python3 meowdfer.py --extract <zips_folder> <out_folder>
```

### Convert

Input folder: 
- names should contain a chapter identifier, for example:
`c 1`, `ch 1`, `chapter 1`.
- should contain numberd images, for example:
`1.jpg`, `13.png`, `21.jpeg`

```sh
python3 meowdfer.py --convert <img_folders> <out_folder> --name example
```

### Merge

`vols.txt` contains increasing chapter cutoffs, for example:
```txt
1, 7, 12, 19
```

```sh
python3 meowdfer.py --merge <pdf_folder> <out_folder> --vols ./vols.txt --name example
```

### Pipelines

Convert -> Merge:
```sh
python3 meowdfer.py --convert-merge <img_folders> <out_folder> --vols ./vols.txt --name example
```

Extract -> Convert -> Merge:
```sh
python3 meowdfer.py --all <zips_folder> <out_folder> --vols ./vols.txt --name example
```

## CLI Options

| Command flag | Description |
|---|---|
| `-e`, `--extract SRC DEST` | Extract many `.zip` files from `SRC` into `DEST`. |
| `-c`, `--convert SRC DEST` | Convert image folders into chapter PDFs. |
| `-m`, `--merge SRC DEST` | Merge chapter PDFs into volumes based on `vols.txt`. |
| `-cm`, `--convert-merge SRC DEST` | Pipeline: convert and merge. |
| `-a`, `--all SRC DEST` | Pipeline: extract, convert, and merge. |

| Data flag | Description |
|---|---|
| `-v`, `--vols VOLS` | File with increasing chapter cutoffs (required for merge pipelines). |
| `-n`, `--name NAME` | Override base output name (otherwise uses destination folder name). |

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
- pytest (dev)

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.

## License

GNU General Public License v3
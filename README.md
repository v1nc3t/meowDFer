# meowDFer

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)

A CLI tool for processing image collections and converting compressed archives into structured, organized PDF chapters and volumes.

---

## Features

- **Multi-Format Archive Extraction:** Supports `.zip`, `.cbz`, `.rar`, `.cbr`, `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz`, and `.tgz`.
- **Pipeline Workflows:** Run complete batch chains seamlessly (`Extract` -> `Convert` -> `Merge`).
- **Transactional File Safety:** Results are processed in temporary staging zones and moved to the final destination directory only upon success.
- **Fault-Tolerant Processing (`--skip`):** Automatically logs corrupted archives or broken folders and skips to the next item instead of aborting the entire batch.
- **Automated Web Scraping:** Scrapes Wikipedia or Fandom tables to generate volume interval mapping files (`vols.txt`) automatically.
- **Cross-Platform:** Runs natively on Linux, macOS, and Windows or via an isolated Docker container environment.

---

## Prerequisites

Before installing `meowDFer`, ensure your environment meets the following requirements:

### For Native Python Installation
- **Python:** Version `3.10` or higher.
- **System Extraction Tools:** `patoolib` depends on native system archive utilities. Ensure your system has the relevant tools installed (e.g., `p7zip-full`, `unzip`, `unrar`, `tar`).

### For Docker Installation (Recommended)
- **Docker:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running (Windows/macOS) or `docker` engine installed (Linux).

---

## Installation

### Option A: Docker (Recommended)

Running `meowDFer` via Docker guarantees all extraction backends are configured cleanly without installing dependencies directly on your host operating system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/v1nc3t/meowDFer.git
   cd meowDFer
   ```

2. **Run the automated setup for your OS:**

   * **Linux / macOS:**
     ```bash
     chmod +x install.sh
     ./install.sh
     ```
     *Builds the image and creates a global launcher executable at `/usr/local/bin/meowdfer`.*

   * **Windows (PowerShell):**
     ```powershell
     powershell -ExecutionPolicy Bypass -File .\install.ps1
     ```
     *Builds the image and appends the project folder to your User `PATH` environment variable. **Restart your terminal after installation** to refresh environment variables.*

#### Video demo installation with docker

<video width="100%" controls muted loop>
  <source src="./assets/linux_docker_install.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

---

### Option B: Native Python Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/v1nc3t/meowDFer.git
   cd meowDFer
   ```

2. **Create and activate a virtual environment:**

   * **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```

   * **Windows (Command Prompt):**
     ```cmd
     python -m venv .venv
     .\.venv\Scripts\activate.bat
     ```

3. **Install dependencies:**
   ```bash
   pip install .
   ```

---

## Usage

If installed via **Docker**, run commands using `meowdfer`. If running **natively**, run using `python meowdfer.py`.

### Basic CLI Syntax
```bash
meowdfer (-e SRC DEST | -c SRC DEST | -m SRC DEST | -cm SRC DEST | -a SRC DEST | -sc URL DEST) [OPTIONS]
```

#### Video demo usage

<video width="100%" controls muted loop>
  <source src="./assets/usage_pipeline.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

---

### Commands & Action Flags

| Action Flag | Parameters | Description |
|---|---|---|
| `-e`, `--extract` | `SRC DEST` | Unpack all supported archive files from `SRC` into `DEST`. |
| `-c`, `--convert` | `SRC DEST` | Convert image directories into chapter PDFs (requires `--type`). |
| `-m`, `--merge` | `SRC DEST` | Merge chapter PDFs into volumes (requires `--file`). |
| `-cm`, `--convert-merge` | `SRC DEST` | Pipeline: Convert image directories and merge them into volumes. |
| `-a`, `--all` | `SRC DEST` | Full Pipeline: Extract archives -> Convert to PDFs -> Merge into volumes. |
| `-sc`, `--scrape` | `URL DEST` | Scrape a Wikipedia or Fandom page to generate a volume interval text file. |

### Data & Modifier Flags

| Modifier Flag | Arguments | Description |
|---|---|---|
| `-t`, `--type` | `chapter` \| `volume` | Specify input folder structure mode (Required for `--convert`, `--convert-merge`, `--all`). |
| `-f`, `--file` | `FILE` | Path to text file containing chapter interval cutoffs for volumes. |
| `-n`, `--name` | `NAME` | Override base output filename prefix. |
| `-s`, `--skip` | *None* | Enable fault tolerance: log errors and skip failing files instead of aborting. |
| `-d`, `--decimal` | *None* | Enable parsing of decimal chapter numbers (e.g., `10.5`). |
| `-v`, `--verbose` | *None* | Enable detailed output logging during scraping. |

### Command-Specific Flags

| Command | Required Flags | Optional Flags |
|---|---|---|
| `-e`, `--extract` | none | `-s`, `--skip` |
| `-c`, `--convert` | `-t`, `--type` | `-n`, `--name`; `-s`, `--skip`; `-d`, `--decimal` |
| `-m`, `--merge` | `-f`, `--file` | `-n`, `--name`; `-s`, `--skip`; `-d`, `--decimal` |
| `-cm`, `--convert-merge` | `-t`, `--type`; `-f`, `--file` | `-n`, `--name`; `-s`, `--skip`; `-d`, `--decimal` |
| `-a`, `--all` | `-t`, `--type`; `-f`, `--file` | `-n`, `--name`; `-s`, `--skip`; `-d`, `--decimal` |
| `-sc`, `--scrape` | none | `-v`, `--verbose` |

---

## Examples

### 1. Extract Archives
Extract supported archive files into structured folders:
```bash
meowdfer -e ./downloads/zips ./extracted_folders --skip
```

### 2. Convert Image Directories to Chapter PDFs
Convert folders containing images into individual chapter PDFs:
```bash
meowdfer -c ./extracted_folders ./chapter_pdfs --type chapter --decimal
```

Expected folder conventions:
* **Volumes:** `v001`, `volume 1`, `vol 1`
* **Chapters:** `c 1`, `ch 1`, `chapter 1`, `001`
* **Pages:** `1.jpg`, `13.png`, `21.jpeg`

### 3. Scrape Volume Intervals
Scrape a Wikipedia or Fandom entry to output a `vols.txt` mapping file:
```bash
meowdfer -sc "https://en.wikipedia.org/wiki/List_of_Manga_Volumes" ./vols.txt -v
```

The generated `vols.txt` output file format:
```txt
1, 7, 12, 19, 25
```

### 4. Merge Chapter PDFs into Volume PDFs
Merge chapter PDFs using the interval mapping file:
```bash
meowdfer -m ./chapter_pdfs ./volume_pdfs --file ./vols.txt
```

### 5. Execute Full Pipeline
Run extraction, image-to-PDF conversion, and volume merging in one continuous run:
```bash
meowdfer -a ./zips_dir ./final_volumes --type volume --file ./vols.txt --skip
```

---

## Manual Docker Execution (Without Installation Scripts)

If you prefer not to use the automated `install.sh` or `install.ps1` scripts, you can execute the container manually by binding your working directory:

### Linux / macOS:
```bash
docker run --rm -it \
    --user "$(id -u):$(id -g)" \
    -v "$(pwd):$(pwd)" \
    -w "$(pwd)" \
    meowdfer:latest -a ./zips_dir ./final_volumes -t volume -f ./vols.txt
```

### Windows (Command Prompt / PowerShell):
```cmd
docker run --rm -it -v "%cd%:%cd%" -w "%cd%" meowdfer:latest -a .\zips_dir .\final_volumes -t volume -f .\vols.txt
```

---

## Running Tests

Install developer dependencies:
```bash
pip install -e ".[dev]"
```

Run test suite:
```bash
pytest tests/ -v
```

---

## CI/CD Workflow

Continuous Integration runs automatically via GitHub Actions on:
- All Pull Requests
- Pushes to `main` or `master` branches

Workflow config: `.github/workflows/ci.yml`

---

## License

Distributed under the terms of the **GNU General Public License v3**. See `LICENSE` for more information.
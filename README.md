# CABI Bike Trip Visualization

Visualize shared-bike trip data from `cabi_bike.csv` with geoplotlib.

The script creates two layers:

- A 2D density histogram of trip start locations
- Sampled routes from start points to end points

The project uses Esri World Street Map tiles. It does not use CartoDB or Stamen services that require an API key, and it does not directly use the public OpenStreetMap tile server.

## Requirements

- Python 3.8.x
- Git
- Internet access is required to install geoplotlib and download map tiles
- `cabi_bike.csv` in the project root, or a path supplied when running the script

> geoplotlib is an old package. Python 3.9 and later, or the latest pyglet and NumPy versions, may cause compatibility problems. Use Python 3.8.

## macOS Setup

### 1. Install pyenv

If Homebrew is not installed, install it from <https://brew.sh/> first.

```bash
brew install pyenv
```

Install Python 3.8:

```bash
export PATH="$(brew --prefix pyenv)/bin:$PATH"
eval "$(pyenv init -)"
pyenv install -s 3.8.18
```

### 2. Create a virtual environment

Run the following commands from the project directory:

```bash
export PATH="$(brew --prefix pyenv)/bin:$PATH"
eval "$(pyenv init -)"
export PYENV_VERSION=3.8.18
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

geoplotlib uses the legacy `use_2to3` build setting. Install older setuptools and wheel versions, then disable pip's isolated build:

```bash
python -m pip install --upgrade "pip<24.1"
python -m pip install "setuptools==57.5.0" "wheel==0.38.4"
python -m pip install --no-build-isolation -r requirements.txt
```

## Windows Setup (Not Sure)

### 1. Install the tools

Install the following tools:

- Python 3.8.x: <https://www.python.org/downloads/release/python-3810/>
- Git: <https://git-scm.com/download/win>

Select **Add Python to PATH** when installing Python.

Verify the versions:

```powershell
py -3.8 --version
git --version
```

### 2. Create a virtual environment

Open PowerShell and change to the project directory:

```powershell
py -3.8 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, allow locally signed scripts for the current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Restart PowerShell and run the activation command again.

### 3. Install dependencies

```powershell
python -m pip install --upgrade "pip<24.1"
python -m pip install "setuptools==57.5.0" "wheel==0.38.4"
python -m pip install --no-build-isolation -r requirements.txt
```

## Run

Confirm that `.venv` is being used:

macOS:

```bash
which python
python --version
```

Windows PowerShell:

```powershell
Get-Command python
python --version
```

Run the interactive map:

```bash
python visualize_cabi_bike.py
```

Use the same command in Windows PowerShell:

```powershell
python visualize_cabi_bike.py
```

The geoplotlib window opens and supports zooming and panning.

## Save PNG

Use `--save` to export a PNG. geoplotlib automatically adds `.png`, so the path can include or omit the extension:

```bash
python visualize_cabi_bike.py --save cabi_bike_geoplotlib.png
```

You can reduce the number of routes to make rendering faster:

```bash
python visualize_cabi_bike.py --sample-every 250 --save cabi_bike_geoplotlib.png
```

## CSV Format

The CSV must contain at least these columns:

```text
start_lat,start_lng,end_lat,end_lng,member_casual
```

The included data also contains ride IDs, timestamps, vehicle types, station names, and station IDs.

## Common Problems

### `ModuleNotFoundError: No module named geoplotlib`

Make sure the virtual environment is active, then reinstall:

```bash
python -m pip install --no-build-isolation -r requirements.txt
```

### `use_2to3 is invalid`

This means that setuptools is too new. Run:

```bash
python -m pip install "setuptools==57.5.0" "wheel==0.38.4"
python -m pip install --no-build-isolation -r requirements.txt
```

### `numpy` or `scipy` installation fails

Make sure the active Python is 3.8 rather than the system Python 3.13/3.14:

```bash
python --version
```

### The window closes or shows `b'invalid operation'`

This is a compatibility issue between old pyglet and the OpenGL debug checker on newer macOS versions. The script sets this before importing geoplotlib:

```python
pyglet.options["debug_gl"] = False
```

Make sure the Python executable comes from the project's `.venv`.

### The basemap reports an API key error

Do not change back to `geoplotlib.tiles_provider("positron")`; it calls an obsolete CartoDB endpoint. The script uses Esri World Street Map and displays attribution for Esri and OpenStreetMap contributors.

### The PNG has no basemap tiles

geoplotlib downloads tiles in the background, so `--save` may capture the image before all tiles finish downloading. Interactive mode normally completes the download after the window opens; wait for the first download to finish.

## Project Files

- `visualize_cabi_bike.py`: Main geoplotlib visualization script
- `visualize_cabi_bike_map.py`: Folium HTML fallback
- `requirements.txt`: Verified pinned dependency versions
- `cabi_bike.csv`: Raw trip data

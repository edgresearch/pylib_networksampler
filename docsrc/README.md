# Documentation Build Instructions

This folder contains the Sphinx source files for the NetworkSampler documentation.

## Requirements

Install the documentation dependencies:

```bash
pip install sphinx sphinx-rtd-theme
```

## Build for GitHub Pages

To generate the HTML documentation and copy it to the `../docs` folder (ready for GitHub Pages):

**Windows:**
```bash
.\make.bat github
```

**Linux / macOS:**
```bash
make github
```

The generated files will be placed in `../docs`.

## Build HTML only

To generate the HTML locally without copying to `../docs`:

**Windows:**
```bash
.\make.bat html
```

**Linux / macOS:**
```bash
make html
```

The output will be in `_build/html`.

## Clean

To remove all generated files:

**Windows:**
```bash
.\make.bat clean
```

**Linux / macOS:**
```bash
make clean
```

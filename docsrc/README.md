# Documentation Build Instructions

This folder contains the Sphinx source files for the NetworkSampler documentation.

## Deployment

Documentation is deployed automatically via GitHub Actions. Every push to `master` that modifies files in `docsrc/` or `networksampler/` triggers a build and deploy to GitHub Pages.

No manual deployment is needed.

## Local preview

To preview the documentation locally, install the dependencies:

```bash
pip install sphinx sphinx-rtd-theme
```

Then build the HTML:

**Windows:**
```bash
.\make.bat html
```

**Linux / macOS:**
```bash
make html
```

The output will be in `_build/html`. Open `_build/html/index.html` in your browser.

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

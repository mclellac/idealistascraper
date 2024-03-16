# Idealista Scraper

## Description

The `Idealista Scraper` is a script designed to scrape listings of homes for sale from any of the Idealista websites (the example in the config.yaml is Lake Como area). It extracts relevant information such as title, price (in Euro and CAD), details, photo, and link to each listing. Additionally, it provides an option to generate an HTML file containing the scraped data for easy viewing.

## Usage
### Prerequisites

    * Python 3.x
    * Required Python packages: requests, beautifulsoup4, rich, PyYAML

### Installation

#### Clone this repository:

```bash
git clone https://github.com/mclellac/idealista-scraper.git
```

### Install the required Python packages:

```bash
    pip install -r requirements.txt
```

### Configuration

Before running the script, you need to set up the config.yaml file. This file should contain the URL of the Idealista search results page with your desired filters applied. You can obtain this URL by configuring your search criteria on the Idealista website (region, country, draw area, custom filters if you have any) and copying the URL from the browser's address bar into the YAML `url:` fieldset.

### Example config.yaml:

```yaml
url: https://www.idealista.it/en/venta-viviendas/roma-roma/con-prezzo_130000-200000,con-foto,media-ante-4/settimane/
```

### Running the Script

To execute the script, navigate to the project directory and run:

```bash
python idealista.py
```

or

```bash
python idealista.py --generate-html
```


This will, as the name implies, scrape the Idealista listings based on the provided URL. It will output a table of the results to stdout. if `--generate-html` is supplied as a flag, it will generate an HTML file (placed in: html/index.html) containing a table of the data, including the display photo. You can open this HTML file in any web browser to view the listings.

## Author

Created by `mclellac`
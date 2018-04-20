# NESA Past Papers Scraper
A web scraper for
[NESA HSC past paper links](http://educationstandards.nsw.edu.au/wps/portal/nesa/11-12/Understanding-the-curriculum/resources/hsc-exam-papers),
built with Scrapy on Python 2.7.14

This project is freely available under the [MIT Licence](https://github.com/notseenee/nesappscraper/blob/master/LICENSE).
Please link back to this repo! :)

This scraper was built to get links for all past paper documents for 
http://hscpastpapers.com

---

## Table of contents
* [Get the data](#get-the-data)
* [Data format](#data-format)
    * [JSON Schema](#json-schema)
    * [Description](#description)
* [Running the scraper yourself](#running-the-scraper-yourself)
    * [Running on Scrapy Cloud](#running-on-scrapy-cloud)
    * [Changing output filename](#changing-output-filename)
    * [Runtime stats](#runtime-stats)
* [NESA HSC Paper upload schedule](#nesa-hsc-paper-upload-schedule)
* [Acknowledgements](#acknowledgements)

---
## Get the data
### https://raw.githubusercontent.com/notseenee/nesappscraper/master/data.json

Check [`meta.json`](https://raw.githubusercontent.com/notseenee/nesappscraper/master/meta.json)
to see when `data.json` was last updated and how many items it scraped.

## Data format
### JSON Schema
```javascript
{
    "type": "array",
    "items": {
        "object": "course_item",
        "type": "object",
        "properties": {
            "course_name": { "type": "string" },
            "packs": {
                "type": "array",
                "items": {
                    "object": "exam_pack_item"
                    "type": "object",
                    "properties": {
                        "docs": {
                            "type": "array",
                            "items": {
                                "object": "doc_item",
                                "type": "object",
                                "properties": { 
                                    "doc_name": { "type": "string" },
                                    "doc_link": { "type": "string" }
                                }
                            }
                        }
                        "link": { "type": "string" },
                        "year": { "type": "number" }
                    }
                }
            }
        }
    }
}
```
### Description
* The first level is an array of `course_item` objects.
* `course_item` is an object for each HSC course and each object contains:
    * `course_name`, a string containing the course name and
    * `packs`, an array of `exam_pack_item` objects.
* `exam_pack_item` is an object for each year there are documents available for
  each course. Each object contains:
    * `docs`, an array of `doc_item` objects,
    * `link`, a string containing the link to the exam pack, and
    * `year`, a number storing the year of the exam pack.
* `doc_item` is an object for each document within each exam pack. Each object
  contains:
    * `doc_name`, a string containing the name of the document and
    * `doc_link`, a string containing the link to the PDF document.

## Running the scraper yourself
1. Download and install Python 2.7 from https://www.python.org/downloads/
2. Download and install Scrapy. Install instructions:
   https://doc.scrapy.org/en/latest/intro/install.html
    * If installing on Windows, Miniconda is recommended.
3. Clone this repo or download ZIP using the green button above.
    * ![Image of button](https://i.imgur.com/HEa7joN.png)
4. Open a command line and browse to the downloaded copy of this repo.
   Your command line should read `.../nesappscraper-master`
    * Note: If running Anaconda/Miniconda on Windows, you may have to use
      `Anaconda Prompt` from the Start menu.
5. Enter `scrapy crawl nesapp`
    * Note: This will overwrite any `data.json` and `meta.json` files.

### Running on Scrapy Cloud
This version of the scraper will not work on Scrapy Cloud without modifications.
You need to switch the item pipeline in `settings.py`
(in the `nesappscraper` folder):

* Comment out lines 69 by putting a `#` at the start of the line.
* Uncomment line 68 by removing the `#` at the start of the line.

### Changing output filename
In `pipelines.py` inside the `nesappscraper` folder:

* On line 16, change `data.json` to the file name you want.
* On line 18, change `meta.json` to the file name you want.
* The file extension must remain `.json`

### Runtime stats
* On an Intel Core i3-6100U, the crawler ran for **~6 min**.
* On Scrapy Cloud with 1 unit, it ran for **~55 min**.
* Total data usage was **~100 MB**.
* Total request count should be **3176+** to get all papers.
* There should be **1589+** items scraped to get all papers.
* There should be **113** courses.

## NESA HSC Paper upload schedule
This crawler should be loaded frequently during the HSC exam block to get the
latest papers. In 2017, papers are usually uploaded **two business days** after
the exam, around noon.


## Acknowledgements
* Scrapy: https://scrapy.org/
* All HSC papers are provided by NESA and owned by the State of New South Wales.
  They are protected by Crown copyright:
  http://educationstandards.nsw.edu.au/wps/portal/nesa/mini-footer/copyright
* This scraper does **not** store or make copies fo the documents themselves.
  It only obtains the links to the official copies on the NESA website.
  It is intended for information purposes only.

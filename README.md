# NESA Past Papers Scraper
A web scraper for
[NESA HSC past paper links](http://educationstandards.nsw.edu.au/wps/portal/nesa/11-12/Understanding-the-curriculum/resources/hsc-exam-papers),
built with Scrapy on Python 2.7.14

This project is freely available under the [MIT Licence](https://github.com/notsidney/nesappscraper/blob/master/LICENSE).
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
### https://raw.githubusercontent.com/notsidney/nesappscraper/master/data.json

Check [`meta.json`](https://raw.githubusercontent.com/notsidney/nesappscraper/master/meta.json)
to see when `data.json` was last updated and how many items it scraped.

## Data format
### JSON Schema
Note: Each course_item is collapsed into one line.
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
1. Download and install Python 3.7 (which should include pip)
    * macOS, using Homebrew: `brew install python`
    * Windows: https://www.python.org/downloads/
2. Download and install pipenv. Instructions:
   https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv
3. Clone this repo or download ZIP using the green button above.
    * ![Image of button](https://i.imgur.com/HEa7joN.png)
4. Open the directory of the cloned or downloaded repo.
5. Install Scrapy and other dependencies using pipenv, making sure it’s using
   Python 3.7: `pipenv install`
6. Run `pipenv run scrapy crawl nesapp`
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
On a 2018 13″ MacBook Pro (i5-8259U) with ~45 Mbps download connection:
* Runtime: ~7 min
* CPU usage: typically 70–80%, spiked at 90%
* RAM usage: typically 150 MB, spiked at 350 MB
* Total bytes sent: ~700 KB
* Total bytes received: ~140 MB
* Scrapy stats: ![Screenshot of Scrapy stats from Terminal](https://imgur.com/QqIoCXe.png)

On Scrapy Cloud with 1 unit, it ran for **~55 min**.

To check if your data is valid:
* Total request count should be **1661+** to get all papers.
* There should be **1654+** items scraped to get all papers.
* There should be **114** courses.

## NESA HSC Paper upload schedule
This crawler should be loaded frequently during the HSC exam block to get the
latest papers. In 2017, papers are usually uploaded **two business days** after
the exam, around noon.


## Acknowledgements
* Scrapy: https://scrapy.org/
* All HSC papers are provided by NESA and owned by the State of New South Wales.
  They are protected by Crown copyright:
  http://educationstandards.nsw.edu.au/wps/portal/nesa/mini-footer/copyright
* This scraper does **not** store or make copies of the documents themselves.
  It only obtains the links to the official copies on the NESA website.
  It is intended for information purposes only.

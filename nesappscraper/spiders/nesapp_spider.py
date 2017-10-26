import scrapy
import logging
import json

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..items import exam_pack_item, doc_item

class NesaPPSpider(scrapy.Spider):
    name = "nesapp"
    start_urls = ['http://educationstandards.nsw.edu.au/wps/portal/nesa/11-12/Understanding-the-curriculum/resources/hsc-exam-papers']

    def parse(self, response):
        # create list of course names
        global course_names
        course_names = []
        # create list of exam pack lists
        global exam_pack_items
        exam_pack_items = []
        # loops through all courses
        for course in response.css('.res-accordion-grp'):

            # gets course name
            course_name = course.css('.res-heading::text').extract_first().strip()
            # adds to list
            course_names.append(course_name)
            # creates empty list in exam_pack_items
            exam_pack_items.append([])
            # loops through all years in each course
            for year in course.css('.res-accordion-content span a'):
                # extracts link & year for each exam pack
                exam_pack_link = response.urljoin(
                    year.css('::attr(href)').extract_first()
                )
                exam_pack_year = year.css('::text').re_first(r'[0-9]{4}')

                # create new exam_pack_item
                exam_pack_item_current = exam_pack_item(
                    course = course_name,
                    year = exam_pack_year,
                    link = exam_pack_link
                )

                # scraper follows this link to each exam pack
                exam_pack_request = scrapy.Request(
                    exam_pack_link,
                    callback = self.parse_docs
                )

                # add metadata
                exam_pack_request.meta['course'] = course_name
                exam_pack_request.meta['year'] = exam_pack_year
                exam_pack_request.meta['exam_pack_item'] = exam_pack_item_current
                # add request
                yield exam_pack_request

    def parse_docs(self, response):
        # Creates a list of all the docs on the page
        doc_items = []
        # create doc_item for each doc on the page
        for doc in response.css('.right-menu-list a'):
            doc_items.append( dict( doc_item(
                doc_link = strip_document_url(response.urljoin(
                    doc.css('::attr(href)').extract_first()
                )),
                doc_name = doc.css('::attr(data-file-name)').extract_first()
                    .lower()
                    .replace(response.meta['course'].lower(),'')
                    .replace(response.meta['year'],'')
                    .lstrip(' - ')
                    .replace('classical','')
                    .replace('modern','')
                    .replace('heritage','')
                    .replace('hebrew','')
                    .replace('continuers','')
                    .replace('chinese','')
                    .replace('(mandarin)','')
                    .replace('mandarin','')
                    .replace('background speakers','')
                    .replace('indonesian','')
                    .replace('and literature','')
                    .replace('japanese','')
                    .replace('korean','')
                    .replace('greek','')
                    .replace('extension','')
                    .replace('beginners','')
                    .replace('ancient history','')
                    .replace('english standard & advanced','')
                    .replace('comparative literature','')
                    .replace('information technology','')
                    .replace('pdhpe','')
                    .replace('physical development, health and physical education','')
                    .replace('aboriginal studies','')
                    .strip()
                    .title()
                    .replace('Hsc','HSC')
                    .replace('Ii','II')
            ) ) )
        # get unfinished exam_pack_item from response meta
        exam_pack_item = response.meta['exam_pack_item']

        # use true redirected url for exam pack
        exam_pack_item['link'] = strip_exam_pack_url(response.url)

        # add doc_items array to exam_pack_item
        exam_pack_item['docs'] = doc_items
        # Yields item
        # Note this does not yield anything if the pipeline is activated in
        # settings.
        yield dict(exam_pack_item)


# Strips unnecessary data from an exam pack url
def strip_exam_pack_url(url):
    # nothing after '/!ut/' is needed
    return url.split('/!ut/')[0]

# Strips unnecessary data from a document url
def strip_document_url(url):
    # CACHEID isn't needed
    return url.split('&CACHEID=')[0]

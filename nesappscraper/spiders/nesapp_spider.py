import scrapy
import logging

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from ..items import course_item, exam_pack_item, doc_item

class NesaPPSpider(scrapy.Spider):
    name = "nesapp"
    start_urls = ['http://educationstandards.nsw.edu.au/wps/portal/nesa/11-12/Understanding-the-curriculum/resources/hsc-exam-papers']
    #start_urls = ['file:///C:/Users/Sidney%20Alcantara/Desktop/test.html']

    def __init__(self):
        dispatcher.connect(self.output, signals.spider_closed)

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
                exam_pack_link = response.urljoin( year.css('::attr(href)').extract_first() )
                exam_pack_year = year.css('::text').re_first(r'[0-9]{4}')

                # create new exam_pack_item
                exam_pack_item_current = exam_pack_item(
                    course = course_name,
                    year = exam_pack_year,
                    link = exam_pack_link
                )

                # scraper follows this link
                exam_pack_request = scrapy.Request(exam_pack_link,callback=self.parse_docs)
                # add metadata
                exam_pack_request.meta['course'] = course_name
                exam_pack_request.meta['year'] = exam_pack_year
                exam_pack_request.meta['exam_pack_item'] = exam_pack_item_current
                # add request
                yield exam_pack_request

    def parse_docs(self, response):
        doc_items = []
        for doc in response.css('.right-menu-list a'):
            doc_items.append( doc_item(
                doc_link = response.urljoin( doc.css('::attr(href)').extract_first() ),
                doc_name = doc.css('::attr(data-file-name)').extract_first()
                    .replace(response.meta['course'],'')
                    .replace(response.meta['year'],'')
                    .strip()
                    .capitalize()
            ) )
        exam_pack_item = response.meta['exam_pack_item']
        exam_pack_item['docs'] = doc_items

        # gets index of corresponding course item
        index = course_names.index(response.meta['course'])
        # append current exam pack item
        exam_pack_items[index].append( exam_pack_item )
        yield exam_pack_item

    def output(self):
        for i in range(len(course_names)):
            course_item_output = course_item()
            course_item_output['course'] = course_names[i]
            course_item_output['packs'] = exam_pack_items[i]

            yield course_item_output

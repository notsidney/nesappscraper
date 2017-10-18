import scrapy
from scrapy import log
from ..items import course_item, exam_pack_item, doc_item

class NesaPPSpider(scrapy.Spider):
    name = "nesapp"
    start_urls = ['http://educationstandards.nsw.edu.au/wps/portal/nesa/11-12/Understanding-the-curriculum/resources/hsc-exam-papers']

    def parse(self, response):
        # create list of course items
        global course_items
        course_items = []
        # loops through all courses
        for course in response.css('.res-accordion-grp'):

            # gets course name
            course_name = course.css('.res-heading::text').extract_first().strip()
            # create new course_item
            course_item_current = course_item(
                course = course_name,
                packs = []
            )
            course_items.append( course_item_current )
            # loops through all years in each course
            for year in course.css('.res-accordion-content span a'):
                # extracts link & year for each exam pack
                exam_pack_link = response.urljoin( year.css('::attr(href)').extract_first() )
                exam_pack_year = year.css('::text').re_first(r'[0-9]{4}')

                # create new exam_pack_item
                exam_pack_items = exam_pack_item(
                    year = exam_pack_year,
                    link = exam_pack_link
                )

                # scraper follows this link
                exam_pack_request = scrapy.Request(exam_pack_link,callback=self.parse_docs)
                # add metadata
                exam_pack_request.meta['course'] = course_name
                exam_pack_request.meta['year'] = exam_pack_year
                exam_pack_request.meta['exam_pack_item'] = exam_pack_items
                exam_pack_request.meta['course_item'] = course_item_current
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

        course_item = response.meta['course_item']

        # gets index of corresponding course item
        index = course_items.index(course_item)
        # append current exam pack item
        log.msg( course_items[index], level=log.DEBUG)
        course_items[index]['packs'].append(course_item)
        log.msg( course_items[index]['packs'], level=log.DEBUG)

        #self.group_items(exam_pack_item, course_item)

#    def group_items(self, exam_pack_item, course_item):

    def output(self):
        for item in course_item:
            yield item

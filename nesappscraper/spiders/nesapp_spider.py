import scrapy
from ..items import course_item, exam_pack_item, doc_item

class NesaPPSpider(scrapy.Spider):
    name = "nesapp"
    start_urls = ['http://educationstandards.nsw.edu.au/wps/portal/nesa/11-12/Understanding-the-curriculum/resources/hsc-exam-papers']

    def parse(self, response):
        # loops through all courses
        for course in response.css('.res-accordion-grp'):
            # gets course name
            course_name = course.css('.res-heading::text').extract_first().strip()
            # creates list of exam packs (per year) for each course
            exam_packs = []
            # loops through all years in each course
            for year in course.css('.res-accordion-content span a'):
                # extracts link & year for each exam pack
                exam_pack_link = response.urljoin( year.css('::attr(href)').extract_first() )
                exam_pack_year = year.css('::text').re_first(r'[0-9]{4}')

                # scraper follows this link
                exam_pack_request = scrapy.Request(exam_pack_link,callback=self.parse_docs)
                # add metadata
                exam_pack_request.meta['course'] = course_name
                exam_pack_request.meta['year'] = exam_pack_year
                # add request
                yield exam_pack_request

                # add new exam_pack_item to exam_packs list
                exam_packs.append( exam_pack_item(
                    year = exam_pack_year,
                    link = exam_pack_link,
                    docs = []
                ) )
            # create new course_item
            global course_items
            course_items = course_item(
                course = course_name,
                packs = exam_packs
            )
            # write json
            yield course_items

    def parse_docs(self, response):
        course_items
        for doc in response.css('.right-menu-list a'):
            doc_items = doc_item(
                doc_course = response.meta['course'],
                doc_year = response.meta['year'],
                doc_name = doc.css('::attr(data-file-name)').extract_first()
                    .replace(response.meta['course'],'')
                    .replace(response.meta['year'],'')
                    .strip()
                    .capitalize(),
                doc_link = response.urljoin( doc.css('::attr(href)').extract_first() )
            )
        yield doc_items

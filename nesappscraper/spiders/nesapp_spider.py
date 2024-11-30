import os
import scrapy
import re
from urllib.parse import urljoin
from urllib.parse import parse_qs
from ..items import exam_pack_item, doc_item

def proxy_url(url):
    proxy_api_key = os.environ.get('SCRAPEOPS_API_KEY')
    return f'https://proxy.scrapeops.io/v1/?api_key={proxy_api_key}&url={url}'

class NesaPPSpider(scrapy.Spider):
    name = "nesapp"
    start_urls = [proxy_url('https://educationstandards.nsw.edu.au/wps/portal/nesa/11-12/Understanding-the-curriculum/resources/hsc-exam-papers')]

    def parse(self, response):
        # create list of course names
        global course_names
        course_names = []
        # create list of exam pack lists
        global exam_pack_items
        exam_pack_items = []
        # loops through all courses
        for course in response.css('.res-accordion-grp'):
            # check that the accordion actually has content as a direct descendant
            if (len(course.xpath("./*[contains(@class, 'res-accordion-content')]")) == 0):
                continue
            # gets course name
            course_name = course.css('.res-heading::text').extract_first().strip()
            # adds to list
            course_names.append(course_name)
            # creates empty list in exam_pack_items
            exam_pack_items.append([])
            # loops through all years in each course
            for year in course.css('.res-accordion-content span a'):
                # extracts link & year for each exam pack
                exam_pack_link = urljoin(
                    'https://educationstandards.nsw.edu.au',
                    year.css('::attr(href)').extract_first()
                )
                exam_pack_year = year.css('::text').re_first(r'[0-9]{4}')

                if exam_pack_year < '2024':
                    continue

                # create new exam_pack_item
                exam_pack_item_current = exam_pack_item(
                    course = course_name,
                    year = exam_pack_year,
                    link = exam_pack_link
                )

                # scraper follows this link to each exam pack
                exam_pack_request = scrapy.Request(
                    proxy_url(exam_pack_link),
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
            # append do doc_items list
            doc_items.append( dict( doc_item(
                doc_link = strip_document_url(urljoin(
                    'https://educationstandards.nsw.edu.au',
                    doc.css('::attr(href)').extract_first()
                )),
                doc_name = format_doc_name(
                    doc.css('::attr(data-file-name)').extract_first(),
                    response.meta['course'],
                    response.meta['year'] )
            ) ) )
        # get unfinished exam_pack_item from response meta
        exam_pack_item = response.meta['exam_pack_item']

        # use true redirected url for exam pack
        exam_pack_item['link'] = sanitise_exam_pack_url(response.url)

        # add doc_items array to exam_pack_item
        exam_pack_item['docs'] = doc_items
        # Yields item
        # Note this does not yield anything if the pipeline is activated in
        # settings.
        yield dict(exam_pack_item)

# Strips unnecessary data from an exam pack url
def sanitise_exam_pack_url(url):
    sanitised = parse_qs(url)['url'][0]
    # nothing after '/!ut/' is needed
    sanitised = sanitised.split('/!ut/')[0]
    return sanitised

# Strips unnecessary data from a document url
def strip_document_url(url):
    # CACHEID isn't needed
    formatted = url.split('&CACHEID=')[0]
    # check if missing .pdf extension
    missing_ext = re.search('[0-9]\?MOD', formatted)
    if missing_ext:
        formatted = formatted.replace('?MOD', '.pdf?MOD')
    # Output
    return formatted

# Formats doc_name
def format_doc_name(name, course, year):
    formatted = name.lower()
    formatted = formatted.replace(course.lower(),'')
    formatted = formatted.replace(year,'')
    formatted = formatted.lstrip(' - ')
    formatted = formatted.replace('classical','')
    formatted = formatted.replace('modern','')
    formatted = formatted.replace('heritage','')
    formatted = formatted.replace('hebrew','')
    formatted = formatted.replace('continuers','')
    formatted = formatted.replace('chinese','')
    formatted = formatted.replace('(mandarin)','')
    formatted = formatted.replace('mandarin','')
    formatted = formatted.replace('background speakers','')
    formatted = formatted.replace('indonesian','')
    formatted = formatted.replace('and literature','')
    formatted = formatted.replace('japanese','')
    formatted = formatted.replace('korean','')
    formatted = formatted.replace('greek','')
    formatted = formatted.replace('extension','')
    formatted = formatted.replace('beginners','')
    formatted = formatted.replace('ancient history','')
    formatted = formatted.replace('english standard & advanced','')
    formatted = formatted.replace('comparative literature','')
    formatted = formatted.replace('information technology','')
    formatted = formatted.replace('pdhpe','')
    formatted = formatted.replace('physical development, health and physical education','')
    formatted = formatted.replace('aboriginal studies','')
    formatted = formatted.strip()
    formatted = formatted.title()
    formatted = formatted.replace('Hsc','HSC')
    formatted = formatted.replace('Ii','II')
    formatted = formatted.replace('Iii','III')
    # Fix for SOR I & II papers
    if course == 'Studies of Religion':
        if ( formatted.startswith("I") or formatted.startswith("1") or
            formatted.startswith("2") ):
            formatted = 'SOR ' + formatted
    # Output
    return formatted

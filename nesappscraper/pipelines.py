# -*- coding: utf-8 -*-

# You must disable this pipeline in settings.py to run on Scrapy Cloud

from .items import course_item
from scrapy.exceptions import DropItem
import datetime
import logging
import json

class NesappscraperPipeline(object):

    # called when the spider opens
    def open_spider(self, spider):
        # create list of exam packs
        self.exam_pack_list = []
        # create json file
        self.file = open('data.json', 'w')
        # creates meta json file
        self.meta = open('meta.json', 'w')
        # creates counter
        self.count = 0
        # gets current time
        self.start_time = datetime.datetime.today()

    # called when each exam_pack_item is yielded in parse_docs
    def process_item(self, item, spider):
        # increment counter
        self.count += 1
        # flag if exam pack was grouped with other exam packs of the same course
        placed = False
        # loops through each element in the list to see if an exam pack has
        # already been stored for this course
        for i in range(len(self.exam_pack_list)):
            course_name = self.exam_pack_list[i][0]['course']
            if item['course'] == course_name:
                # group this exam pack with other exam packs of the same course
                # already in the list
                self.exam_pack_list[i].append(item)
                placed = True
        # If this is the first exam pack of the course, append it to the list
        if placed == False:
            self.exam_pack_list.append([item])
        # Raises DropItem exception so it doesn't output anything
        raise DropItem('Using custom output for item #' + str(self.count))

    # called when the spider closes
    def close_spider(self, spider):
        # Add open bracket for JSON file
        self.file.write('[')
        # Sorts courses by course
        self.exam_pack_list.sort(key=lambda k: k[0]['course'])
        # Loops through each course in exam_pack_list
        for i in range(len(self.exam_pack_list)):
            # Sorts exam_packs by year
            self.exam_pack_list[i].sort(key=lambda k: k['year'], reverse=True)
            # Makes a course_item for each course and formats properly
            line = dict(course_item(
                course_name = self.exam_pack_list[i][0]['course'],
                packs = self.exam_pack_list[i]
            ))
            # Writes course_item to the JSON file
            self.file.write(json.dumps(line))
            # If not the last line, add a comma
            if i != len(self.exam_pack_list) - 1:
                self.file.write(',\n')
        # Add close bracket
        self.file.write(']')
        # Close JSON file
        self.file.close()

        # Get end time
        self.end_time = datetime.datetime.today()
        # Get runtime
        self.runtime = self.end_time - self.start_time

        # Writes to meta JSON file
        self.meta.write(
            '{ ' +
            '"timestamp": "' + str( self.end_time.isoformat() ) + '", ' +
            '"runtime": "' + str( self.runtime.total_seconds() ) + '", ' +
            '"exam_pack_items": ' + str( self.count ) +
            ' }'
        )
        self.meta.close()

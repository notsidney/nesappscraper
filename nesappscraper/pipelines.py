# -*- coding: utf-8 -*-

# You must disable this pipeline in settings.py to run on Scrapy Cloud

from items import course_item
import datetime
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
        # If this is the first exam pack of the course, append it to the lsit
        if placed == False:
            self.exam_pack_list.append([item])
        # Returns nothing - usually this would return an item
        # This prevents it from working on scrapy cloud
        return None

    # called when the spider closes
    def close_spider(self, spider):
        # Add open bracket for JSON file
        self.file.write('[')
        # Loops through each course in exam_pack_list
        for i in range(len(self.exam_pack_list)):
            # Makes a course_item for each course and formats properly
            line = str(course_item(
                course_name = self.exam_pack_list[i][0]['course'],
                packs = self.exam_pack_list[i]
            )).replace('u\'', '\'').replace('\'','"') + '\n,'
            # Writes coruse_item to the JSON file
            self.file.write(line)
        # Deletes , for last course_item for valid JSON
        self.file.seek(-1,2)
        # Add close bracket
        self.file.write(']')
        # Close JSON file
        self.file.close()

        # Get end time
        self.end_time = datetime.datetime.today()
        # Get runtime
        self.runtime = self.end_time - self.start_time

        # Writes to meta json file
        self.meta.write(
            '{ ' + 
            '"timestamp": "' + str( self.end_time.isoformat() ) + '", ' +
            '"runtime": "' + str( self.runtime.total_seconds() ) + '", ' +
            '"exam_pack_items": ' + str( self.count ) +
            ' }'
        )
        self.meta.close()

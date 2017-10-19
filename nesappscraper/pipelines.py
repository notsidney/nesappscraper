# -*- coding: utf-8 -*-

# You must disable this pipeline in settings.py to run on Scrapy Cloud

from items import course_item
import json

class NesappscraperPipeline(object):

    # called when the spider opens
    def open_spider(self, spider):
        # create list of exam packs
        global exam_pack_list
        exam_pack_list = []
        # create json file
        self.file = open('data.json', 'w')

    # called when each exam_pack_item is yielded in parse_docs
    def process_item(self, item, spider):
        # flag if exam pack was grouped with other exam packs of the same course
        placed = False
        # loops through each element in the list to see if an exam pack has
        # already been stored for this course
        for i in range(len(exam_pack_list)):
            course_name = exam_pack_list[i][0]['course']
            if item['course'] == course_name:
                # group this exam pack with other exam packs of the same course
                # already in the list
                exam_pack_list[i].append(item)
                placed = True
        # If this is the first exam pack of the course, append it to the lsit
        if placed == False:
            exam_pack_list.append([item])
        # Returns nothing - usually this would return an item
        return None

    # called when the spider closes
    def close_spider(self, spider):
        # Add open bracket for JSON file
        self.file.write('[')
        # Loops through each course in exam_pack_list
        for i in range(len(exam_pack_list)):
            # Makes a course_item for each course and formats properly
            line = str(course_item(
                course_name = exam_pack_list[i][0]['course'],
                packs = exam_pack_list[i]
            )).replace('u\'', '\'').replace('\'','"') + '\n,'
            # Writes coruse_item to the JSON file
            self.file.write(line)
        # Deletes , for last course_item for valid JSON
        self.file.seek(-1,2)
        # Add close bracket
        self.file.write(']')
        # Close JSON file
        self.file.close()

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from items import course_item
import json

class NesappscraperPipeline(object):

    def open_spider(self, spider):
        # create list of exam packs
        global exam_pack_list
        exam_pack_list = []

        self.file = open('data.json', 'w')

    def process_item(self, item, spider):
        placed = False

        for i in range(len(exam_pack_list)):
            course_name = exam_pack_list[i][0]['course']
            if item['course'] == course_name:
                exam_pack_list[i].append(item)
                placed = True

        if placed == False:
            exam_pack_list.append([item])

        # return {'item':'test'}
        return None

    def close_spider(self, spider):
        self.file.write('[')

        for i in range(len(exam_pack_list)):
            line = str(course_item(
                course_name = exam_pack_list[i][0]['course'],
                packs = exam_pack_list[i]
            )).replace('u\'', '\'').replace('\'','"') + '\n,'
            self.file.write(line)

        self.file.seek(-1,2)
        self.file.write(']')
        self.file.close()

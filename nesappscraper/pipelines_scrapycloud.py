# -*- coding: utf-8 -*-

# You must disable this pipeline in settings.py to run on Scrapy Cloud

from .items import course_item
from scrapy.exceptions import DropItem
import datetime
import json

import os
import threading

from scrapinghub.hubstorage.serialization import jsondefault
from scrapinghub.hubstorage.utils import millitime

class NesappscraperPipelineScrapyCloud(object):
    # from https://github.com/scrapinghub/scrapinghub-entrypoint-scrapy/blob/master/sh_scrapy/writer.py
    # and https://doc.scrapinghub.com/scrapy-cloud-write-entrypoint.html
    def __init__(self):
        self.path = os.environ['SHUB_FIFO_PATH']
        self._lock = threading.Lock()
        self._pipe = None
        # create list of exam packs
        self.exam_pack_list = []
        # creates counter
        self.count = 0

    # called when the spider opens
    def open_spider(self, spider):
        # open pipe
        with self._lock:
            self._pipe = open(self.path, 'w')

    def _write(self, command, payload):
        # binary command
        command = command.encode('utf-8')
        # binary payload
        encoded_payload = json.dumps(
            payload,
            separators=(',', ':'),
            default=jsondefault
        ).encode('utf-8')
        # write needs to be locked because write can be called from multiple threads
        with self._lock:
            self._pipe.write(command)
            self._pipe.write(b' ')
            self._pipe.write(encoded_payload)
            self._pipe.write(b'\n')
            self._pipe.flush()

    def write_item(self, item):
        self._write('ITM', item)

    def write_log(self, level, message):
        log = {
            'time': millitime(),
            'level': level,
            'message': message
        }
        self._write('LOG', log)

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
        # Raises DropItem exception so it doesn't output anything
        raise DropItem('Using custom output for item #' + str(self.count))

    # called when the spider closes
    def close_spider(self, spider):
        # Sorts courses by course
        self.exam_pack_list.sort(key=lambda k: k[0]['course'])
        # Loops through each course in exam_pack_list
        for i in range(len(self.exam_pack_list)):
            # Sorts exam_packs by year
            self.exam_pack_list[i].sort(key=lambda k: k['year'], reverse=True)
            # Makes a course_item for each course and formats properly
            line = dict( course_item(
                course_name = self.exam_pack_list[i][0]['course'],
                packs = self.exam_pack_list[i]
            ) )
            # Writes coruse_item 
            self.write_item(line)

        self._pipe.close()

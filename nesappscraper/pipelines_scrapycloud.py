# -*- coding: utf-8 -*-

# You must disable this pipeline in settings.py to run on Scrapy Cloud

from items import course_item
import datetime
import json

import os
import threading

from scrapinghub.hubstorage.serialization import jsondefault
from scrapinghub.hubstorage.utils import millitime

class NesappscraperPipelineScrapyCloud(object):
    # from https://github.com/scrapinghub/scrapinghub-entrypoint-scrapy/blob/master/sh_scrapy/writer.py
    def __init__(self):
        self.path = ''
        self._lock = threading.Lock()
        self._pipe = None
        if not self.path:
            self._write = _not_configured
            self.open = _not_configured
            self.close = _not_configured

    # called when the spider opens
    def open_spider(self, spider):
        # open pipe
        with self._lock:
            self._pipe = open(self.path, 'wb')
        # create list of exam packs
        self.exam_pack_list = []
        # creates counter
        self.count = 0
        # gets current time
        self.start_time = datetime.datetime.today()

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

    def write_stats(self, stats):
        self._write('STA', {'time': millitime(), 'stats': stats})

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
        # Loops through each course in exam_pack_list
        for i in range(len(self.exam_pack_list)):
            # Makes a course_item for each course and formats properly
            line = course_item(
                course_name = self.exam_pack_list[i][0]['course'],
                packs = self.exam_pack_list[i]
            )
            # Writes coruse_item to the JSON file
            self.write_item(line)

        # Get end time
        self.end_time = datetime.datetime.today()
        # Get runtime
        self.runtime = self.end_time - self.start_time

        # Writes to meta json file
        self.write_stats(
            'STA { "stats: {' + 
            '"timestamp": "' + str( self.end_time.isoformat() ) + '", ' +
            '"runtime": "' + str( self.runtime.total_seconds() ) + '", ' +
            '"exam_pack_items": ' + str( self.count ) +
            ' }}'
        )

        # finished!
        self._write('FIN', {'outcome': 'finished'})
        self._pipe.flush()
        self._pipe.close()

#!/bin/bash
# scrapy crawl nesapp
cat meta.json
git add data.json
git add meta.json
git commit -m "Update data: $(date +%D) $(date +%T)"
git log

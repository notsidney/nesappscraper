@echo off
title NESA PP Scraper - Started %time%
scrapy crawl nesapp
git add data.json

git add meta.json

git commit -m "Update data: %date% %time%"

git push
pause
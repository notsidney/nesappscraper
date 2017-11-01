@echo off
title NESA PP Scraper - Started %time%
scrapy crawl nesapp
type meta.json
git add data.json
git add meta.json
git commit -S -m "Update data: %date% %time%"
git push
pause

@echo off
title nesappscraper
scrapy crawl nesapp
git add data.json
git add meta.json
git commit -m "Update data: %date% %time%"
git push
pause
#!/bin/sh
# Set title
echo "\033]0;NESA Past Papers Scraper – Started $(date +"%T")\007"
# Colours
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'
# Run crawler
scrapy crawl nesapp
# Print meta.json
echo "${YELLOW}$(cat meta.json)"
# Get timestamp at end of scraping
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
# Push to git
echo "\nPush to nesappscraper:"
git add data.json
git add meta.json
git commit -S -m "Update data: ${TIMESTAMP}"
git push
# Copy to hscpastpapers git
echo "\nPush to hscpastpapers:"
cp data.json ../hscpastpapers/data.json
cp meta.json ../hscpastpapers/meta.json
# Push to hscpastpapers git
cd ../hscpastpapers
git add data.json
git add meta.json
git commit -S -m "Update data: ${TIMESTAMP}"
git push
echo "\n${GREEN}Data updated: ${TIMESTAMP}"
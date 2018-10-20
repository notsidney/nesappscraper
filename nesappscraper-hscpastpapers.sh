#!/bin/sh
# Set title
echo "\033]0;NESA Past Papers Scraper – Started $(date +"%T")\007"
# Colours
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'
# Run crawler
pipenv run scrapy crawl nesapp
# Print meta.json
echo "${YELLOW}$(cat meta.json)${NC}"
# Get timestamp at end of scraping
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
# Push to git
echo "\n${YELLOW}Push to nesappscraper:${NC}"
git add data.json
git add meta.json
git commit -S -m "Update data: ${TIMESTAMP}"
git push
# Copy to hscpastpapers git
echo "\n${YELLOW}Push to hscpastpapers:${NC}"
cp data.json ../hscpastpapers/data/data.json
cp meta.json ../hscpastpapers/data/meta.json
# Push to hscpastpapers git
cd ../hscpastpapers
git add data/data.json
git add data/meta.json
git commit -S -m "Update data: ${TIMESTAMP}"
git push
echo "\n${GREEN}Data updated: ${TIMESTAMP}${NC}"

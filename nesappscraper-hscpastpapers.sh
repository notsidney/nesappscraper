#!/bin/sh
# Set title
echo "\033]0;NESA Past Papers Scraper – Started $(date +"%T")\007"
# Colours
YELLOW='\033[1;33m'
NC='\033[0m'
# Run crawler
echo scrapy crawl nesapp
# Print meta.json
echo "\n${YELLOW}$(cat meta.json)\n${NC}"
# Get timestamp at end of scraping
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
# Push to git
git add data.json
git add meta.json
git commit -S -m "Update data: ${TIMESTAMP}"
git push
# Copy to hscpastpapers git
cp data.json ../hscpastpapers/data.json
cp meta.json ../hscpastpapers/meta.json
# Push to hscpastpapers git
cd ../hscpastpapers
git add data.json
git add meta.json
git commit -S -m "Update data: ${TIMESTAMP}"
git push
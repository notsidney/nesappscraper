@echo off
title nesappscraper
echo "Update" %date% %time%
git add nesappscraper.bat
git commit -m "Update data"
git push
pause
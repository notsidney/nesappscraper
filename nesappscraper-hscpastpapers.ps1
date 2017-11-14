# Change title
$host.ui.RawUI.WindowTitle = "NESA PP Scraper - Started $(Get-Date -UFormat %T)"
# Run crawler
scrapy crawl nesapp
# Print meta.json
write-host (Get-Content meta.json) -ForegroundColor Yellow
# Get time
$timestamp = Get-Date -Format g
# Push to git
git add data.json
git add meta.json
git commit -S -m "Update data: $timestamp"
git push
# Copy to hscpapers git
Copy-Item -Path data.json -Destination ..\hscpapers\data\data.json
Copy-Item -Path meta.json -Destination ..\hscpapers\data\meta.json
# Push to hscpapers git
cd ..\hscpapers
git add data/data.json
git add data/meta.json
git commit -S -m "Update data: $timestamp"
git push
# Prompt
Read-Host -Prompt "Press Enter to exit"
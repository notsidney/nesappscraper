# Change title
$host.ui.RawUI.WindowTitle = "NESA PP Scraper - Started $(Get-Date -UFormat %T)"
# Run crawler
scrapy crawl nesapp
# Print meta.json
write-host (Get-Content meta.json) -ForegroundColor Yellow
# Push to git
git add data.json
git add meta.json
git commit -S -m "Update data: $(Get-Date -Format g)"
git push
# Prompt
Read-Host -Prompt "Press Enter to exit"
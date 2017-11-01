# Create timer for window title
$count = 0
$timer = New-Object System.Timers.Timer
$timer.Interval = 1000
# Write runtime to window title
Register-ObjectEvent -InputObject $timer -EventName Elapsed -Action {
  $count++
  $runtime = [timespan]::fromseconds($count).ToString("mm\:ss")
  $host.ui.RawUI.WindowTitle = "NESA PP Scraper - Runtime $runtime"
}
# Run crawler
scrapy crawl nesapp
# Stop timer
$timer.Stop()
# Print meta.json
write-host (Get-Content meta.json) -ForegroundColor Yellow
# Push to git
git add data.json
git add meta.json
git commit -S -m "Update data: %date% %time%"
git push

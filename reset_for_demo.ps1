# Reset helper for Budget Buddy demos

Write-Host "Budget Buddy demo reset guidance" -ForegroundColor Cyan
Write-Host ""
Write-Host "Restore the current branch after a demo with:" -ForegroundColor Yellow
Write-Host "  git restore ." -ForegroundColor White
Write-Host ""
Write-Host "Then verify the baseline:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\python.exe main.py" -ForegroundColor White
Write-Host "  .\.venv\Scripts\python.exe -m pytest" -ForegroundColor White
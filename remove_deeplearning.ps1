Set-Location "C:\D_Drive\lowfieldPipeline"

Write-Host "Step 1: Removing deeplearning/ folder from repo..." -ForegroundColor Cyan
git rm -rf "deeplearning/" 2>&1

Write-Host "Step 2: Removing deeplearning section from README.md..." -ForegroundColor Cyan

# Read current README
$readme = Get-Content "README.md" -Raw

# Remove the deeplearning block (the 7 lines under "Deep Learning Baseline")
$readme = $readme -replace `
    '\|\r?\n\|-- Deep Learning Baseline\r?\n\|   \|-- deeplearning/.*?\r?\n(\|   \|--.*?\r?\n)*', ''

# Also remove any leftover single-line reference to deeplearning
$readme = $readme -replace '(?m)^\|.*deeplearning.*\r?\n', ''

# Clean up any double blank lines that result
$readme = $readme -replace '(\r?\n){3,}', "`r`n`r`n"

Set-Content "README.md" -Value $readme -Encoding UTF8 -NoNewline
Write-Host "  README.md updated." -ForegroundColor Green

# Stage and commit both changes together
git add "README.md"
git commit -m "cleanup: remove deeplearning folder and its README reference entirely"

# Push
git push origin main

Write-Host "`nDone! deeplearning/ removed from repo and README." -ForegroundColor Magenta

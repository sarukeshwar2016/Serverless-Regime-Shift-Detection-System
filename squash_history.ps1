<#
.SYNOPSIS
    Squashes all April-3 commits into exactly 15 logical commits, then force-pushes.
    Run from PowerShell:
        powershell -ExecutionPolicy Bypass -File "C:\D_Drive\regime-platform\squash_history.ps1"
#>

Set-Location "C:\D_Drive\lowfieldPipeline"
$ErrorActionPreference = "Continue"

# ─── 1. Find the last commit that existed BEFORE April 3 ───────────────────────
Write-Host "`nFinding pre-April-3 base commit..." -ForegroundColor Cyan
$base = git log --before="2026-04-02T23:59:59" --format="%H" -1

if (-not $base) {
    # Fallback: use the very first commit ever
    $base = git log --format="%H" | Select-Object -Last 1
}

$baseMsg = git log --format="%s" -1 $base
$aprilCount = (git log --after="2026-04-02T23:59:59" --oneline | Measure-Object -Line).Lines

Write-Host "  Base commit : $base"
Write-Host "  Base message: $baseMsg"
Write-Host "  Commits to squash: $aprilCount"

# ─── 2. Safety backup branch ───────────────────────────────────────────────────
$backupBranch = "backup-$(Get-Date -Format 'yyyyMMdd-HHmm')"
git branch $backupBranch HEAD 2>&1 | Out-Null
Write-Host "  Backup saved to branch: $backupBranch" -ForegroundColor Yellow

# ─── 3. Soft-reset to base: stages all April-3 diffs ──────────────────────────
Write-Host "`nResetting to base commit (soft)..." -ForegroundColor Cyan
git reset --soft $base

# Unstage everything → changes go back to working tree / unstaged
git restore --staged . 2>&1 | Out-Null

Write-Host "  All changes unstaged. Making 15 logical commits..." -ForegroundColor Cyan

# ─── Helper ────────────────────────────────────────────────────────────────────
$n = 0
function Do-GroupCommit {
    param([string[]]$Paths, [string]$Message)
    foreach ($p in $Paths) {
        # handles new files, modifications, and deletions
        git add -A -- $p 2>&1 | Out-Null
    }
    $staged = git diff --cached --name-only
    if ($staged) {
        git commit -m $Message 2>&1 | Out-Null
        $script:n++
        Write-Host ("  [$($script:n.ToString('00'))] $Message") -ForegroundColor Green
    } else {
        Write-Host ("  [--] Nothing staged for: $Message") -ForegroundColor DarkGray
    }
}

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 1 – Remove legacy batch pipeline scripts
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "enhance_batch_61_112.py",
        "enhance_new_batch_50.py",
        "run_batch_pipeline.py",
        "run_batch_pipeline_no_bm3d.py"
    ) `
    -Message "cleanup: remove legacy batch pipeline scripts superseded by corrected runner"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 2 – Remove old simulation and debugging utilities
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "simulate_new_nifti_batch.py",
        "inspect_ppt.py",
        "filter_report.py",
        "compare_mri_metadata.py"
    ) `
    -Message "cleanup: remove outdated simulation scripts and one-off debugging utilities"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 3 – Remove redundant document generation scripts
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "generate_advanced_plots.py",
        "gen_methodology_diagrams.py",
        "generate_arch_doc.py",
        "generate_project_docs.py",
        "rebuild_func_doc.py",
        "rebuild_sprint_retro.py"
    ) `
    -Message "cleanup: remove doc-generation scripts all documents already produced"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 4 – Remove old report and scratch text files
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "report.txt",
        "pipeline_stage_report.txt",
        "ppt_structure.txt",
        "func_doc_template.txt"
    ) `
    -Message "cleanup: remove outdated report files and scratch planning artifacts"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 5 – Remove old batch result folders and duplicate docs
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "batch_enhanced",
        "batch_enhanced_stable",
        "batch_enhanced_no_bm3d",
        "batch_enhanced_final",
        "Functional Document (1).docx",
        "Functional Test case Template (1).xlsx",
        "Sprint Retrospective (1).xlsx",
        "deeplearning"
    ) `
    -Message "cleanup: remove old batch result folders, duplicate root documents and deeplearning folder"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 6 – README
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @("README.md") `
    -Message "docs: add README with pipeline overview, project structure and results summary"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 7 – RESULTS + CHANGELOG
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @("RESULTS.md", "CHANGELOG.md") `
    -Message "docs: add RESULTS.md with evaluation metrics and CHANGELOG.md with version history"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 8 – Build and CI files
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @("requirements.txt", "setup.py", "LICENSE", ".gitignore") `
    -Message "build: add requirements.txt, setup.py, LICENSE and updated gitignore"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 9 – config.py
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @("config.py") `
    -Message "refactor: add config.py to centralize all pipeline parameters and data paths"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 10 – utils.py
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @("utils.py") `
    -Message "refactor: add utils.py with shared SNR, PSNR, SSIM and image utility functions"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 11 – pipeline/ package
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @("pipeline") `
    -Message "refactor: add pipeline/ importable package with config and utils modules"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 12 – Docstrings: simulation and enhancement scripts
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "dicom_to_lf_sim.py",
        "enhanced_batch_9_100.py",
        "linear_pipeline_clean.py",
        "simulate_batch_9_100.py"
    ) `
    -Message "docs: add module docstrings to simulation and enhancement pipeline scripts"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 13 – Docstrings: batch runners and analysis scripts
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "run_batch_fully_corrected.py",
        "run_batch_spine_stable.py",
        "generate_plots.py",
        "generate_report2.py",
        "pipeline_stage_report.py",
        "research_pipeline_updated.py"
    ) `
    -Message "docs: add module docstrings to batch runners and analysis scripts"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 14 – New utility scripts
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @(
        "validate_outputs.py",
        "check_snr_constraints.py",
        "summarize_results.py",
        "export_csv.py",
        "batch_stats.py"
    ) `
    -Message "feat: add output validation, SNR checking, results summary and CSV export scripts"

# ══════════════════════════════════════════════════════════════════════════════
#  COMMIT 15 – Unit tests
# ══════════════════════════════════════════════════════════════════════════════
Do-GroupCommit `
    -Paths @("tests") `
    -Message "test: add unit tests for compute_snr, PSNR, SSIM and histogram overlap"

# ─── Final status ──────────────────────────────────────────────────────────────
Write-Host "`nTotal commits made: $n" -ForegroundColor Cyan
Write-Host "Current log (last 20):" -ForegroundColor Cyan
git log --oneline -20

# ─── Force push ────────────────────────────────────────────────────────────────
Write-Host "`nForce-pushing to origin/main..." -ForegroundColor Cyan
git push --force-with-lease origin main

Write-Host "`n=============================================" -ForegroundColor Magenta
Write-Host "  Done! $n commits on April 3 (was 87)." -ForegroundColor Magenta
Write-Host "  GitHub graph will update in a few minutes." -ForegroundColor Magenta
Write-Host "  Backup branch: $backupBranch" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Magenta

# verify.ps1 — Check that a Spendly route returns HTTP 200
#
# Usage:
#   .\verify.ps1                        # checks /
#   .\verify.ps1 -Route "/login"
#   .\verify.ps1 -Route "/terms" -Host "http://127.0.0.1:5001"
#
# Run from the project root:
#   .\.claude\skills\spendly-style-guide\scripts\verify.ps1 -Route "/register"

param(
    [string]$Route = "/",
    [string]$Host  = "http://127.0.0.1:5001"
)

$url = "$Host$Route"

try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -ErrorAction Stop
    $status   = $response.StatusCode

    if ($status -eq 200) {
        Write-Host "  OK   $url  →  $status" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "  WARN $url  →  $status (expected 200)" -ForegroundColor Yellow
        exit 1
    }
} catch {
    $status = $_.Exception.Response.StatusCode.value__
    if ($status) {
        Write-Host "  FAIL $url  →  $status" -ForegroundColor Red
    } else {
        Write-Host "  FAIL $url  →  no response (is Flask running?)" -ForegroundColor Red
        Write-Host "       Start the server: python app.py" -ForegroundColor DarkGray
    }
    exit 1
}
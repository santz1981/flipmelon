# Download the official scrcpy Windows release required by Flipmelon.
# No browser automation, no bypassing OS policies. Fails closed on checksum mismatch.
$ErrorActionPreference = 'Stop'
$version = 'v5.0.1'
$filename = "scrcpy-win64-$version.zip"
$url = "https://github.com/Genymobile/scrcpy/releases/download/$version/$filename"
# Published by Genymobile at https://github.com/Genymobile/scrcpy/blob/master/doc/windows.md
$expectedSha256 = 'b12a2c4ee8be317422451fc7dcf8ee20a71b5ea7ef9ad73ddd825a25316227a5'
$repo = Split-Path -Parent $PSScriptRoot
$vendor = Join-Path $repo 'vendor\windows'
$temp = Join-Path $env:TEMP ('flipmelon-scrcpy-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $temp | Out-Null
try {
    $archive = Join-Path $temp $filename
    Write-Host "Downloading official scrcpy $version ..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri $url -OutFile $archive -UseBasicParsing
    $actual = (Get-FileHash -Algorithm SHA256 -Path $archive).Hash.ToLowerInvariant()
    if ($actual -ne $expectedSha256) {
        throw "SHA-256 verification failed. Expected $expectedSha256 but got $actual. Do NOT use this archive."
    }
    $expanded = Join-Path $temp 'unzipped'
    Expand-Archive -Path $archive -DestinationPath $expanded -Force
    $from = Join-Path $expanded "scrcpy-win64-$version"
    if (!(Test-Path (Join-Path $from 'scrcpy.exe'))) { throw 'The verified scrcpy archive has an unexpected directory layout.' }
    New-Item -ItemType Directory -Force -Path $vendor | Out-Null
    Copy-Item -Path (Join-Path $from '*') -Destination $vendor -Recurse -Force
    foreach ($required in @('adb.exe','scrcpy.exe','scrcpy-server','LICENSE.txt')) {
        if (!(Test-Path (Join-Path $vendor $required))) { throw "Missing $required after extraction." }
    }
    Write-Host "Success: installed checksum-verified scrcpy runtime into vendor\windows" -ForegroundColor Green
}
finally {
    if (Test-Path $temp) { Remove-Item -Path $temp -Recurse -Force -ErrorAction SilentlyContinue }
}

$files = Get-ChildItem 'E:\Downloads\vehicle\labels\valid\'
$files = Get-ChildItem 'E:\Downloads\vehicle\labels\train\'
foreach ($f in $files){
    $outfile ='E:\Downloads\vehicle_out\' + $f.BaseName + '.txt'
    (Get-Content $f.FullName) | Where-Object { ($_ -match '^2 ' -or $_ -match '^3 '-or $_ -match '^6 ') } | % {$_ -replace '^6 ','1 ' -replace '^2 ','1 ' -replace '^3 ','0 '} | Set-Content $outfile
}

$files = Get-ChildItem 'E:\Downloads\vehicle\labels\valid\'
# $files = Get-ChildItem 'E:\Downloads\vehicle\labels\train\'
foreach ($f in $files){
    $outfile ='E:\Downloads\vehicle_out\' + $f.BaseName + '.txt'
    (Get-Content $f.FullName) |
    Where-Object {(($_.split(" ")[0] -eq 0) -and ($_.split(" ")[3] -ge 0.20) -and ($_.split(" ")[4] -ge 0.20)) -or (($_.split(" ")[0] -eq 1) -and ($_.split(" ")[3] -ge 0.30) -and ($_.split(" ")[4] -ge 0.30))} |
    Set-Content $outfile
}

$files = Get-ChildItem 'E:\Downloads\vehicle\images\valid\'
# $files = Get-ChildItem 'E:\Downloads\vehicle\images\train\'
foreach ($f in $files){
    $outfile ='E:\Downloads\vehicle_out\' + $f.BaseName + '.txt'
    $labelfile = 'E:\Downloads\vehicle\labels\valid\' + $f.BaseName + '.txt'
    # $labelfile = 'E:\Downloads\vehicle\labels\train\' + $f.BaseName + '.txt'
    # echo $outfile
    # echo $labelfile
    If (Test-Path -Path   $labelfile ) {
        Copy-Item -Path  $labelfile -Destination $outfile
    }
    Else {
        Remove-Item $f.FullName
    }
    # echo
}
$files = Get-ChildItem 'E:\Downloads\vehicle\images\valid\'
# $files = Get-ChildItem 'E:\Downloads\vehicle\images\train\'
$outfile = 'E:\Downloads\vehicle_out\valid.txt'
# $outfile = 'E:\Downloads\vehicle_out\train.txt'
foreach ($f in $files){
    $outname ='/content/vehicle/images/valid/' + $f.BaseName + '.jpg'
    # $outname ='/content/vehicle/images/train/' + $f.BaseName + '.jpg'
    Add-Content -Path $outfile -Value $outname
}
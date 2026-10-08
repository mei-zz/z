$ErrorActionPreference = 'Continue'
$base = 'https://raw.githubusercontent.com/kimiyoung/planetoid/master/data'
$target = 'E:\Z\planetoid_raw'
New-Item -ItemType Directory -Force -Path $target | Out-Null
foreach ($dataset in @('cora','pubmed')) {
  foreach ($suffix in @('x','tx','allx','y','ty','ally','graph','test.index')) {
    $filename = "ind.$dataset.$suffix"
    $outfile = Join-Path $target $filename
    try {
      Invoke-WebRequest -Uri "$base/$filename" -OutFile $outfile -UseBasicParsing -TimeoutSec 120 -ErrorAction Stop
      Write-Output "$filename`t$((Get-Item -LiteralPath $outfile).Length)"
    } catch {
      Write-Output "$filename`tERROR $($_.Exception.Message)"
    }
  }
}

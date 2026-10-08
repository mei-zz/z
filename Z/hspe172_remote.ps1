$script:V172Repo='E:\我的资料库\Documents\Downloads\DCDLP-main'
$script:V172Credentials=@{}
Get-Content (Join-Path $script:V172Repo '.env') | ForEach-Object {if($_ -match '^([^#=]+)=(.*)$'){$script:V172Credentials[$matches[1]]=$matches[2].Trim().Trim('"')}}
$env:DCDLP_SSH_PASSWORD=$script:V172Credentials['psw']
$env:SSH_ASKPASS='E:\Z\.codex_ssh_askpass.exe'
$env:SSH_ASKPASS_REQUIRE='force'
$env:DISPLAY='codex'
$script:V172Target=$script:V172Credentials['user']+'@'+$script:V172Credentials['IP']
$script:V172Opts=@('-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','ConnectTimeout=15','-o','StrictHostKeyChecking=yes')
function Invoke-V172Ssh([string]$Command) { ssh @script:V172Opts $script:V172Target $Command; if($LASTEXITCODE -ne 0){throw "Remote command exit $LASTEXITCODE"} }
function Send-V172File([string]$Source,[string]$Destination) { scp @script:V172Opts $Source "${script:V172Target}:$Destination"; if($LASTEXITCODE -ne 0){throw 'Upload failed'} }
function Get-V172File([string]$Source,[string]$Destination) { scp @script:V172Opts "${script:V172Target}:$Source" $Destination; if($LASTEXITCODE -ne 0){throw 'Download failed'} }

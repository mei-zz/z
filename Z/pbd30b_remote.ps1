$script:PbdRepo='E:\我的资料库\Documents\Downloads\DCDLP-main'
$script:PbdConfig=@{}
Get-Content -LiteralPath 'E:\Z\.env' | ForEach-Object {if($_ -match '^([^#=]+)=(.*)$'){$script:PbdConfig[$matches[1]]=$matches[2].Trim().Trim('"')}}
if($script:PbdConfig['IP'] -ne '10.16.15.66'){throw 'V30B server identity mismatch'}
$env:DCDLP_SSH_PASSWORD=$script:PbdConfig['psw']
$env:SSH_ASKPASS='E:\Z\.codex_ssh_askpass.exe'
$env:SSH_ASKPASS_REQUIRE='force'
$env:DISPLAY='codex'
$script:PbdTarget=$script:PbdConfig['user']+'@'+$script:PbdConfig['IP']
$script:PbdOpts=@('-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','ConnectTimeout=15','-o','StrictHostKeyChecking=yes')
function Invoke-PbdSsh([string]$Command) {ssh @script:PbdOpts $script:PbdTarget $Command; if($LASTEXITCODE -ne 0){throw "Remote command exit $LASTEXITCODE"}}
function Send-PbdFile([string]$Source,[string]$Destination) {scp @script:PbdOpts $Source "${script:PbdTarget}:$Destination"; if($LASTEXITCODE -ne 0){throw 'Upload failed'}}
function Get-PbdFile([string]$Source,[string]$Destination) {scp @script:PbdOpts "${script:PbdTarget}:$Source" $Destination; if($LASTEXITCODE -ne 0){throw 'Download failed'}}

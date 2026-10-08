param([string]$Command,[string]$Upload,[string]$Download,[string]$Remote)
$cfg=@{}
foreach($line in Get-Content -LiteralPath 'E:/Z/.env'){if($line -match '^\s*([^#=\s]+)\s*=\s*(.*)$'){$cfg[$matches[1]]=$matches[2]}}
$env:DCDLP_SSH_PASSWORD=[string]$cfg.psw
$env:SSH_ASKPASS='E:/Z/dcdlp_askpass.exe'
$env:SSH_ASKPASS_REQUIRE='force'
$env:DISPLAY='codex'
$opt=@('-o','ConnectTimeout=20','-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile=NUL')
$hostSpec="$($cfg.user)@$($cfg.ip)"
if($Upload){ & scp @opt $Upload "${hostSpec}:$Remote" }
elseif($Download){ & scp @opt "${hostSpec}:$Remote" $Download }
else { & ssh @opt $hostSpec $Command }
exit $LASTEXITCODE

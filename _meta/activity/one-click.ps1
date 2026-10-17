param(
    [switch]$Setup,
    [switch]$Scheduled
)

$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$collector = Join-Path $PSScriptRoot 'collect.py'
$dataFile = Join-Path $root 'docs\assets\activity\data.json'
$privateDir = Join-Path $env:LOCALAPPDATA 'AIActivityDashboard'
$readTokenFile = Join-Path $privateDir 'read-token.dpapi'
$writeTokenFile = Join-Path $privateDir 'publish-token.dpapi'
$consentFile = Join-Path $privateDir 'publish-consent.txt'
$analyzerShim = Join-Path $privateDir 'codex-analyzer.cmd'
$targetRepo = 'seok-jun/ai-agent-diary'
$targetBranch = 'main'
$targetPath = 'docs/assets/activity/data.json'

function Ask-Default([string]$label, [string]$default) {
    $value = Read-Host "$label [$default]"
    if ([string]::IsNullOrWhiteSpace($value)) { return $default }
    return $value.Trim()
}

function Save-PrivateSecret([string]$label, [string]$destination) {
    $secret = Read-Host $label -AsSecureString
    $encrypted = ConvertFrom-SecureString -SecureString $secret
    [IO.File]::WriteAllText($destination, $encrypted, (New-Object System.Text.UTF8Encoding($false)))
    $secret.Dispose()
}

function Get-PrivateSecret([string]$source) {
    $ciphertext = [IO.File]::ReadAllText($source)
    $secure = ConvertTo-SecureString $ciphertext
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
        $secure.Dispose()
    }
}

function Add-DailySchedule {
    try {
        $actionArgs = '-NoProfile -ExecutionPolicy RemoteSigned -File "' + $PSCommandPath + '" -Scheduled'
        $action = New-ScheduledTaskAction -Execute "$env:WINDIR\System32\WindowsPowerShell\v1.0\powershell.exe" -Argument $actionArgs
        $trigger = New-ScheduledTaskTrigger -Daily -At '23:30'
        $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
        $identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
        $principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
        Register-ScheduledTask -TaskName 'AI Activity Dashboard Update' -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
        Write-Host '매일 23:30 자동 실행이 등록되었습니다. (로그인 사용자 세션)'
    } catch {
        Write-Host '자동 실행을 등록하지 못했습니다. 원클릭 수동 갱신은 계속 사용할 수 있습니다.'
    }
}

function Initialize-Settings {
    [IO.Directory]::CreateDirectory($privateDir) | Out-Null
    Write-Host ''
    Write-Host '=== AI 활동 대시보드: 최초 1회 설정 ==='
    Write-Host '아래 설정과 토큰은 이 PC의 개인 폴더에만 저장됩니다.'
    Write-Host 'GitHub 사용자와 Public/Private 저장소는 키로 자동 조회합니다.'
    Write-Host '프로젝트명, PR 제목, 커밋 메시지는 공개하지 않습니다.'
    Write-Host ''
    Write-Host '브라우저에서 GitHub Fine-grained PAT 2개를 준비하세요.'
    Write-Host '  A. 읽기 전용: 집계할 모든 저장소 Contents / Pull requests / Issues = Read'
    Write-Host '       토큰이 허용한 저장소만 자동 발견됩니다. All repositories 권한 설정을 확인하세요.'
    Write-Host '  B. 게시 전용: ai-agent-diary 하나만 Contents = Read and write'
    Write-Host '토큰은 공용 저장소가 아닌 이 PC 사용자 계정 DPAPI로 암호화합니다.'
    $consent = Ask-Default '검증된 날짜/숫자 집계를 공개 블로그 main에 자동 게시할까요? y/N' 'N'
    if ($consent -notmatch '^[yY]$') { throw '공개 게시 동의가 없어 설정을 취소했습니다.' }
    Save-PrivateSecret 'A. 집계용 읽기 전용 PAT' $readTokenFile
    Save-PrivateSecret 'B. 블로그 게시 전용 PAT' $writeTokenFile
    [IO.File]::WriteAllText($consentFile, 'approved')
    Write-Host '개인 설정이 저장되었습니다.'
    $schedule = Ask-Default '매일 23:30 자동 갱신을 예약할까요? y/N' 'N'
    if ($schedule -match '^[yY]$') { Add-DailySchedule }
}

function Get-Python {
    $py = Get-Command 'py.exe' -ErrorAction SilentlyContinue
    if ($py) {
        & $py.Source -3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>$null
        if ($LASTEXITCODE -eq 0) { return @{ file = $py.Source; prefix = @('-3') } }
    }
    $python = Get-Command 'python.exe' -ErrorAction SilentlyContinue
    if ($python) {
        & $python.Source -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>$null
        if ($LASTEXITCODE -eq 0) { return @{ file = $python.Source; prefix = @() } }
    }
    throw 'Python 3.10 이상이 필요합니다. 설치 후 이 파일을 다시 더블클릭하세요.'
}

function Invoke-Collector([hashtable]$python, [string[]]$arguments) {
    $commandArgs = @($python.prefix) + @($collector) + $arguments
    & $python.file @commandArgs
    if ($LASTEXITCODE -ne 0) { throw '데이터 수집·검증에 실패했습니다. 기존 게시 데이터는 유지됩니다.' }
}

function Initialize-AnalyzerShim {
    $npx = Get-Command 'npx.cmd' -ErrorAction SilentlyContinue
    if (-not $npx) { throw 'Node.js/npm의 npx.cmd가 필요합니다. Node.js 20 이상을 확인하세요.' }
    $native = Get-Command 'codex.exe' -ErrorAction SilentlyContinue
    $nativePath = $null
    if ($native) { $nativePath = $native.Source }
    if (-not $nativePath) {
        $installed = Join-Path $env:APPDATA 'npm\node_modules\@openai\codex'
        if (Test-Path -LiteralPath $installed) {
            $found = Get-ChildItem -LiteralPath $installed -Filter 'codex.exe' -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) { $nativePath = $found.FullName }
        }
    }
    if (-not $nativePath) { throw 'Codex CLI의 codex.exe를 찾지 못했습니다. @openai/codex 설치 상태를 확인하세요.' }
    # The shim contains paths but never credentials or private repository names.
    $nativeDir = Split-Path -Parent $nativePath
    $shimLines = @(
        '@echo off',
        ('set "PATH=' + $nativeDir + ';%PATH%"'),
        ('call "' + $npx.Source + '" --yes codex-usage-analyzer@0.4.1 %*')
    )
    [IO.File]::WriteAllLines($analyzerShim, $shimLines, [Text.Encoding]::Default)
    return $analyzerShim
}

function Publish-SafeJson {
    $publicData = [IO.File]::ReadAllBytes($dataFile)
    $base64 = [Convert]::ToBase64String($publicData)
    $token = Get-PrivateSecret $writeTokenFile
    if ([string]::IsNullOrWhiteSpace($token)) { throw '게시 토큰이 비어 있습니다.' }
    $headers = @{
        'Authorization' = 'Bearer ' + $token
        'Accept' = 'application/vnd.github+json'
        'X-GitHub-Api-Version' = '2022-11-28'
        'User-Agent' = 'ai-activity-one-click'
    }
    $uri = 'https://api.github.com/repos/' + $targetRepo + '/contents/' + $targetPath
    try {
        $remote = Invoke-RestMethod -Uri ($uri + '?ref=' + $targetBranch) -Headers $headers -Method Get -MaximumRedirection 0 -TimeoutSec 30
        if (-not $remote.sha -or -not $remote.content) { throw 'invalid remote data' }
        $remote64 = [regex]::Replace([string]$remote.content, '\s', '')
        if ($remote64 -eq $base64) {
            Write-Host '변경 사항이 없어 게시를 건너뛰었습니다.'
            return
        }
        $body = @{
            message = 'Update safe AI development activity aggregates'
            content = $base64
            sha = [string]$remote.sha
            branch = $targetBranch
        } | ConvertTo-Json -Depth 5 -Compress
        $result = Invoke-RestMethod -Uri $uri -Headers $headers -Method Put -ContentType 'application/json; charset=utf-8' -Body ([Text.Encoding]::UTF8.GetBytes($body)) -MaximumRedirection 0 -TimeoutSec 60
        if (-not $result.commit.sha) { throw 'missing commit confirmation' }
        Write-Host '게시 완료! main의 숫자 통계가 갱신되었습니다. Pages 배포는 GitHub가 처리합니다.'
    } catch {
        throw 'GitHub 게시 실패: 먼저 활동 페이지 PR을 main에 병합했는지, 게시 PAT에 Contents 쓰기 권한이 있는지 확인하세요. (공개 데이터 일부 게시 없음)'
    } finally {
        $token = $null
        $headers = $null
    }
}

try {
    if (-not (Test-Path -LiteralPath $consentFile) -or $Setup) {
        if ($Scheduled) { throw '최초 설정이 필요합니다. update-activity.cmd를 직접 실행하세요.' }
        Initialize-Settings
    }
    foreach ($file in @($readTokenFile, $writeTokenFile, $consentFile)) {
        if (-not (Test-Path -LiteralPath $file)) { throw '개인 설정이 불완전합니다. configure-activity.cmd를 실행하세요.' }
    }
    $python = Get-Python
    Write-Host ''
    Write-Host '[1/4] Codex 통계 실시간 조회 및 검증'
    $analyzer = Initialize-AnalyzerShim
    Invoke-Collector -python $python -arguments @('codex', '--analyzer', $analyzer)

    Write-Host '[2/4] GitHub 계정 및 접근 가능 저장소 자동 검색 후 활동 집계'
    $env:ACTIVITY_READ_TOKEN = Get-PrivateSecret $readTokenFile
    $env:ACTIVITY_EXPECTED_GITHUB_LOGIN = ($targetRepo -split '/')[0]
    try {
        Invoke-Collector -python $python -arguments @('github-auto')
    } finally {
        Remove-Item Env:ACTIVITY_READ_TOKEN -ErrorAction SilentlyContinue
        Remove-Item Env:ACTIVITY_EXPECTED_GITHUB_LOGIN -ErrorAction SilentlyContinue
    }

    Write-Host '[3/4] 공개 숫자만 최종 검증'
    Invoke-Collector -python $python -arguments @('validate')

    Write-Host '[4/4] 블로그에 자동 게시'
    Publish-SafeJson
    Write-Host '완료: https://seok-jun.github.io/ai-agent-diary/activity/'
    exit 0
} catch {
    # Never print tokens, private paths, repo lists, upstream HTTP responses or raw exceptions.
    Write-Host ''
    Write-Host '실행에 실패했습니다. 공개된 데이터는 변경하지 않았습니다.'
    Write-Host 'Codex 로그인, Python/Node 설치, PAT 권한, PR 병합 상태와 개인 설정을 확인하세요.'
    exit 1
} finally {
    Remove-Item Env:ACTIVITY_READ_TOKEN -ErrorAction SilentlyContinue
    Remove-Item Env:ACTIVITY_EXPECTED_GITHUB_LOGIN -ErrorAction SilentlyContinue
}

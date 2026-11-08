param([switch]$Aplicar)

$ErrorActionPreference = 'Stop'
$workspaceRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..')).TrimEnd('\')
$testRoot = Join-Path $workspaceRoot '.pruebas'
$candidatePaths = [Collections.Generic.List[string]]::new()

function Assert-WorkspacePath([string]$Path) {
    $absolute = [IO.Path]::GetFullPath($Path)
    if (-not $absolute.StartsWith($workspaceRoot + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "Ruta fuera del proyecto: $absolute"
    }
    $ancestor = Get-Item -LiteralPath $absolute -Force
    while ($ancestor.FullName -ne $workspaceRoot) {
        if ($ancestor.Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "No se siguen enlaces ni junctions: $($ancestor.FullName)"
        }
        $ancestor = $ancestor.Parent
    }
    return $absolute
}

function Find-Candidates([string]$Folder) {
    foreach ($entry in Get-ChildItem -LiteralPath $Folder -Directory -Force) {
        if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
        if ($entry.Name -in @('.git', '.venv', '.aws', 'node_modules')) { continue }
        $isTest = $entry.FullName.StartsWith($testRoot + '\', [StringComparison]::OrdinalIgnoreCase)
        $isProfile = $isTest -and ($entry.Name -match '^perfil(?:-\d+)?$')
        $isInstallCache = $entry.FullName -eq (Join-Path $testRoot 'pip-cache')
        $isEditorTest = $entry.Parent.FullName -eq $testRoot -and $entry.Name -match '^edicion-\d+$'
        if ($entry.Name -eq '__pycache__' -or $isProfile -or $isInstallCache -or $isEditorTest) {
            $candidatePaths.Add((Assert-WorkspacePath $entry.FullName))
        } else {
            Find-Candidates $entry.FullName
        }
    }
}

function Measure-SafeTree([string]$Folder) {
    $bytes = [long]0
    $files = 0
    $pending = [Collections.Generic.Stack[string]]::new()
    $pending.Push($Folder)
    while ($pending.Count -gt 0) {
        foreach ($entry in Get-ChildItem -LiteralPath $pending.Pop() -Force) {
            if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw "El temporal contiene un enlace; se conserva: $($entry.FullName)"
            }
            if ($entry.PSIsContainer) {
                $pending.Push($entry.FullName)
            } else {
                $bytes += $entry.Length
                $files++
            }
        }
    }
    return @{ bytes = $bytes; archivos = $files }
}

Find-Candidates $workspaceRoot
$items = @(
    foreach ($candidate in $candidatePaths) {
        $measurement = Measure-SafeTree $candidate
        [PSCustomObject]@{
            ruta = $candidate.Substring($workspaceRoot.Length + 1).Replace('\', '/')
            bytes = $measurement.bytes
            archivos = $measurement.archivos
        }
    }
)
$totalBytes = [long](($items | Measure-Object -Property bytes -Sum).Sum)
$totalFiles = [long](($items | Measure-Object -Property archivos -Sum).Sum)
$report = [ordered]@{
    aplicado = [bool]$Aplicar
    directorios = $items.Count
    archivos = $totalFiles
    bytes = $totalBytes
    elementos = $items
}

if ($Aplicar) {
    $reportFolder = Join-Path $workspaceRoot ('.local/limpieza/' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    New-Item -ItemType Directory -Path $reportFolder -Force | Out-Null
    $reportPath = Join-Path $reportFolder 'informe.json'
    $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportPath -Encoding UTF8
    $remaining = [Collections.Generic.List[string]]::new()
    foreach ($candidate in $candidatePaths) {
        $verified = Assert-WorkspacePath $candidate
        try {
            Remove-Item -LiteralPath $verified -Recurse -Force
        } catch {
            $remaining.Add($verified)
            Write-Warning "Temporal ocupado o inaccesible; se conserva lo que siga en uso: $verified"
        }
    }
    $remainingBytes = [long]0
    $remainingFiles = [long]0
    foreach ($candidate in $remaining) {
        $measurement = Measure-SafeTree $candidate
        $remainingBytes += $measurement.bytes
        $remainingFiles += $measurement.archivos
    }
    $report['directorios_eliminados'] = $items.Count - $remaining.Count
    $report['archivos_eliminados'] = $totalFiles - $remainingFiles
    $report['bytes_liberados'] = $totalBytes - $remainingBytes
    $report['temporales_ocupados'] = @($remaining)
    $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $reportPath -Encoding UTF8
    Write-Output "Temporales retirados: $($report.directorios_eliminados) directorios, $($report.archivos_eliminados) archivos, $($report.bytes_liberados) bytes."
    Write-Output "Informe: $reportPath"
} else {
    $report | ConvertTo-Json -Depth 5
}

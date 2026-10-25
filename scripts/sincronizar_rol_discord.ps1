[CmdletBinding()]
param(
    [ValidateSet('sincronizar', 'estado', 'inicializar')]
    [string]$Accion = 'sincronizar',
    [ValidateRange(1, 1000)]
    [int]$Ventana = 100
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$discordProjectPath = Split-Path $PSScriptRoot -Parent
$discordPythonPath = Join-Path $discordProjectPath '.venv\Scripts\python.exe'
$discordScriptPath = Join-Path $PSScriptRoot 'sincronizar_rol_discord.py'
$discordSecureToken = $null
$discordTokenPointer = [IntPtr]::Zero
$discordPlainToken = $null
$discordExitCode = 1

try {
    if ($Accion -eq 'sincronizar') {
        $discordTokenPath = Join-Path $discordProjectPath '.local\discord\token.dpapi'
        $discordSecureToken = ConvertTo-SecureString -String ([System.IO.File]::ReadAllText($discordTokenPath))
        $discordTokenPointer = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($discordSecureToken)
        $discordPlainToken = [System.Runtime.InteropServices.Marshal]::PtrToStringBSTR($discordTokenPointer)
        # El token viaja solo por stdin; nunca aparece en argumentos ni archivos.
        $discordPlainToken | & $discordPythonPath -X utf8 $discordScriptPath sincronizar --ventana $Ventana
    }
    else {
        & $discordPythonPath -X utf8 $discordScriptPath $Accion
    }
    $discordExitCode = $LASTEXITCODE
}
catch {
    Write-Host 'No se pudo iniciar la sincronizacion local con esta cuenta de Windows.'
}
finally {
    $discordPlainToken = $null
    if ($discordTokenPointer -ne [IntPtr]::Zero) {
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($discordTokenPointer)
    }
    if ($null -ne $discordSecureToken) {
        $discordSecureToken.Dispose()
    }
}
exit $discordExitCode

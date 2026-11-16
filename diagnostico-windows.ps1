# Somente leitura: registra eventos de bloqueio da integridade de codigo.
Write-Host "Flipmelon - eventos de Code Integrity (ultimos 3 dias)"
try {
  Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-CodeIntegrity/Operational';Id=3077;StartTime=(Get-Date).AddDays(-3)} -MaxEvents 12 -ErrorAction Stop |
    Select-Object TimeCreated, Message | Format-List
} catch {
  Write-Host "Nao foi possivel obter os eventos: $($_.Exception.Message)"
}

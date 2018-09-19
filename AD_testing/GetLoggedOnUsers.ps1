function Get-LoggedOnUser
{
  [CmdletBinding()]
  param
  (
    [Parameter()]
    [ValidateScript({ Test-Connection -ComputerName $_ -Quiet -Count 1 })]
    [ValidateNotNullOrEmpty()]
    [string[]]$ComputerName = $env:COMPUTERNAME
  )
  foreach ($comp in $ComputerName)
  {
    $output = @{ 'ComputerName' = $comp }
    $output.UserName = (Get-WmiObject -Class win32_computersystem -ComputerName $comp).UserName
    [PSCustomObject]$output
  }
}


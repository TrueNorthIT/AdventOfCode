
(Get-Content "$PSScriptRoot\input.txt").Split(",") | ForEach-Object {
    $range = $_.Split("-")
    for ($i = [long]$range[0]; $i -le [long]$range[1]; $i++) {
        $istr = $i.ToString()
        if ($istr.Length % 2 -eq 0)
        {
            if ($istr.Substring(0, $istr.Length / 2) -eq $istr.Substring($istr.Length / 2))
            {
                $i
            }
        }
    }
} | Measure-Object -Sum | Select-Object -Property Sum
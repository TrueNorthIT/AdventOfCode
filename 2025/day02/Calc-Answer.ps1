
(Get-Content "$PSScriptRoot\input.txt").Split(",") | ForEach-Object {
    $range = $_.Split("-")
    for ($i = [long]$range[0]; $i -le [long]$range[1]; $i++) {
        $istr = $i.ToString()
        $matching = $false
        for ($fragments = 2; (-not $matching) -and ($fragments -le $istr.Length); $fragments ++) {
            if ($istr.Length % $fragments -eq 0)
            {
                $firstPart = $istr.Substring(0, $istr.Length / $fragments)
                $index = $firstPart.Length
                $matching = $true
                do
                {
                    if ($firstPart -ne $istr.Substring($index, $firstPart.Length))
                    {
                        $matching = $false
                    }
                    $index += $firstPart.Length
                } while ($matching -and ($index -lt $istr.Length))
            }
        }
        if ($matching) {
            $i
        }
    }
} | Measure-Object -Sum | Select-Object -Property Sum
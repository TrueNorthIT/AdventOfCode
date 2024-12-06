$lines = Get-Content "$PSScriptRoot\input.txt"
$index = 0
$positionsOccupied = @{}

function Find-Guard($Lines)
{
    $foundXIndex = -1
    for ($index = 0; $index -lt $Lines.Count; $index++) {
        $foundXIndex = $Lines[$index].IndexOf("^");
        if ($foundXIndex -gt -1) 
        {
            return [pscustomobject] @{x=$foundXIndex;y=$index;x_delta=0;y_delta=-1}
        }
    }
}

function Move-Guard($Lines, $Position, $Occupations)
{
    $x_max = $lines[0].length - 1
    $y_max = $lines.length - 1
    $lastPosition = [pscustomobject] @{
        x=$Position.x;
        y=$Position.y;
        x_delta=$Position.x_delta;
        y_delta=$Position.y_delta}
    $nextPosition = [pscustomobject] @{
        x=$lastPosition.x + $Position.x_delta;
        y=$lastPosition.y + $Position.y_delta;
        x_delta=$Position.x_delta;
        y_delta=$Position.y_delta}
    while ($true)
    {
        if ($nextPosition.x -lt 0 -or $nextPosition.x -gt $x_max -or $nextPosition.y -lt 0 -or $nextPosition.y -gt $y_max)
        {
            return $()
        }
        if ($Lines[$nextPosition.y][$nextPosition.x] -eq "#")
        {
            $lastPosition.x_delta = -$Position.y_delta
            $lastPosition.y_delta = $Position.x_delta
            return $lastPosition
        }
        $positionsOccupied[($nextPosition.y*1000) + $nextPosition.x] = $true
        $lastPosition = [pscustomobject] @{
            x=$nextPosition.x;
            y=$nextPosition.y;
            x_delta=$Position.x_delta;
            y_delta=$Position.y_delta}
        $nextPosition = [pscustomobject] @{
            x=$lastPosition.x + $Position.x_delta;
            y=$lastPosition.y + $Position.y_delta;
            x_delta=$Position.x_delta;
            y_delta=$Position.y_delta}
    }
}


$guardPos = Find-Guard -Lines $lines

Write-Host "Guard is at ($($guardPos.x),$($guardPos.y)), facing ($($guardPos.x_delta),$($guardPos.y_delta))"
$positionsOccupied[($guardPos.y*1000) + $guardPos.x] = $true

while ($guardPos)
{
    $guardPos = Move-Guard -Lines $lines -Position $guardPos -Occupations $positionsOccupied
}
Write-Host "Total positions occupied = $($positionsOccupied.Keys.Count)"


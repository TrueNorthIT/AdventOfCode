var robots = File.ReadAllLines("input.txt").Select(line => string.Concat(
        line.Where(ch => char.IsDigit(ch) || ch == ' ' || ch == '-' || ch == ','))
    .Split([" ", ","], StringSplitOptions.RemoveEmptyEntries).Select(long.Parse).ToList())
    .Select(arr => arr switch { [var px, var py, var vx, var vy] 
        => (px,py, vx, vy)
    }).ToList();

const int W = 101;
const int H = 103;
var step = (long step) => robots.Select(robot => 
    (   x: (robot.px + step * (robot.vx + W)) % W,
        y: (robot.py + step * (robot.vy + H)) % H));

long countQuadrants(IEnumerable<(long x, long y)> robots)
    => robots.CountBy(tp => tp switch {
        ( < W / 2, < H / 2) => 0,
        ( > W / 2, < H / 2) => 1,
        ( < W / 2, > H / 2) => 2,
        ( > W / 2, > H / 2) => 3,
        (var x, var y) when x == W / 2 || y == H / 2 => 99,
    }).Where(kvp => kvp.Key != 99)
    .Aggregate(1L, (acc, n) => acc * n.Value);

(var bx, var by) = (analyse(true), analyse(false));
for (long t = bx; true; t += W)
    if (t % H == by)
    {
        Console.WriteLine(showGrid(step(t)));
        Console.WriteLine($"Part 1: {countQuadrants(step(100))}, Part 2: t={t}");
        Console.WriteLine($"{t} = {bx} mod {H}");
        Console.WriteLine($"{t} = {by} mod {W}");
        break;
    }

long analyse(bool xDir)
{
    const bool PRINT = true;
    var direction = xDir ? "x" : "y";
    (var minVariance, var minVarianceStep) = (double.MaxValue, 0);
    var limit = xDir ? W : H;

    for (int s = 0; s < limit; s++)
    {
        var variance = step(s).Select(point => xDir ? point.x : point.y) switch { var positions
            => positions.Average() switch { var mean 
            => positions.Sum(p => Math.Pow(p - mean, 2)) }};
        
        (minVariance, minVarianceStep) = variance < minVariance ? (variance, s) 
            : (minVariance, minVarianceStep);

        if (PRINT)
        {
            //plot the distribution by count, it looks like a tree in 1d when we hit the magic number :)
            printSpectrum(s, xDir, limit);
            Console.WriteLine($"Step = {s}, variance = {variance:F1}");
            Console.WriteLine();
            Thread.Sleep(50);
        }
    }

    Console.SetCursorPosition(0, 0);
    printSpectrum(minVarianceStep, xDir, limit);
    Console.WriteLine();
    Console.WriteLine($"Check complete for axis {direction}, signal detected with variance {minVariance} at s={minVarianceStep}:");
    return minVarianceStep;
}

///
/// Helpers to visualize the grid and the spectrums
///
void printSpectrum(long s, bool xDir, int limit)
{
    Console.SetCursorPosition(0, 0);    
    var countsByPosition = Enumerable.Range(0, limit)
        .Select(i => step(s).Select(point => xDir ? point.x : point.y)
        .GroupBy(p => p).ToDictionary(kvp => kvp.Key, 
            kvp => kvp.Count()).GetValueOrDefault(i, 0))
    .ToArray();

    for (int h = 30; h >= 1; h--)
        Console.WriteLine(String.Concat(countsByPosition.Select(v => v >= h ? "*" : " ")));
}

string showGrid(IEnumerable<(long x, long y)> robots)
{
    var output = Enumerable.Range(0, H).Select(y => Enumerable.Repeat(' ', W).ToArray()).ToArray();    
    foreach (var robot in robots)
        output[robot.y][robot.x] = '*';

    var result = new System.Text.StringBuilder();
    foreach (var arr in output)
    {
        foreach (var ch in arr)
            result.Append(ch);
        result.AppendLine();
    }
    result.AppendLine();

    return result.ToString();
}
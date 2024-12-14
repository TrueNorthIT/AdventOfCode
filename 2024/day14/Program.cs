var robots = File.ReadAllLines("input.txt").Select(line => string.Concat(
        line.Where(ch => char.IsDigit(ch) || ch == ' ' || ch == '-' || ch == ','))
    .Split([" ", ","], StringSplitOptions.RemoveEmptyEntries).Select(long.Parse).ToList())
    .Select(arr => arr switch {
        [var px, var py, var vx, var vy] => (px,py, vx, vy)
    }).ToList();

(var W, var H) = (101, 103);
var step = (long step) => robots.Select(robot => 
    (   x: (robot.px + step * (robot.vx + W)) % W,
        y: (robot.py + step * (robot.vy + H)) % H));


Console.WriteLine($"Part 1: {countQuadrants(step(100))}");

(var bx, var by) = (analyse(true), analyse(false));
for (long t = bx; true; t += W)
    if (t % H == by)
    {
        printGrid(step(t));
        Console.WriteLine($"Tree detected at t={t}");
        Console.WriteLine($"{t} = {bx} mod 101");
        Console.WriteLine($"{t} = {by} mod 103");
        break;
    }

long countQuadrants(IEnumerable<(long x, long y)> robots)
{
    var quadrants = new long[] { 0, 0, 0, 0, 0 };
    foreach (var robot in robots)
    {
        if (robot.x == (W / 2) || robot.y == H / 2)
            quadrants[4]++;
        if (robot.x < (W / 2) && robot.y < H / 2)
            quadrants[0]++;
        if (robot.x < (W / 2) && robot.y > H / 2)
            quadrants[1]++;
        if (robot.x > (W / 2) && robot.y < H / 2)
            quadrants[2]++;
        if (robot.x > (W / 2) && robot.y > H / 2)
            quadrants[3]++;
    }
    return quadrants.Take(4).Aggregate(1L, (acc, n) => acc * n);
}

long analyse(bool xDir)
{
    var direction = xDir ? "x" : "y";
    (var minVariance, var minVarianceStep) = (double.MaxValue, 0);
    var limit = xDir ? W : H;

    //loop through all possible values for this axis
    //and plot the distribution by count, it looks like a tree in 1d :)
    for (int s = 0; s < limit; s++)
    {
        var variance = printSpectrum(s, xDir, limit);
        if (variance < minVariance)
        {
            (minVariance, minVarianceStep) = (variance, s);
        }
        Console.WriteLine($"Step = {s}, variance = {variance:F1}");
        Console.WriteLine();
        Thread.Sleep(50);
    }

    Console.SetCursorPosition(0, 0);
    printSpectrum(minVarianceStep, xDir, limit);
    Console.WriteLine();
    Console.WriteLine($"Check complete for axis {direction}, signal detected with variance {minVariance} at s={minVarianceStep}:");
    Console.WriteLine();
    Console.ReadKey();
    return minVarianceStep;
}
double printSpectrum(long s, bool xDir, int limit)
{
    Console.SetCursorPosition(0, 0);
    var positions = step(s).Select(point => xDir ? point.x : point.y);
    var countsByPositionsMap = positions.GroupBy(p => p).ToDictionary(kvp => kvp.Key, kvp => kvp.Count());
    var countsByPosition = Enumerable.Range(0, limit).Select(i => countsByPositionsMap.GetValueOrDefault(i, 0)).ToArray();

    var mean = positions.Average();
    var variance = positions.Sum(p => Math.Pow(p - mean, 2));
    for (int h = 30; h >= 1; h--)
    {
        var line = String.Concat(countsByPosition.Select(v => v >= h ? "*" : "."));
        Console.WriteLine(line);
    }

    return variance;
}

void printGrid(IEnumerable<(long x, long y)> robots)
{
    var output = Enumerable.Range(0, H).Select(y => Enumerable.Repeat('.', W).ToArray()).ToArray();
    foreach (var robot in robots)
        output[robot.y][robot.x] = '*';
    foreach (var arr in output)
    {
        foreach (var ch in arr)
            Console.Write(ch);
        Console.WriteLine();
    }
    Console.WriteLine();
}
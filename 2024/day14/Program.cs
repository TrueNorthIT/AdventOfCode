var robots = File.ReadAllLines("input.txt").Select(line => string.Concat(
        line.Where(ch => char.IsDigit(ch) || ch == ' ' || ch == '-' || ch == ','))
    .Split([" ", ","], StringSplitOptions.RemoveEmptyEntries).Select(long.Parse).ToList())
    .Select(arr => arr switch {
        [var px, var py, var vx, var vy] => (px,py, vx, vy)
    }).ToList();

(var W, var H) = (101, 103);
List<(long x, long y)> step(long step)
{
    var next = robots.Select(robot => 
        ((robot.px + step * (robot.vx + W)) % W,
        (robot.py + step * (robot.vy + H)) % H))
    .ToList();

    if ((step - 86) % 101 == 0)
    {
        Console.WriteLine($"STEP={step}");
        print(next);
    }
    return next;
}

long countQuadrants(List<(long x, long y)> robots)
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
Console.WriteLine($"Part 1: {countQuadrants(step(100))}");

for (var s = 0; s <= 10403; s++)
    step(s);

Console.WriteLine($"Part 2: Inspect the output!");


void print(List<(long x, long y)> robots)
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
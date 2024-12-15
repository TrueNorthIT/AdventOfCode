var start = File.ReadAllLines("input.txt").Select(line => string.Concat(
        line.Where(ch => char.IsDigit(ch) || ch == ' ' || ch == '-' || ch == ','))
    .Split([" ", ","], StringSplitOptions.RemoveEmptyEntries).Select(int.Parse).ToList())
    .Select(arr => arr switch { [var px, var py, var vx, var vy] 
        => (px,py, vx, vy)
    }).ToList();

const int W = 101; const int H = 103;

(int x, int y)[] robots(int step) => start.Select(robot => 
    (   x: (robot.px + step * (robot.vx + W)) % W,
        y: (robot.py + step * (robot.vy + H)) % H)).ToArray();

long countQuadrants((int x, int y)[] robots)
    => robots.CountBy(tp => tp switch {
        ( < W / 2, < H / 2) => 0,
        ( > W / 2, < H / 2) => 1,
        ( < W / 2, > H / 2) => 2,
        ( > W / 2, > H / 2) => 3,
        (var x, var y) when x == W / 2 || y == H / 2 => 99,
    }).Where(kvp => kvp.Key != 99)
    .Aggregate(1L, (acc, n) => acc * n.Value);

Console.WriteLine($"Part 1: {countQuadrants(robots(100))}");
(var bx, var by) = (analyse(true), analyse(false));

var part2 = bx + W * Enumerable.Range(0, int.MaxValue).First(i => (bx + W * i) % H == by);
Console.WriteLine($"Part 2: {part2}");

int analyse(bool xDir) =>
    Enumerable.Range(0, xDir ? W : H).Index().MinBy(s => robots(s.Item)
    .Select(point => xDir ? point.x : point.y) switch { var positions
    => positions.Average() switch { var mean 
    => positions.Sum(position => Math.Pow(position - mean, 2)) }}).Index;

//Console.WriteLine(showGrid(step(t)));
//Console.WriteLine($"{t} = {bx} mod {H}");
//Console.WriteLine($"{t} = {by} mod {W}");

///
/// Helpers to visualize the grid and the spectrums
///
//void printSpectrum(long s, bool xDir, int limit)
//{
//    Console.SetCursorPosition(0, 0);    
//    var countsByPosition = Enumerable.Range(0, limit)
//        .Select(i => step(s).Select(point => xDir ? point.x : point.y)
//        .GroupBy(p => p).ToDictionary(kvp => kvp.Key, 
//            kvp => kvp.Count()).GetValueOrDefault(i, 0))
//    .ToArray();

//    for (int h = 30; h >= 1; h--)
//        Console.WriteLine(String.Concat(countsByPosition.Select(v => v >= h ? "*" : " ")));
//}

//string showGrid(IEnumerable<(long x, long y)> robots)
//{
//    var output = Enumerable.Range(0, H).Select(y => Enumerable.Repeat(' ', W).ToArray()).ToArray();    
//    foreach (var robot in robots)
//        output[robot.y][robot.x] = '*';

//    var result = new System.Text.StringBuilder();
//    foreach (var arr in output)
//    {
//        foreach (var ch in arr)
//            result.Append(ch);
//        result.AppendLine();
//    }
//    result.AppendLine();

//    return result.ToString();
//}
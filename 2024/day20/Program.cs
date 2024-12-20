using System.Diagnostics;
using System.Numerics;

var grid = File.ReadAllText("input.txt").Split("\r\n")
        .SelectMany((line, r) => line.Select((ch, c) => (new Complex(r, c), ch)))
        .ToDictionary(tp => tp.Item1, tp => tp.ch);


var R = (int) grid.Max(kvp => kvp.Key.Real);
var C = (int) grid.Max(kvp => kvp.Key.Imaginary);

var start = grid.Where(kvp => kvp.Value == 'S').Single().Key;
var end = grid.Where(kvp => kvp.Value == 'E').Single().Key;
grid[start] = '.';
grid[end] = '.';

var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) }; //E, S, W, N

var timeFromEnd = solveNoCheats(start, end);

var p1Solutions = solve(2, timeFromEnd).GroupBy(tp => tp.timeSaved).OrderBy(grp => grp.Key);
var p1 = p1Solutions.Where(grp => grp.Key >= 100).Sum(grp => grp.Count());
Console.WriteLine($"Part 1: {p1}");

var p2Solutions = solve(20, timeFromEnd).GroupBy(tp => tp.timeSaved).OrderBy(grp => grp.Key);
var p2 = p2Solutions.Where(grp => grp.Key >= 100).Sum(grp => grp.Count());
Console.WriteLine($"Part 2: {p2}");

Dictionary<Complex, int> solveNoCheats(Complex start, Complex end)
{
    var route = new Dictionary<Complex, int>();
    var prev = end;
    int t = 0;
    route.Add(end, t);
    do
    {
        (end, prev) = (dirs.Select(dir => end + dir).Single(next =>
            next != prev && grid.GetValueOrDefault(next, '#') == '.'), end);
        t++;
        route.Add(end, t);
    }
    while (end != start);
    return route;
}

List<(int timeSaved, (int start, int end) cheat)> solve(int range, Dictionary<Complex, int> timesFromEnd)
{
    var results = new List<(int timeSaved, (int start, int end) cheat)>();
    foreach ((var from, var sourceTimeFromEnd) in timesFromEnd)
    {
        var _inRange = inRange(timesFromEnd, from, range);
        foreach ((var to, var cheatTime) in _inRange)
        {
            var timeSaved = sourceTimeFromEnd - timesFromEnd[to] - cheatTime;
            results.Add((timeSaved, (timesFromEnd[from], timesFromEnd[to])));
        }
    }
    return results;
}
List<(Complex pos, int cheatTime)> inRange(Dictionary<Complex, int> timeFromEnd, Complex from, int range)
{
    List<(Complex, int)> results = new();
    for (int r = -range; r <= range; r++)
        for (int c = -range; c <= range; c++)
        {
            var distance = Math.Abs(r) + Math.Abs(c);
            if (distance > range)
                continue;

            var key = new Complex(from.Real + r, from.Imaginary + c);
            if (timeFromEnd.ContainsKey(key))
            {
                results.Add((key, distance));
            }
        }
    return results;
}


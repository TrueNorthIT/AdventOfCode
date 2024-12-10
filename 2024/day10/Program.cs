using System.Numerics;

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var gridMap = grid.GroupBy(kvp => kvp.Value).ToDictionary(grp => grp.Key, grp => grp.Select(kvp => kvp.Key).ToList());

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };
var preceding = (char h, Complex square) =>
    dirs.Select(dir => square + dir)
    .Where(n => grid.ContainsKey(n) && (h - grid[n]) == 1);

var trailHeadsCanReach = gridMap['0'].ToDictionary(key => key, key => new HashSet<Complex>([key]));
solvedp(trailHeadsCanReach, (h, square) => preceding(h, square).SelectMany(neighbour => trailHeadsCanReach[neighbour]).ToHashSet());
Console.WriteLine($"Part 1: {gridMap['9'].Sum(square => trailHeadsCanReach[square].Count())}");

var pathCounts = gridMap['0'].ToDictionary(key => key, _ => 1);
solvedp(pathCounts, (h, square) => preceding(h, square).Sum(neighbour => pathCounts[neighbour]));
Console.WriteLine($"Part 2: {gridMap['9'].Sum(square => pathCounts[square])}");

void solvedp<T>(Dictionary<Complex, T> paths, Func<char, Complex, T> dp)
{
    for (char h = '1'; h <= '9'; h++)
        gridMap[h].ForEach(square => paths[square] = dp(h, square));
}
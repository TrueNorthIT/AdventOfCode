using System.Numerics;

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var heightMap = grid.GroupBy(kvp => kvp.Value).ToDictionary(grp => grp.Key, 
    grp => grp.Select(kvp => kvp.Key).ToList());

var dirs = new Complex[] { new (1, 0), new(0, -1), new(-1, 0), new(0, 1) };

var canReach = grid.Keys.ToDictionary(square => square, 
    square => grid[square] == '0' ? new HashSet<Complex>([square]) : []);

var paths = grid.Keys.ToDictionary(square => square, 
    square => grid[square] == '0' ? 1 : 0);

foreach (char h in Enumerable.Range('0', 10))
    foreach (var square in heightMap[h])
        foreach (var neighbour in dirs.Select(dir => square + dir)
            .Where(n => grid.ContainsKey(n) && (h - grid[n]) == 1))
    {
        canReach[square].UnionWith(canReach[neighbour]);
        paths[square] += paths[neighbour];
    }

Console.WriteLine($"Part 1: {heightMap['9'].Sum(
    square => canReach[square].Count())}");
Console.WriteLine($"Part 2: {heightMap['9'].Sum(square => paths[square])}");

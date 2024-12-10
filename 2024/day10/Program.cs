using System.Numerics;

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var gridMap = grid.GroupBy(kvp => kvp.Value).ToDictionary(grp => grp.Key, grp => grp.Select(kvp => kvp.Key).ToArray());

var neighourPaths = gridMap['0'].ToDictionary(key => key, key => new HashSet<Complex>(new[] { key }));
var dp1 = (char h, Complex square) => dirs.Select(dir => square + dir)
                        .Where(n =>
                            grid.ContainsKey(n) && (h - grid[n]) == 1)
                        .SelectMany(neighbour => neighourPaths[neighbour])
                        .ToHashSet();

solvedp(neighourPaths, '1', dp1);
var part1 = gridMap['9'].Sum(square => neighourPaths[square].Count());

var paths = gridMap['0'].ToDictionary(key => key, _ => 1);
var dp2 = (char h, Complex square) => dirs.Select(dir => square + dir)
                        .Where(n => grid.ContainsKey(n) && (h - grid[n]) == 1)
                        .Sum(neighbour => paths[neighbour]);

solvedp<int>(paths, '1', dp2);
var part2 = gridMap['9'].Sum(square => paths[square]);

Console.WriteLine($"Part 2: {part2}");

void solvedp<T>(Dictionary<Complex, T> paths, char h, Func<char, Complex, T> dp)
{
    foreach (var square in gridMap[h])
    {        
        paths[square] = dp(h, square);
    }

    if (h == '9')
        return;

    solvedp(paths, (char)(h + 1), dp);
}
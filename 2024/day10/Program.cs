using System.Numerics;

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var gridMap = grid.GroupBy(kvp => kvp.Value).ToDictionary(grp => grp.Key, grp => grp.Select(kvp => kvp.Key).ToArray());

var trailHeadsCanReach = gridMap['0'].ToDictionary(key => key, key => new HashSet<Complex>([key]));
var dp1 = (char h, Complex square) => dirs.Select(dir => square + dir)
                        .Where(n => grid.ContainsKey(n) && (h - grid[n]) == 1)
                        .SelectMany(neighbour => trailHeadsCanReach[neighbour])
                        .ToHashSet();

solvedp(trailHeadsCanReach, '1', dp1);
var part1 = gridMap['9'].Sum(square => trailHeadsCanReach[square].Count());

var pathCounts = gridMap['0'].ToDictionary(key => key, _ => 1);
var dp2 = (char h, Complex square) => dirs.Select(dir => square + dir)
                        .Where(n => grid.ContainsKey(n) && (h - grid[n]) == 1)
                        .Sum(neighbour => pathCounts[neighbour]);

solvedp(pathCounts, '1', dp2);
var part2 = gridMap['9'].Sum(square => pathCounts[square]);

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
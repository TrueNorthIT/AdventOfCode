using System.Numerics;

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var gridMap = grid.GroupBy(kvp => kvp.Value).ToDictionary(grp => grp.Key, grp => grp.Select(kvp => kvp.Key).ToArray());

var neighourPaths = gridMap['0'].ToDictionary(key => key, key => new HashSet<Complex>(new[] { key }));
solvedp(neighourPaths, '1');
var part11 = gridMap['9'].Sum(square => neighourPaths[square].Count());

var paths = gridMap['0'].ToDictionary(key => key, _ => 1);
solvedp2(paths, '1');
var part22 = gridMap['9'].Sum(square => paths[square]);


void solvedp(Dictionary<Complex, HashSet<Complex>> paths, char h)
{
    foreach (var square in gridMap[h])
    {
        var toMerge = dirs.Select(dir => square + dir)
                        .Where(n =>
                            grid.ContainsKey(n) && (h - grid[n]) == 1)
                        .SelectMany(neighbour => paths[neighbour])
                        .ToHashSet();        
        
        paths[square] = toMerge;
    }

    if (h == '9')
        return;

    solvedp(paths, (char)(h + 1));
}

void solvedp2(Dictionary<Complex,int> paths, char h)
{
    foreach (var square in gridMap[h])
        paths[square] = dirs.Select(dir => square + dir)
                        .Where(n => grid.ContainsKey(n) && (h - grid[n]) == 1)
                        .Sum(neighbour => paths[neighbour]);

    if (h == '9')
        return;

    solvedp2(paths, (char) (h + 1));
}



(int,int) solve()
{
    (int part1, int part2) = (0, 0);
    foreach (var kvp in grid.Where(kvp => kvp.Value == '0'))
    {
        var visitedCount = new[] { kvp.Key }.ToDictionary(key => key, _ => 1);
        var queue = new Queue<Complex>();
        queue.Enqueue(kvp.Key);
        while (queue.Any())
        {
            var current = queue.Dequeue();
            foreach (var next in dirs.Select(dir => current + dir)
                .Where(x => grid.ContainsKey(x) && (grid[x] - grid[current] == 1)))
            {
                if (visitedCount.TryAdd(next, visitedCount[current]))
                    queue.Enqueue(next);
                else
                    visitedCount[next] += visitedCount[current];

            }
        }

        var paths = visitedCount.Where(kvp => grid[kvp.Key] == '9').Select(kvp => kvp.Value);
        part1 += paths.Count();
        part2 += paths.Sum();
    }
    return (part1, part2);
}

var (part1, part2) = solve();
Console.WriteLine($"Part 1: {part1}");
Console.WriteLine($"Part 2: {part2}");
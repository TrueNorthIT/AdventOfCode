using System.Numerics;

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

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

Console.WriteLine($"Part 1: {part1}");
Console.WriteLine($"Part 2: {part2}");
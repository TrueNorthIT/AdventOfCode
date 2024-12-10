using System.Numerics;

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .Where(tp => tp.ch != '.')
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => int.Parse($"{tp.ch}"));

var dirs = Enumerable.Repeat(new Complex(1,0), 4).Aggregate(c => c * new int(0,1));

int part1 = 0;
int part2 = 0;
foreach (var kvp in grid.Where(kvp => kvp.Value == 0))
{
    var visited = new Dictionary<Complex,int>();
    var queue = new Queue<Complex>();
    queue.Enqueue(kvp.Key);
    while (queue.Any())
    {
        var current = queue.Dequeue();
        foreach (var next in dirs.Select(dir => current + dir)
            .Where(x => grid.ContainsKey(x) && (grid[x] - grid[current] == 1)))
        {
            if (visited.ContainsKey(next))
                visited[next]++;
            else
                visited.Add(next, 1);

            queue.Enqueue(next);
        }
    }
    part1 += visited.Where(kvp => grid[kvp.Key] == 9).Count();
    part2 += visited.Where(kvp => grid[kvp.Key] == 9).Sum(kvp => kvp.Value);
}

Console.WriteLine($"Part 1: {part1}");
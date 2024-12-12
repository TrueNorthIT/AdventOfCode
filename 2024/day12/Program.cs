using System;
using System.Numerics;

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };

var regions = new List<(int perimeter, int sides, HashSet<Complex> points)>();

foreach (var key in grid.Keys)
{
    if (regions.Any(region => region.points.Contains(key)))
        continue;

    var queue = new Queue<Complex>();
    queue.Enqueue(key);
    var visited = new HashSet<Complex>();
    var neighbours = new HashSet<(Complex, Complex)>();    
    //flood fill from here
    while (queue.Any())
    {
        var curr = queue.Dequeue();

        if (visited.Contains(curr))
            continue;

        foreach (var neighbour in dirs.Select(dir => curr + dir).Where(n => grid.ContainsKey(n) && grid[n] == grid[curr]))
        {
            queue.Enqueue(neighbour);
        }
        foreach (var neighbour in dirs.Select(dir => curr + dir).Where(n => (grid.ContainsKey(n) && grid[n] != grid[curr]) || !grid.ContainsKey(n)))
        {
            var wall = new[] { curr, neighbour }.OrderBy(c => c.Real).ThenBy(c => c.Imaginary).ToArray();            
            neighbours.Add((wall[0], wall[1]));
        }

        visited.Add(curr);
    }

    var sides = count(neighbours, grid[key], c => c.Imaginary, c => c.Real) + count(neighbours, grid[key], c => c.Real, c => c.Imaginary);
    regions.Add((neighbours.Count, sides, visited));
}

int count(HashSet<(Complex, Complex)>  neighbours, char plant, Func<Complex, double> first, Func<Complex, double> second)
{
    //(r1,c1) -> (r2,c2)
    //p1
    //p2
    //for a horizontal wall, the Im parts will match, the Real will be x and x+1
    //-   -- - -
    //  -    --
    //So we group by r / c and count the number of clusters
    //also keeping track of which c / r is inside for a particual scan-line so we know if we are on a new wall

    return neighbours.Where(c => first(c.Item1) == first(c.Item2))
        .GroupBy(c => second(c.Item1))
        .Select(grp => grp.OrderBy(c => first(c.Item1)).ToArray())
        .Sum(set =>
    {
        int count = 1;
        var inside = (grid.ContainsKey(set[0].Item1) ? grid[set[0].Item1] == plant : false) ? second(set[0].Item1) : second(set[0].Item2);
        var last = set[0];
        foreach (var h in set.Skip(1))
        {
            var newInside = (grid.ContainsKey(h.Item1) ? grid[h.Item1] == plant : false) ? second(h.Item1) : second(h.Item2);
            if (Math.Abs(first(h.Item1) - first(last.Item1)) > 1 || inside != newInside)
                count++;
            last = h;
            inside = newInside;
        }
        return count;
    });
};

var part1 = regions.Sum(tp => tp.perimeter * tp.points.Count);
Console.WriteLine($"Part 1: {part1}");
var part2 = regions.Sum(tp => tp.sides * tp.points.Count);
Console.WriteLine($"Part 2: {part2}");

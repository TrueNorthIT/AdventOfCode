using System.Numerics;

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };

var regions = new List<(int perimeter, int sides, HashSet<Complex> points)>();
foreach (var key in grid.Keys.Where(key => !regions.Any(region => region.points.Contains(key))))
{
    (var visited, var neighbours) = (new HashSet<Complex>(), new HashSet<(Complex,Complex)>());
    var queue = new Queue<Complex>([key]);
    while (queue.TryDequeue(out Complex curr))
    {
        if (!visited.Add(curr))
            continue;

        dirs.Select(dir => curr + dir)
            .Where(n => grid.ContainsKey(n) && grid[n] == grid[curr])
            .ToList().ForEach(queue.Enqueue);

        foreach (var neighbour in dirs.Select(dir => curr + dir).Where(n => !grid.ContainsKey(n) || grid[n] != grid[curr]))
        {
            var wall = new[] { curr, neighbour }.OrderBy(c => c.Real).ThenBy(c => c.Imaginary).ToArray();
            neighbours.Add((wall[0], wall[1]));
        }
    }

    var sides =     count(neighbours, grid[key], c => c.Imaginary, c => c.Real) 
                +   count(neighbours, grid[key], c => c.Real, c => c.Imaginary);

    regions.Add((neighbours.Count, sides, visited));
}

Complex innerSide((Complex c1, Complex c2) wall, char plant) => !grid.ContainsKey(wall.c1) || grid[wall.c1] != plant ? wall.c2 : wall.c1;
int count(HashSet<(Complex p1, Complex p2)> neighbours, char plant, Func<Complex, double> first, Func<Complex, double> second)
    => neighbours.Where(wall => first(wall.p1) == first(wall.p2))
    .GroupBy(wall => second(wall.p1))
    .Select(grp => grp.OrderBy(wall => first(wall.p1)).ToArray())
    .Sum(set => set.Aggregate(
        new Acc(set[0], second(innerSide(set[0], plant)), 1),
        (acc, curr) => new Acc(curr, second(innerSide(curr, plant)),
            (Math.Abs(first(curr.p1) - first(acc.prev.p1)) > 1) || (acc.inside != second(innerSide(curr, plant)))
                ? acc.total + 1 : acc.total),
        acc => acc.total));

var part1 = regions.Sum(tp => tp.perimeter * tp.points.Count);
Console.WriteLine($"Part 1: {part1}");
var part2 = regions.Sum(tp => tp.sides * tp.points.Count);
Console.WriteLine($"Part 2: {part2}");

record Acc((Complex p1, Complex p2) prev, Complex inside,int total);
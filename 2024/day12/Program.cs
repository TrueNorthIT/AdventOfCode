using System.Numerics;

var dirs = new Complex[] { new(1, 0), new(0, -1), new(-1, 0), new(0, 1) };
var grid = File.ReadAllLines("input.txt")
    .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
    .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var regions = new List<(int perimeter, int sides, HashSet<Complex> points)>();
foreach (var key in grid.Keys.Where(key => !regions.Any(region => region.points.Contains(key))))
{
    (var visited, var walls) = (new HashSet<Complex>(), new List<(Complex p1,Complex p2)>());
    var queue = new Queue<Complex>([key]);
    while (queue.TryDequeue(out Complex curr))
    {
        if (!visited.Add(curr))
            continue;

        foreach (var n in from dir in dirs select curr + dir)
        {
            if (grid.ContainsKey(n) && grid[n] == grid[curr])
                queue.Enqueue(n);
            if (!grid.ContainsKey(n) || grid[n] != grid[curr])
                walls.Add(sort(curr, n));
        }
    }
    int count = walls.Where(wall => wall.p1.Real == wall.p2.Real)
        .GroupBy(wall => wall.p1.Imaginary)
        .Select(grp => grp.OrderBy(wall => wall.p1.Real))
        .Sum(set => set.Aggregate(
            (set.First(), inner(set.First(), grid[key]).Imaginary, 1),
            (acc, curr) => 
                (acc, inner(curr, grid[key]).Imaginary) is ((var prev, var pi, var total), var i)
                    ? (curr, i, (Math.Abs(curr.p1.Real - acc.Item1.p1.Real) > 1) || pi != i 
                        ? total + 1 : total) 
                : default,
            acc => acc.Item3));

    regions.Add((walls.Count, 2 * count, visited));
}

Complex inner((Complex c1, Complex c2) wall, char plant) 
    => !grid.ContainsKey(wall.c1) || grid[wall.c1] != plant ? wall.c2 : wall.c1;

(Complex, Complex) sort(Complex c1, Complex c2) 
    => c1.Real <= c2.Real ? c1.Imaginary < c2.Imaginary ? (c1, c2) : (c2, c1) : (c1, c2);

Console.WriteLine($"Part 1: {regions.Sum(tp => tp.perimeter * tp.points.Count)}");
Console.WriteLine($"Part 2: {regions.Sum(tp => tp.sides * tp.points.Count)}");
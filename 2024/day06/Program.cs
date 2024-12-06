using System.Numerics;

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var start = grid.Where(kvp => kvp.Value == '^').Single().Key;

var guardsRoute = solve(null);
Console.WriteLine($"Part 1: {guardsRoute.Count()}");

var part2 = guardsRoute.Where(position => position != start)
                .AsParallel()
                .Count(obstacle => solve(obstacle) == null);

Console.WriteLine($"Part 2: {part2}");

List<Complex> solve(Complex? obstacle)
{
    var visited = new HashSet<(Complex position, Complex direction)>();
    (Complex position, Complex direction) current = (start, new (-1,0));
    while (visited.Add(current))
    {
        var next = current.position + current.direction;
        if (!grid.ContainsKey(next))
            return visited.Select(tp => tp.position).Distinct().ToList();

        current = next == obstacle  || grid[next] == '#'
                    ? (current.position, current.direction * new Complex(0,-1))
                    : (next, current.direction);
    }
    return null;
}

using System.Numerics;

Complex[] dirs = { new(-1, 0), new(0, 1), new(1, 0), new(0, -1) };

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var start = grid.Where(kvp => kvp.Value == '^').Single().Key;

var guardsRoute = solve(new Complex(-1,-1));
Console.WriteLine($"Part 1: {guardsRoute.Count()}");

var part2 = guardsRoute.Where(position => position != start)
                .AsParallel()
                .Count(obstacle => solve(obstacle) == null);

Console.WriteLine($"Part 2: {part2}");

List<Complex> solve(Complex obstacle)
{
    var visited = new HashSet<(Complex position, int direction)>();
    (Complex position, int direction) current = (start, 0);
    while (visited.Add(current))
    {
        var next = current.position + dirs[current.direction];
        if (!grid.ContainsKey(next))
            return visited.Select(tp => tp.position).Distinct().ToList();

        current = next == obstacle  || grid[next] == '#'
                    ? (current.position, (current.direction + 1) % 4)
                    : (next, current.direction);
    }
    return null;
}

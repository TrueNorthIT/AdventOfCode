using System.Numerics;

const int take = 1024;
const int X = 70;
const int Y = 70;

var fullGrid = File.ReadAllText("input.txt").Split("\r\n")
        .Select((line, r) => {
            var sp = line.Split(",").Select(int.Parse).ToArray();
            return (new Complex(sp[0], sp[1]), r);
        }).ToList();

var end = new Complex(X, Y);

var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) }; //E, S, W, N

var grid = fullGrid.Take(take).ToDictionary();
var part1 = solve();
Console.WriteLine($"Part 1: {part1}");

for (int t = take; t < int.MaxValue; t++)
{
    grid = fullGrid.Take(t).ToDictionary();
    var p1 = solve();
    if (p1 == -1)
    {
        Console.WriteLine($"Part 2: {fullGrid.Skip(t-1).First()}");
        break;
    }

}

int solve()
{
    var queue = new Queue<(Complex, int)>();
    queue.Enqueue((new Complex(0, 0), 0));
    var visited = new HashSet<Complex>();
    while (queue.TryDequeue(out (Complex position, int steps) curr))
    {
        if (visited.Contains(curr.position))
            continue;

        if (curr.position == end)
            return curr.steps;

        visited.Add(curr.position);

        foreach (var next in dirs.Select(dir => curr.position + dir))
        {            
            if (!grid.ContainsKey(next) && inBounds(next))
                queue.Enqueue((next, curr.steps + 1));
        }
    }

    return -1;
}

bool inBounds(Complex point) => (point.Real, point.Imaginary) switch {
    (>= 0 and <= X, >=0 and <= Y) => true,
    _ => false,
};
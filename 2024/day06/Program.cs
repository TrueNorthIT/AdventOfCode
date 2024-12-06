    using System.Numerics;

    Complex[] dirs = { new(-1, 0), new(0, 1), new(1, 0), new(0, -1) };

    var grid = File.ReadAllLines("input.txt")
                .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
                .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

    var part1 = solve(grid).Select(tp => tp.position).Distinct().Count();
    Console.WriteLine($"Part 1: {part1}");

    int part2 = 0;
    Parallel.ForEach(grid.Where(kvp => kvp.Value == '.').Select(kvp => kvp.Key), obstacle =>
    {
        var newGrid = grid.ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
        newGrid[obstacle] = '#';
        if (solve(newGrid) == null) Interlocked.Increment(ref part2);
    });
    Console.WriteLine($"Part 2: {part2}");

    HashSet<(Complex position,int direction)> solve(Dictionary<Complex, char> grid)
    {
        var R = grid.Keys.Max(tp => tp.Real);
        var C = grid.Keys.Max(tp => tp.Imaginary);

        var start = grid.Where(kvp => kvp.Value == '^').Single().Key;

        var visited = new HashSet<(Complex, int)>();
        (Complex position, int direction) current = (start, 0);
        while (visited.Add(current))
        {
            while (true)
            {
                Complex next = current.position + dirs[current.direction];
                if (!grid.ContainsKey(next))
                    return visited;

                if (grid[next] == '#')
                {
                    current = (current.position, (current.direction + 1) % 4);
                }
                else
                {
                    current = (next, current.direction);
                    break;
                }
            }
        }
        return null;
    }

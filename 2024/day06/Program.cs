using System.Diagnostics;
using System.Numerics;

    var grid = File.ReadAllLines("input.txt").Select(line => line.ToArray()).ToArray();
    (int sr, int sc, char _) = grid.SelectMany((str, r) => str.Select((ch, c) => (r, c, ch))).Single(tp => tp.ch == '^');
    grid[sr][sc] = '.';

    (int or, int oc) [] dirs = { (-1, 0), (0, 1), (1, 0), (0, -1) };

    Stopwatch watch = new Stopwatch();
    watch.Start();
    var guardsRoute = solve(grid, (-1,-1)).DistinctBy(tp => tp.position);
    Console.WriteLine($"Part 1: {guardsRoute.Count()} in {watch.ElapsedMilliseconds}ms");

    watch.Restart();
    int part2 = 0;
    Parallel.ForEach(guardsRoute, new ParallelOptions { MaxDegreeOfParallelism = 16 }, obstacle =>
    {
        if (obstacle.position == (sr, sc)) return;
        var solution = solve(grid, obstacle.position);
        if (solution == null)
        {
            Console.WriteLine($"Obstacle at {obstacle.position} resulted in loop");
            Interlocked.Increment(ref part2);
        }
        else
        {
            Console.WriteLine($"Obstacle at {obstacle.position} left room and covered {solution.Count} spaces");
        }
    });
    Console.WriteLine($"Part 2: {part2} in {watch.ElapsedMilliseconds}ms");

    HashSet<((int r, int c) position,int direction)> solve(char[][] grid, (int r, int c) obstacle)
    {
        var visited = new HashSet<((int r, int c) position, int direction)>();
        ((int r, int c) position, int direction) current = ((sr,sc), 0);
        while (visited.Add(current))
        {
            (int r, int c) next = (current.position.r + dirs[current.direction].or, current.position.c + dirs[current.direction].oc);
            if (next.r < 0 || next.r >= grid.Length || next.c < 0 || next.c >= grid[0].Length)
                return visited;

            current = grid[next.r][next.c] == '#' || next == obstacle 
                ? (current.position, (current.direction + 1) % 4)
                : (next, current.direction);
        }
        return null;
    }

using System.Diagnostics;
using System.Numerics;

namespace day06
{
    internal class Program
    {
        static Complex[] dirs = { new(-1, 0), new(0, 1), new(1, 0), new(0, -1) };
        static void Main(string[] args)
        {
            Stopwatch watch = new Stopwatch();
            watch.Start();
            var grid = File.ReadAllLines("input.txt")
                        .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
                        .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

            var part1 = solve(grid).Select(tp => tp.Item1).Distinct().Count();
            Console.WriteLine($"Part 1: {part1} in {watch.ElapsedMilliseconds}ms");
            watch.Restart();

            int part2 = 0;
            Parallel.ForEach(grid.Where(kvp => kvp.Value == '.').Select(kvp => kvp.Key), obstacle =>
            {
                var newGrid = grid.ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
                newGrid[obstacle] = '#';
                if (solve(newGrid) == null)
                {
                    Interlocked.Increment(ref part2);
                }
            });
            Console.WriteLine($"Part 2: {part2} in {watch.ElapsedMilliseconds}ms");
        }

        public static HashSet<(Complex,int)> solve(Dictionary<Complex, char> grid)
        {
            var R = grid.Keys.Max(tp => tp.Real);
            var C = grid.Keys.Max(tp => tp.Imaginary);

            var start = grid.Where(kvp => kvp.Value == '^').Single().Key;

            var visited = new HashSet<(Complex, int)>();
            (Complex position, int direction) current = (start, 0);
            visited.Add(current);
            while (true)
            {
                while (true)
                {
                    Complex next = current.position + dirs[current.direction];
                    if (!grid.ContainsKey(next))
                        goto escape;

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

                if (!visited.Add(current))
                {
                    return null;
                }
            }
        escape:;
            return visited;
        }
    }
}

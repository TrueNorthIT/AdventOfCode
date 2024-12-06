using System.Numerics;

namespace day06
{
    internal class Program
    {
        static Complex[] dirs = { new(-1, 0), new(0, 1), new(1, 0), new(0, -1) };
        static void Main(string[] args)
        {
            var grid = File.ReadAllLines("input.txt")
                        .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
                        .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

            var part1 = solve(grid).Select(tp => tp.Item1).Distinct().Count();
            Console.WriteLine($"Part 1: {part1}");

            int part2 = 0;
            foreach (var obstacle in grid.Where(kvp => kvp.Value == '.').Select(kvp => kvp.Key))
            {
                grid[obstacle] = '#';
                if (solve(grid) == null)
                {
                    part2++;
                }
                grid[obstacle] = '.';
            }
            Console.WriteLine($"Part 2: {part2}");
        }

        public static HashSet<(Complex,int)> solve(Dictionary<Complex, char> grid)
        {
            var R = grid.Keys.Max(tp => tp.Real);
            var C = grid.Keys.Max(tp => tp.Imaginary);

            var start = grid.Where(kvp => kvp.Value == '^').Single().Key;
            int dir = 0;

            var visited = new HashSet<(Complex, int)>();
            var current = start;
            visited.Add((current, dir));
            while (true)
            {
                Complex next;
                while (true)
                {
                    next = current + dirs[dir];
                    if (!grid.ContainsKey(next))
                        goto escape;

                    if (grid[next] == '#')
                    {
                        dir = (dir + 1) % 4;
                    }
                    else
                    {
                        break;
                    }
                }

                if (visited.Contains((next, dir)))
                {
                    return null;
                }
                visited.Add((next,dir));
                current = next;
            }
        escape:;
            return visited;
        }
    }
}

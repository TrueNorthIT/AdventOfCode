using System.Numerics;
var nodes = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .GroupBy(tp => tp.ch)
            .ToDictionary(grp => grp.Key, grp => grp.Select(tp => new Complex(tp.r, tp.c)).ToArray());

int R = (int)nodes.SelectMany(kvp => kvp.Value).Max(tp => tp.Real);
int C = (int) nodes.SelectMany(kvp => kvp.Value).Max(tp => tp.Imaginary);
Func<Complex, bool> inGrid = tp => tp.Real >= 0 && tp.Real <= R && tp.Imaginary >= 0 && tp.Imaginary <= C;

(var part1, var part2) = (new HashSet<Complex>(), new HashSet<Complex>());
foreach (var (node,pair) in from n in nodes
                            where n.Key != '.'
                            from n1 in n.Value
                            from n2 in n.Value
                            where n1 != n2
                            select (n, (n1, n2)))
{
    //we don't consider points between the antenna, luckily we don't have to!
    var delta = pair.n2 - pair.n1;
    var solutions = new[] { pair.n1 + 2 * delta, pair.n2 - 2 * delta };
    foreach (var valid in solutions.Where(inGrid))
        part1.Add(valid);

    //don't have to reduce by the gcd, data is kind to us again!
    foreach (var dir in new[] { -1, 1 })
        foreach (var solution in Enumerable.Range(0, int.MaxValue).Select(i => pair.n1 + dir * i * delta))
            if (inGrid(solution))
                part2.Add(solution);
            else
                break;
}
Console.WriteLine($"Part 1: {part1.Count}");
Console.WriteLine($"Part 2: {part2.Count}");

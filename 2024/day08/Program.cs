using System.Numerics;
var nodes = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .GroupBy(tp => tp.ch)
            .ToDictionary(grp => grp.Key, grp => grp.Select(tp => new Complex(tp.r, tp.c)).ToArray());

int R = (int)nodes.SelectMany(kvp => kvp.Value).Max(tp => tp.Real);
int C = (int) nodes.SelectMany(kvp => kvp.Value).Max(tp => tp.Imaginary);
Func<Complex, bool> inGrid = tp => tp.Real >= 0 && tp.Real <= R && tp.Imaginary >= 0 && tp.Imaginary <= C;

nodes.Remove('.');
var antiNodes = new HashSet<Complex>();
var antiNodes2 = new HashSet<Complex>();
foreach (var node in nodes)
{
    foreach (var pair in from n1 in node.Value
                         from n2 in node.Value
                         where n1 != n2
                         select (n1, n2))
    {
        var delta = pair.n2 - pair.n1;
        var solutions = new[] { pair.n1 + 2 * delta, pair.n2 - 2 * delta };
        foreach (var valid in solutions.Where(inGrid))
        {
            antiNodes.Add(valid);
        }

        //now find GCD delta
        var gcd = BigInteger.GreatestCommonDivisor((BigInteger)delta.Real, (BigInteger)delta.Imaginary);
        var gcdDelta = new Complex((int) ((int) delta.Real / gcd), (int) ((int) delta.Imaginary / gcd));
        Action<bool> process = direction =>
        {
            foreach (var i in Enumerable.Range(0, int.MaxValue))
            {
                var solution = pair.n1 + (direction ? 1 : -1) * i * gcdDelta;
                if (inGrid(solution))
                    antiNodes2.Add(solution);
                else
                    break;
            }
        };
        process(false);
        process(true);
    }

}
Console.WriteLine($"Part 1: {antiNodes.Count}");
Console.WriteLine($"Part 2: {antiNodes2.Count}");

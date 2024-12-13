using System.Numerics;
using System.Text.RegularExpressions;

var machines = File.ReadAllText("input.txt").Split($"{Environment.NewLine}{Environment.NewLine}");
Console.WriteLine($"Part 1: {solve(new BigInteger(00000000000000))}");
Console.WriteLine($"Part 2: {solve(new BigInteger(10000000000000))}");

BigInteger solve(BigInteger offset)
{
    BigInteger prizes = 0;
    BigInteger tokens = 0;

    foreach (var machine in machines)
    {
        var machineRegex = new Regex(@"Button [AB]: X\+(\d+), Y\+(\d+)");
        var prizeRegex = new Regex(@"Prize: X=(\d+), Y=(\d+)");

        var arr = machine.Split($"{Environment.NewLine}");
        var m1 = machineRegex.Match(arr[0]);
        var m2 = machineRegex.Match(arr[1]);
        var mp = prizeRegex.Match(arr[2]);

        var (x1, y1) = (BigInteger.Parse(m1.Groups[1].Value),
                        BigInteger.Parse(m1.Groups[2].Value));

        var (x2, y2) = (BigInteger.Parse(m2.Groups[1].Value), 
                        BigInteger.Parse(m2.Groups[2].Value));

        var (xp, yp) = (offset + BigInteger.Parse(mp.Groups[1].Value), offset + BigInteger.Parse(mp.Groups[2].Value));

        var (nom, den) = (yp * x2 - xp * y2, y1 * x2 - x1 * y2);
        var a = nom / den;
        var bx2 = xp - a * x1;

        if (nom % den == 0 && bx2 % x2 == 0)
            tokens += 3 * a + (bx2 / x2);
    }
    return tokens;
}
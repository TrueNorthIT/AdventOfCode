using System.Numerics;
using System.Text.RegularExpressions;

var machines = File.ReadAllText("input.txt").Split($"{Environment.NewLine}{Environment.NewLine}");

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
        var (x1, y1) = (BigInteger.Parse(m1.Groups[1].Value), BigInteger.Parse(m1.Groups[2].Value));
        var (x2, y2) = (BigInteger.Parse(m2.Groups[1].Value), BigInteger.Parse(m2.Groups[2].Value));
        var (xp, yp) = (offset + BigInteger.Parse(mp.Groups[1].Value), offset + BigInteger.Parse(mp.Groups[2].Value));

        //na * x1 + nb * x2 = xp
        //na * y1 + nb * y2 = yp
        //na * y1 + (xp - na * x1) * y2 / x2 = yp
        //na ( y1 - x1.y2/x2) = yp - xp . y2 / x2
        //na = (yp - xp . y2 / x2) / ( y1 - x1.y2/x2)
        //na = (yp . x2 - xp . y2) / ( y1 . x2 - x1.y2)
        var nom = yp * x2 - xp * y2;
        var den = y1 * x2 - x1 * y2;
        if (nom % den == 0)
        {
            var a = nom / den;
            var b = xp - a * x1;
            if (b % x2 == 0)
            {
                b = b / x2;
                prizes++;
                tokens += 3 * a + b;
            }
        }
    }
    return tokens;
}

Console.WriteLine($"Part 1: {solve(new BigInteger(00000000000000))}");
Console.WriteLine($"Part 2: {solve(new BigInteger(10000000000000))}");

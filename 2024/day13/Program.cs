    using System.Numerics;
    Console.WriteLine((solve(0), solve((long)1E13)));

    long solve(long offset) => File.ReadAllText("input.txt").Split("\r\n\r\n")
    .Sum(machine => machine.Split("\r\n").SelectMany(
        line => new string(line.Where(ch => Char.IsDigit(ch) || ch == ' ').ToArray())
            .Split(" ", StringSplitOptions.RemoveEmptyEntries)
            .Select(str => BigRational.Parse(str))).ToArray() 
                is [var xa, var ya, var xb, var yb, var xp, var yp]
                ? ((yp + offset) * xb - (xp + offset) * yb) / (ya * xb - xa * yb) is var a 
                && ((xp + offset) - a * xa) / xb is var b
                && new[] { a, b }.All(BigRational.IsInteger) 
            ? (long) (3 * a + b) : 0 : 0);
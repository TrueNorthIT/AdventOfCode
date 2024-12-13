    using System.Numerics;
    new [] { 0, (long) 1E13 }.Select(
        offset => File.ReadAllText("input.txt").Split("\r\n\r\n")
            .Sum(machine => machine.Split("\r\n").SelectMany(
                line => string.Concat(line.Where(ch => char.IsDigit(ch) || ch == ' '))
                    .Split(" ", StringSplitOptions.RemoveEmptyEntries)
                    .Select(str => BigRational.Parse(str))).ToList()
                is [var xa, var ya, var xb, var yb, var xp, var yp]
                    ? (xp + offset, yp + offset) is (var xpo, var ypo)
                    ? ((ypo * xb - xpo * yb) / (ya * xb - xa * yb)) is var a
                    ? ((xpo - a * xa) / xb) is var b
                    ? new[] { a, b }.All(BigRational.IsInteger)
                    ? (long)(3 * a + b) : 0 : 0 : 0 : 0 : 0))
    .ToList().ForEach(Console.WriteLine);
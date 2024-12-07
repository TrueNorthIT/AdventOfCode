(long target, long[] ops)[] equations = File.ReadAllLines("input.txt")
    .Select(str => str.Split(':'))
    .Select(sp => ( long.Parse(sp[0]),
                    sp[1].Trim().Split(' ').Select(long.Parse).ToArray())
    ).ToArray();

var solve = (bool part2) => equations.AsParallel()
        .Where(equation => possible(equation, equation.ops[0], 1, part2))
        .Sum(eq => eq.target);

Console.WriteLine($"Part 1: {solve(false)}");
Console.WriteLine($"Part 2: {solve(true)}");

static bool possible((long target, long[] ops) equation, long currentTotal, int index, bool part2) => 
    index >= equation.ops.Length 
    ? equation.target == currentTotal
    :   possible(equation, currentTotal + equation.ops[index], index + 1, part2)
        || possible(equation, currentTotal * equation.ops[index], index + 1, part2)
        || (part2 ? possible(equation, concat(currentTotal, equation.ops[index]), index + 1, true) : false);

static long concat(long a, long b) =>  a * (long)Math.Pow(10, Math.Ceiling(Math.Log(b + 1, 10))) + b;
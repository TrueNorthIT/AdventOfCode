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

    bool possible((long target, long[] ops) equation, long total, int i, bool p2) => 
        i >= equation.ops.Length 
        ? equation.target == total
        :   possible(equation, total + equation.ops[i], i + 1, p2)
            || possible(equation, total * equation.ops[i], i + 1, p2)
            || (p2 ? possible(equation, concat(total, equation.ops[i]), i + 1, true) : false);

    long concat(long a, long b) =>  a * (long)Math.Pow(10, Math.Ceiling(Math.Log(b + 1, 10))) + b;
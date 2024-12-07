var equations = File.ReadAllLines("input.txt").Select(str => { var sp = str.Split(':'); 
        return (long.Parse(sp[0]), sp[1].Trim().Split(' ').Select(long.Parse).ToList()); 
}).ToArray();

(var part1, var part2) = (0L, 0L);
foreach ((long target, List<long> operands) in equations)
{
    if (totalWays(target, operands.First(), operands.Skip(1).ToList(), false) > 0) part1 += target;
    if (totalWays(target, operands.First(), operands.Skip(1).ToList(), true) > 0) part2 += target;
}

Console.WriteLine($"Part 1: {part1}");
Console.WriteLine($"Part 2: {part2}");

static int totalWays(long target, long currentTotal, List<long> numbers, bool part2) => 
!numbers.Any() ? target == currentTotal ? 1 : 0
    :   totalWays(target, currentTotal * numbers.First(), numbers.Skip(1).ToList(), part2)
        + totalWays(target, currentTotal + numbers.First(), numbers.Skip(1).ToList(), part2)
        + (part2 ? totalWays(target, long.Parse($"{currentTotal}{numbers.First()}"), numbers.Skip(1).ToList(), part2) : 0);

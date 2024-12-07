namespace day07
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var equations = File.ReadAllLines("input.txt").Select(str => 
                { var sp = str.Split(':'); return (long.Parse(sp[0]), sp[1].Trim().Split(' ').Select(long.Parse).ToList()); }).ToArray();

            var part1 = 0L;
            var part2 = 0L;
            foreach ((long target, List<long> operands) in equations)
            {
                var res1 = totalWays(target, operands.First(), operands.Skip(1).ToList(), false);
                if (res1 > 0) part1 += target;
                var res2 = totalWays(target, operands.First(), operands.Skip(1).ToList(), true);
                if (res2 > 0) part2 += target;
            }
        }
        static int totalWays(long target, long currentTotal, List<long> numbers, bool part2)
        {
            if (!numbers.Any())
            {
                return target == currentTotal ? 1 : 0;
            }
            return totalWays(target, currentTotal * numbers.First(), numbers.Skip(1).ToList(), part2)
                + totalWays(target, currentTotal + numbers.First(), numbers.Skip(1).ToList(), part2)
                + (part2 ? totalWays(target, long.Parse($"{currentTotal}{numbers.First()}"), numbers.Skip(1).ToList(), part2) : 0);
        }
    }
}

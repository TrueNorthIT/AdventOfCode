namespace day05
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var file = File.ReadAllText("input.txt").Split($"{Environment.NewLine}{Environment.NewLine}");
            var rules = file[0].Split(Environment.NewLine).Select(rule => { var sp = rule.Split("|"); return (int.Parse(sp[0]), int.Parse(sp[1])); }).ToArray();
            var updates = file[1].Split(Environment.NewLine).Select(update => update.Split(",").Select(int.Parse).ToArray()).ToArray();

            var nodes = updates.SelectMany(arr => arr).Distinct();
            Console.WriteLine($"Distinct nodes : {nodes}");

            int part1 = 0; int part2 = 0;
            foreach (var update in updates)
            {
                bool failed = true;
            runagain:;
                for (int i = 1; i < update.Length; i++)
                {
                    //is there a rule that causes update[i] to have to be before update[i-1]
                    if (rules.Any(tp => tp.Item1 == update[i] && tp.Item2 == update[i - 1]))
                    {
                        //this isn't a possible ordering
                        //these two should be the other way, so swap
                        //we need to swap these two values
                        failed = false;
                        var tmp = update[i - 1];
                        update[i - 1] = update[i];
                        update[i] = tmp;
                        goto runagain;
                    }
                }
                //this is a positive order
                if (failed)
                {
                    part1 += update[update.Length / 2];
                }
                else
                {
                    part2 += update[update.Length / 2];
                }
            }
            Console.WriteLine($"Part 1: {part1}");
            Console.WriteLine($"Part 2: {part2}");
        }

    }
}

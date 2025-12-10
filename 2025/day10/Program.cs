using System.Numerics;

namespace day10
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var parts = File.ReadAllLines("input.txt").Select(l => l.Split(" ").Select(p => p.Substring(1, p.Length-2))).ToArray();
            var targets = parts.Select(p => { 
                var hashesStr = p.First();
                int total = 0;
                for (var i = 0; i < hashesStr.Length; i++) { 
                    if (hashesStr[i] == '#') { total += 1 << i; } 
                }
                return total;
            }).ToArray();
            var switches = parts.Select(ps => ps.Skip(1).SkipLast(1).Select(p => {
                var switchParts = p.Split(",").Select(int.Parse);
                int switch_ = 0;
                foreach (var switchPart in switchParts)
                {
                    switch_ += 1 << switchPart;
                }
                return switch_;
            }).ToArray()).ToArray();
            var presses = new List<int>();
            for (var targetIndex = 0; targetIndex < targets.Length; targetIndex++)
            {
                var target = targets[targetIndex];
                presses.Add(GetPresses(target, switches[targetIndex]).Value);
                Console.WriteLine("Target {0}, switches {1}, presses {2}", target, string.Join(",", switches[targetIndex]), presses.Last());
            }
            Console.WriteLine(presses.Sum());
        }

        static int? GetPresses(int target, int[] switches, int startFrom = 0)
        {
            foreach (var s in switches)
            {
                var newVal = startFrom ^ s;
                if (newVal == target) return 1;
            }
            var possibilities = new List<int>();
            for (var sIndex1 = 0; sIndex1 < switches.Length; sIndex1++)
            {
                var newVal = startFrom ^ switches[sIndex1];
                var recurseVal = GetPresses(target, switches.Skip(sIndex1 + 1).ToArray(), newVal);
                if (recurseVal.HasValue) possibilities.Add(recurseVal.Value + 1);
            }
            if (possibilities.Any()) return possibilities.Min();
            return null;
        }
    }
}

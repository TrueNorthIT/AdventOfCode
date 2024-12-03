using System.Text.RegularExpressions;

namespace day03
{
    internal class Program
    {
        static void Main()
        {
            Console.WriteLine(Part2("input1.txt"));
        }

        static long Part2(string filename)
        {
            var findInstruc = new Regex(@"(?:mul\((?<num1>\d{1,3}),(?<num2>\d{1,3})\))|(?<do>do\(\))|(?<dont>don't\(\))");
            var enabled = true;
            long total = 0;
            foreach (var match in File.ReadAllLines(filename).SelectMany(s => findInstruc.Matches(s)))
            {
                if (match.Groups["do"].Value != string.Empty)
                {
                    enabled = true;
                }
                else if (match.Groups["dont"].Value != string.Empty)
                {
                    enabled = false;
                }
                else if (enabled)
                {
                    total += long.Parse(match.Groups[1].Value) * long.Parse(match.Groups[2].Value);
                }
            }
            return total;
        }

        static long Part1(string filename)
        {
            var findInstruc = new Regex(@"mul\((\d{1,3}),(\d{1,3})\)");
            return File.ReadAllLines(filename).SelectMany(s => findInstruc.Matches(s).Select(m => long.Parse(m.Groups[1].Value) * long.Parse(m.Groups[2].Value))).Sum();
        }
    }
}

using System.Text.RegularExpressions;

namespace Day03
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var line = File.ReadAllText("input.txt");

            Console.WriteLine($"Part 1: {part1(line)}");

            bool enabled = true;
            int part2 = 0;
            string remainder = line;
            while (remainder != null)
            {
                if (enabled)
                {
                    (remainder, int score) = processDoSegment(remainder);
                    part2 += score;
                    enabled = false;
                }
                else
                {
                    remainder = processDontSegment(remainder);
                    enabled = true;
                }
            }

            Console.WriteLine($"Part 2: {part2}");
        }

        static int part1(string segment)
        {
            Regex regex = new Regex(@"(mul\((\d{1,3}),(\d{1,3})\))");
            var matches = regex.Matches(segment);

            int total = 0;
            foreach (Match match in matches)
            {
                total += int.Parse(match.Groups[2].Value) * int.Parse(match.Groups[3].Value);
            }
            return total;
        }

        private static (string remainder, int score) processDoSegment(string segment)
        {
            var indexOfDont = segment.IndexOf("don't()");
            if (indexOfDont == -1)
            {
                return (null, part1(segment));
            }
            var doSeg = segment[0..(indexOfDont - 1 + 7)];
            return (segment[indexOfDont..], part1(doSeg));
        }
        private static string processDontSegment(string segment)
        {
            var indexOfDo = segment.IndexOf("do()");
            if (indexOfDo == -1)
            {
                return null;
            }            
            return segment[(indexOfDo+4)..];
        }
    }
}

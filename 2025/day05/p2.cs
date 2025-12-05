using System;
using System.Collections.Frozen;
using System.Collections.Generic;
using System.IO;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //string[] lines = File.ReadAllLines("C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\demo.txt");
            string[] lines = File.ReadAllLines("C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\input.txt");

            List<(long start, long end)> ranges = new List<(long start, long end)>();
            List<long> ids = new List<long>();

            long freshCount = 0;

            foreach (string line in lines)
            {
                if (line.Contains("-") )
                {
                    ranges.Add((long.Parse(line.Split('-')[0]), long.Parse(line.Split('-')[1])));
                }
                else if (line == "")
                {
                    continue;
                }
                else
                {
                    ids.Add(long.Parse(line));
                }
            }

            Console.WriteLine($"Total Ranges: {ranges.Count}");
            Console.WriteLine($"Total IDs: {ids.Count}");


            var sortedRanges = ranges.OrderBy(r => r.start).ToList();

            long currentEnd = 0;
            long currentStart = 0;

            foreach (var range in sortedRanges)
            {
                if (range.start <= currentEnd + 1)
                {
                    currentEnd = Math.Max(currentEnd, range.end);
                }
                else
                {
                    freshCount += (currentEnd - currentStart + 1);
                    currentStart = range.start;
                    currentEnd = range.end;
                }
            }

            freshCount += (currentEnd - currentStart);

            Console.WriteLine($"Total Fresh IDs: {freshCount}");

        }
    }
}
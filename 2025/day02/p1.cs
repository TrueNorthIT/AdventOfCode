using System;
using System.Collections.Generic;
using System.IO;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {

            List<string> input = new List<string>();
            FileStream fs = new FileStream("C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\input.txt", FileMode.Open, FileAccess.Read);
            //FileStream fs = new FileStream("C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\demo.txt", FileMode.Open, FileAccess.Read);

            StreamReader streamReader = new StreamReader(fs);

            while (!streamReader.EndOfStream)
            {
                input.Add(streamReader.ReadLine());
            }

            Console.WriteLine($"Read {input.Count} lines");

            List<String> ranges = new List<string>();

            long idSum = 0;

            foreach (var line in input)
            {
                foreach (var range in line.Split(','))
                {
                    ranges.Add(range);
                    Console.WriteLine(range);
                }
            }

            Console.WriteLine($"Parsed {ranges.Count} ranges");

            foreach (var range in ranges)
            {
                Console.WriteLine($"Working on range: {range}");
                var bounds = range.Split('-');
                long lower = Int64.Parse(bounds[0]);
                long upper = Int64.Parse(bounds[1]);
                Console.WriteLine($"Range: {lower} to {upper}");

                for (long i = lower; i <= upper; i++)
                {
                    Console.WriteLine($"Checking number: {i}");

                    if (i.ToString().ToCharArray().Length % 2 != 0)
                    {
                        Console.WriteLine($"Number {i} has an odd number of digits, skipping");
                        continue;
                    }
                    int midpoint = i.ToString().ToCharArray().Length / 2;

                    string firstHalf = i.ToString().Substring(0, midpoint);
                    string secondHalf = i.ToString().Substring(midpoint);
                    Console.WriteLine($"First half: {firstHalf}, Second half: {secondHalf}");
                    if (firstHalf == secondHalf)
                    {
                        Console.WriteLine($"Number {i} has duplicate parts!");
                        idSum += i;

                    }
                }
            }

            Console.WriteLine($"Sum of all IDs with duplicate parts: {idSum}");
        }
    }
}
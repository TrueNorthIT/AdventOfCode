using System;
using System.Collections.Generic;
using System.IO;
using System.Text; // Added for StringBuilder

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
                }
            }

            Console.WriteLine($"Parsed {ranges.Count} ranges");

            foreach (var range in ranges)
            {
                var bounds = range.Split('-');
                long lower = Int64.Parse(bounds[0]);
                long upper = Int64.Parse(bounds[1]);

                for (long i = lower; i <= upper; i++)
                {
                    if (IsMadeOfRepeatingSequence(i.ToString()))
                    {
                        Console.WriteLine($"Found invalid ID: {i}");
                        idSum += i;
                    }
                }
            }

            Console.WriteLine($"Sum of all IDs with duplicate parts: {idSum}");
        }

        static bool IsMadeOfRepeatingSequence(string numStr)
        {
            int len = numStr.Length;

            for (int patternLen = 1; patternLen <= len / 2; patternLen++)
            {
                if (len % patternLen != 0)
                {
                    continue;
                }

                string pattern = numStr.Substring(0, patternLen);
                StringBuilder builder = new StringBuilder();

                int repetitions = len / patternLen;
                for (int k = 0; k < repetitions; k++)
                {
                    builder.Append(pattern);
                    Console.WriteLine($"Building comparison: {builder.ToString()}");
                }

                if (builder.ToString() == numStr)
                {
                    Console.WriteLine($"Number {numStr} is made of repeating sequence: {pattern}");
                    return true;
                }
            }

            return false;
        }
    }
}
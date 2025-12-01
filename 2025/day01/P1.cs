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

            int dial = 50;
            int zeroCount = 0;

            foreach (var line in input)
            {
                Console.WriteLine($"Processing line: {line}");

                int number = int.Parse(line.Substring(1));

                if (line[0] == 'R')
                {
                    dial += number;
                    Console.WriteLine($"Adding {number}");
                }
                else if (line[0] == 'L')
                {
                    dial -= number;
                    Console.WriteLine($"Subtracting {number}");
                }

                dial = (dial + 100) % 100;

                if (dial == 0)
                {
                    zeroCount++;
                }

                Console.WriteLine($"Dial: {dial}");
            }

            Console.WriteLine($"Zero Count: {zeroCount}");
        }
    }
}
using System;
using System.Collections.Generic;
using System.IO;
using System.Numerics;
using System.Text;

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

            int totalOutput = 0;

            foreach (var line in input)
            {
                Vector2 num1 = new Vector2 (0,0);
                Vector2 num2 = new Vector2(0, 0);
                float current = 0;

                for (int i = 0; i < line.Length; i++)
                {
                    current = float.Parse(line[i].ToString());
                    if (current > num1.X && i != line.Length - 1)
                    {
                        num1.X = current;
                        num1.Y = i;
                        num2 = new Vector2(0, 0);
                    }
                    else if (current > num2.X && i > num1.Y)
                    {
                        num2.X = current;
                        num2.Y = i;
                    }
                }
                Console.WriteLine($"Line: {line} Max1: {num1.X} at pos {num1.Y} Max2: {num2.X} at {num2.Y} combo: {num1.X}{num2.X}");
                totalOutput += int.Parse($"{num1.X}{num2.X}");
            }

            Console.WriteLine($"Total Output: {totalOutput}");
        }
    }
}
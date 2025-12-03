using System;
using System.Collections.Generic;
using System.IO;
using System.Numerics; // Needed for Vector2 and BigInteger
using System.Text;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            List<string> input = new List<string>();

            string filePath = "C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\input.txt";
            //string filePath = "C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\demo.txt";

            using (StreamReader streamReader = new StreamReader(filePath))
            {
                while (!streamReader.EndOfStream)
                {
                    string line = streamReader.ReadLine();
                    if (!string.IsNullOrWhiteSpace(line))
                    {
                        input.Add(line);
                    }
                }
            }

            Console.WriteLine($"Read {input.Count} lines");

            long totalOutput = 0;

            foreach (var line in input)
            {
                StringBuilder sb = new StringBuilder();
                int lastIndexFound = -1;

                for (int i = 0; i < 12; i++)
                {
                    int remainingNeeded = 11 - i;

                    int maxSearchIndex = line.Length - 1 - remainingNeeded;

                    Vector2 bestCandidate = new Vector2(-1, -1);

                    for (int k = lastIndexFound + 1; k <= maxSearchIndex; k++)
                    {
                        float currentVal = float.Parse(line[k].ToString());

                        if (currentVal > bestCandidate.X)
                        {
                            bestCandidate = new Vector2(currentVal, k);
                            if (currentVal == 9) break;
                        }
                    }

                    sb.Append(bestCandidate.X);

                    lastIndexFound = (int)bestCandidate.Y;
                }

                long lineValue = long.Parse(sb.ToString());
                totalOutput += lineValue;
            }

            Console.WriteLine($"Total Output: {totalOutput}");
        }
    }
}
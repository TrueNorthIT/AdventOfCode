using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace MyApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //string[] lines = File.ReadAllLines("C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\demo.txt");
            string[] lines = File.ReadAllLines("C:\\Users\\RichardKelsey\\source\\repos\\Aoc\\Aoc\\input.txt");

            List<List<string>> grid = new List<List<string>>();

            foreach (var line in lines)
            {
                var tokens = line.Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries).ToList();

                if (tokens.Count > 0)
                {
                    grid.Add(tokens);
                }
            }

            List<string> operatorRow = grid.Last();
            int numberOfProblems = operatorRow.Count;

            long finalTotal = 0;

            Console.WriteLine($"Found {numberOfProblems} problems");

            for (int col = 0; col < numberOfProblems; col++)
            {
                string op = operatorRow[col];
                long currentResult = 0;

                if (op == "+")
                {
                    currentResult = 0;
                }
                else if (op == "*")
                {
                    currentResult = 1;
                }

                for (int row = 0; row < grid.Count - 1; row++)
                {
                    if (col < grid[row].Count)
                    {
                        string numberStr = grid[row][col];
                        if (long.TryParse(numberStr, out long number))
                        {
                            if (op == "+")
                            {
                                currentResult += number;
                            }
                            else if (op == "*")
                            {
                                currentResult *= number;
                            }
                        }
                    }
                }

                Console.WriteLine($"Problem {col + 1} ({op}): Result = {currentResult}");
                finalTotal += currentResult;
            }

            Console.WriteLine($"Total: {finalTotal}");
        }
    }
}
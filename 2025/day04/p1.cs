using System;
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

            int rows = lines.Length;
            int columns = lines[0].Length;
            int total = 0;

            string[,] input = new string[rows, columns];

            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < columns; c++)
                {
                    input[r, c] = lines[r][c].ToString();
                    Console.Write(input[r, c]);
                }
                Console.WriteLine();
            }

            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < columns; c++)
                {
                    if (input[r, c] == "@")
                    {
                        int neighborCount = 0;
                        Console.WriteLine($"Checking cell: ({r}, {c})");
                        for (int dr = -1; dr <= 1; dr++)
                        {
                            for (int dc = -1; dc <= 1; dc++)
                            {
                                if (dr == 0 && dc == 0)
                                    continue;
                                int newRow = r + dr;
                                int newCol = c + dc;
                                if (newRow >= 0 && newRow < rows && newCol >= 0 && newCol < columns)
                                {
                                    Console.WriteLine($"Surrounding cell: ({newRow}, {newCol}) = {input[newRow, newCol]}");
                                    if (input[newRow, newCol] == "@") neighborCount++;
                                }
                            }
                        }

                        if(neighborCount < 4) total++;
                    }
                }
            }

            Console.WriteLine($"Total: {total}");

        }
    }
}
﻿using System.Numerics;

var grid = File.ReadAllLines("input.txt")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

Complex[][] xOffsets = [
    [ new (-1,-1), new (0, 0), new (1, 1) ],
    [ new (-1, 1), new (0, 0), new (1,-1) ],
];

var offsets = from or in new [] { -1, 0, 1 }
            from oc in new [] { -1, 0, 1 }
            where !(or == 0 && oc == 0)
            select (from i in Enumerable.Range(0, 4) select new Complex(or * i, oc * i)).ToArray();

var part1 = grid.SelectMany(kvp => 
                offsets.Where(line => Enumerable.Range(0, 4).All(i => 
                    "XMAS"[i] == grid.GetValueOrDefault(kvp.Key + line[i]))))
            .Count();

var part2 = grid.Where(kvp => 
                    (   from arr in xOffsets
                        from tp in arr
                        select string.Concat(arr.Select(tp => grid.GetValueOrDefault(tp + kvp.Key, '.')))
                    ).All(str => str == "MAS" || str == "SAM"))
            .Count();

Console.WriteLine($"Part 1: {part1}");
Console.WriteLine($"Part 2: {part2}");
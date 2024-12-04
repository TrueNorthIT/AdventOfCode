var grid = File.ReadAllLines("input.txt").SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
        .ToDictionary(tp => (tp.r, tp.c), tp => tp.ch);

var Xs = new (int or, int oc)[][] {
    new [] { (-1,-1),(1,1) },
    new [] { (-1,1),(1,-1) },
};

var lines = from or in new[] { -1, 0, 1 }
            from oc in new[] { -1, 0, 1 }
            where !(or == 0 && oc == 0)
            select (    from i in Enumerable.Range(0, 4) select (or * i, oc * i))
            .ToArray<(int r, int c)>();

var part1 = grid.Where(kvp => kvp.Value == 'X')
    .Select(kvp => lines.Count(
        line => Enumerable.Range(0, 4)
                .Select(i => ("XMAS"[i], (kvp.Key.r + line[i].r, kvp.Key.c + line[i].c)))
                .All(tp => tp.Item1 == grid.GetValueOrDefault(tp.Item2, '.'))))
    .Sum();

var part2 = grid.Where(kvp => kvp.Value == 'A' 
                                && (    from arr in Xs
                                        from tp in arr
                                        select new String(
                                            arr.Select(tp => (tp.or + kvp.Key.r, tp.oc + kvp.Key.c))
                                            .Select(tp => grid.GetValueOrDefault(tp, '.')).ToArray())
                                    ).All(str => str == "MS" || str == "SM"))
            .Count();

Console.WriteLine($"Part 1: {part1}");
Console.WriteLine($"Part 2: {part2}");
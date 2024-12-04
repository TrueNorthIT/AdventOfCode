var grid = File.ReadAllLines("input.txt").SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
        .ToDictionary(tp => (tp.r, tp.c), tp => tp.ch);

Console.WriteLine(grid.Keys.Select( key => (grid.TryGetValue((key.r, key.c), out char first), first) switch
{
    (true, 'A') => (0,  new (int or, int oc)[][] {
                            new [] { (-1,-1),(1,1) },
                            new [] { (-1,1),(1,-1) },
                        }.Select(arr => new String(arr.Select(tp => (tp.or + key.r, tp.oc + key.c))
                                                    .Select(tp => grid.ContainsKey(tp) ? grid[tp] : '.').ToArray()))
                        .Count(str => str == "MS" || str == "SM")),
    (true, 'X') => ((   from or in new[] { -1, 0, 1 }
                        from oc in new[] { -1, 0, 1 }
                        where !(or == 0 && oc == 0)
                        select (from i in Enumerable.Range(0, 4)
                                select (or * i, oc * i))
                                .ToArray<(int r, int c)>()
                        ).Count(line => Enumerable.Range(0, 4).Select(i => (i, (key.r + line[i].r, key.c + line[i].c)))
                            .All(tp => grid.ContainsKey(tp.Item2) && grid[tp.Item2] == "XMAS"[tp.Item1])), 0),
    (_, _) => (0, 0),
}).Aggregate((0,0), (acc, tp) => (acc.Item1 + tp.Item1, acc.Item2 + tp.Item2)));

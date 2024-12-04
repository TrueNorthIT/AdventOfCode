    var grid = File.ReadAllLines("input.txt").SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
        .ToDictionary(tp => (tp.r, tp.c), tp => tp.ch);

    var R = grid.Max(tp => tp.Key.r);
    var C = grid.Max(tp => tp.Key.c);

    (int r, int c)[][] validLines =
        (   from or in new[] { -1, 0, 1 }
            from oc in new[] { -1, 0, 1 }
            where !(or == 0 && oc == 0)
            select (from i in Enumerable.Range(0, 4) 
                    select (or * i, oc * i))
                    .ToArray()
        ).ToArray();

    var Xs = new (int r, int c)[][] {
        new [] { (-1,-1),(1,1) },
        new [] { (-1,1),(1,-1) },
    };
    (int part1, int part2) = (0, 0);
    for (int r = 0; r <= R; r++)
    {
        for (int c = 0; c <= C; c++)
        {
            if (grid.ContainsKey((r, c)) && grid[(r, c)] == 'A')
            {
                if (Xs.Select(arr => new String(
                        arr.Select(tp => (tp.r + r, tp.c + c)).Select(tp => grid.ContainsKey(tp) ? grid[tp] : '.').ToArray()))
                    .All(str => str == "MS" || str == "SM"))
                {
                    part2++;
                }
            }
            foreach (var line in validLines)
            {
                bool allCorrect = true;
                for (int i = 0; i < line.Length; i++)
                {
                    var key = (r + line[i].r, c + line[i].c);
                    if (!grid.ContainsKey(key) || grid[key] != "XMAS"[i])
                    {
                        allCorrect = false;
                        break;
                    }
                }
                if (allCorrect) part1++;
            }
        }
    }

    Console.WriteLine($"Part 1: {part1}");
    Console.WriteLine($"Part 2: {part2}");

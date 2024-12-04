    var grid = File.ReadAllLines("input.txt").SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
        .ToDictionary(tp => (tp.r, tp.c), tp => tp.ch);

    var R = grid.Max(tp => tp.Key.r);
    var C = grid.Max(tp => tp.Key.c);

    var validLines = new (int r, int c)[][] {
        new [] { (0,0),(1,0), (2,0), (3,0) }, //down
        new [] { (0,0),(0,1), (0,2), (0,3) }, //right
        new [] { (0,0),(1,1), (2,2), (3,3) }, //right-down
        new [] { (0,0),(-1,0), (-2,0), (-3,0) }, //up
        new [] { (0,0),(0,-1), (0,-2), (0,-3) }, //left
        new [] { (0,0),(-1,-1), (-2,-2), (-3,-3) }, //left-up
        new [] { (0,0),(-1, 1), (-2, 2), (-3, 3) }, //right-up
        new [] { (0,0),(1, -1), (2, -2), (3, -3) }, //left-down
    };

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

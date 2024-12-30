(var lockHeights, var keyHeights) = (new List<List<int>>(), new List<List<int>>());
foreach (var lck in File.ReadAllText("input.txt").Split("\r\n\r\n"))
{
    var lines = lck.Split("\r\n");
    var h = Enumerable.Repeat(0, 5).ToList();
    for (int r = 0; r < lines.Length; r++)
        for (int c = 0; c < lines.First().Length; c++)
            h[c] += lines[r][c] == '#' ? 1 : 0;

    if (lines[0][0] == '#')
        lockHeights.Add(h);
    else
        keyHeights.Add(h);
}

long p1 = lockHeights.SelectMany(lck => keyHeights.Where(key => lck.Zip(key).Select(tp => tp.First + tp.Second).All(i => i <= 7))).Count();
Console.WriteLine(p1);
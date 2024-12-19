    var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
    var patterns = files[0].Split(", ").ToArray();
    var designs = files[1].Split("\r\n");

    var cache = new Dictionary<string, long>();

    Console.WriteLine($"Part 1: {designs.Where(d => possibleMemoized(d) > 0).Count()}");
    Console.WriteLine($"Part 2: {designs.Sum(possibleMemoized)}");

    long possibleMemoized(string design)
    {
        if (!cache.ContainsKey(design))
            cache.Add(design, possible(design));
        return cache[design];
    }
    long possible(string design) => design switch {
        var empty when String.IsNullOrEmpty(empty) => 1,
        var other => patterns.Where(other.StartsWith).Sum(p => possibleMemoized(other[p.Length..])),
    };
    using System.Collections.Concurrent;

    var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
    var patterns = files[0].Split(", ").ToArray();
    var designs = files[1].Split("\r\n");

    var cache = new ConcurrentDictionary<string, long>();

    Console.WriteLine(designs.Select(waysMemoized) switch { var sol => (sol.Count(r => r > 0), sol.Sum())});

    long waysMemoized(string design) => cache.GetOrAdd(design, ways);

    long ways(string design) => design switch {
        var empty when String.IsNullOrEmpty(empty) => 1,
        var other => patterns.Where(other.StartsWith).Sum(p => waysMemoized(other[p.Length..])),
    };
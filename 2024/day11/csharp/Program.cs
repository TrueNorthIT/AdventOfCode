var cache = new System.Collections.Concurrent.ConcurrentDictionary<(double, int), long>();

var solve = (int steps) => File.ReadAllText("input.txt").Split(' ')
    .Sum(tile => count(long.Parse(tile), steps));

Console.WriteLine($"Part 1: {solve(25)}, Part2: {solve(75)}");

long count(long tile, int step) => cache.GetOrAdd((tile, step),
    _ => step switch {
        0 => 1L,
        _ => (tile switch {
            0 => [1L],
                _ => (digits(tile), Math.Pow(10, digits(tile) / 2)) switch {
                    (var d, var p) when d % 2 == 0
                        => [(long)Math.Floor(tile / p), (long) (tile % p)],
                    (_, _) => new [] { tile * 2024 }
            }}).Sum(i => count(i, step))});

long digits(long a) => (long) Math.Ceiling(Math.Log(a + 1, 10));
using System.Collections.Concurrent;
var cache = new ConcurrentDictionary<(double, int), long>();

var tiles = File.ReadAllText("input.txt").Split(' ').Select(long.Parse).ToList();
var solve = (int steps) => tiles.Sum(tile => count(tile, steps));

Console.WriteLine($"Part 1: {solve(25)}, Part2: {solve(75)}");

long count(long tile, int step) => cache.GetOrAdd((tile, step),
    _ => step switch {
        0 => 1L,
        _ => (tile, digits(tile), Math.Pow(10, digits(tile) / 2)) switch {
            (0, _, _) => count(1, step - 1),
            (var even, var d, var p) when d % 2 == 0 =>
                count((long) Math.Floor(even / p), step - 1)
                + count((long) (even % p), step - 1),
            (var other, _, _) => count(other * 2024, step - 1),
        }
    });

long digits(long a) => (long) Math.Ceiling(Math.Log(a + 1, 10));
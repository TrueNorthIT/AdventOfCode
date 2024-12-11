using System.Collections.Concurrent;

var tiles = File.ReadAllText("input.txt").Split(' ').Select(double.Parse).ToList();

var cache = new ConcurrentDictionary<(double, int), long>();
var p1 = tiles.Sum(tile => count(tile, 25));
var p2 = tiles.Sum(tile => count(tile, 75));

Console.WriteLine($"Part 1: {p1}");
Console.WriteLine($"Part 2: {p2}");

long count(double tile, int step) =>
    cache.GetOrAdd((tile, step),
        cache.GetOrAdd((tile,step), step == 0 ? 1 : 
            (tile, digits(tile), Math.Pow(10, digits(tile) / 2)) switch {
                (0, _, _) => count(1, step - 1),
                (var even, var noDigits, var power) when noDigits % 2 == 0 =>
                    count(Math.Floor(even / power), step - 1)
                    +  count(even % power, step - 1),
                (var other, _, _) => count(other * 2024, step - 1),
            }));

double digits(double a) => (long) Math.Ceiling(Math.Log(a + 1, 10));
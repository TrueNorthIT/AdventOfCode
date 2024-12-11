var cache = new System.Collections.Concurrent.ConcurrentDictionary<(double, int), double>();

var solve = (int steps) => File.ReadAllText("test.txt").Split(' ')
    .Select(double.Parse)
    .Sum(count(steps));

Console.WriteLine($"Part 1: {solve(25)}, Part2: {solve(75)}");

Func <double, double> count(int step) => tile => cache.GetOrAdd((tile, step),
    _ => step switch {
        0 => 1L,
        _ => (tile switch {
            0 => [1L],
            _ => digits(tile) switch {
                var dig when dig % 2 == 0
                    => [Math.Floor(tile / power10(dig/2)), (tile % power10(dig/2))],
                _ => new [] { tile * 2024 }
        }}).Sum(count(step - 1))});

double power10(double a) => Math.Pow(10, a);
double digits(double a) => Math.Ceiling(Math.Log(a + 1, 10));
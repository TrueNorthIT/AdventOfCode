var tiles = File.ReadAllText("input.txt").Split(' ').Select(double.Parse).ToList();

var cache = new Dictionary<(double, int), long>();
var p1 = tiles.Sum(tile => count(tile, 25));
var p2 = tiles.Sum(tile => count(tile, 75));

Console.WriteLine($"Part 1: {p1}");
Console.WriteLine($"Part 2: {p2}");

long count(double tile, int step)
{
    if (cache.ContainsKey((tile, step)))
        return cache[(tile, step)];

    if (step == 0)
    {
        cache[(tile, step)] = 1;
        return 1;
    }
    else
    {
        if (tile == 0)
        {
            return count(1, step - 1);
        }
        else
        {
            var noDigits = digits(tile);
            if (noDigits % 2 == 0)
            {
                var power = Math.Pow(10, noDigits / 2);
                var answer = count(Math.Floor(tile / power), step - 1)
                             + count(tile % power, step - 1);

                cache[(tile, step)] = answer;
                return answer;
            }
            else
            {
                var answer = count(tile * 2024, step - 1);
                cache[(tile, step)] = answer;
                return answer;
            }
        }
    }
}

double digits(double a) => (long) Math.Ceiling(Math.Log(a + 1, 10));
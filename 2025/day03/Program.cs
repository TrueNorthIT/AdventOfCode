var banks = File.ReadAllLines("input.txt");

var joltages = new List<long>();
foreach (var bank in banks)
{
    var joltage = best(bank, new List<char>(), 12);
    Console.WriteLine($"Best for {bank}: {joltage}");
    joltages.Add(joltage);
}

long best(string remainder, List<char> digits, int maxLength)
{
    if (digits.Count == 0 && String.IsNullOrEmpty(remainder))
        return 0;

    if (remainder.Length + digits.Count < maxLength)
        return 0;

    if (digits.Count == maxLength || String.IsNullOrEmpty(remainder))
    {
        return long.Parse(String.Join("", digits));
    }

    //two options, take or skip
    var o1 = best(remainder[1..], digits.ToList(), maxLength);
    var o2 = best(remainder[1..], digits.Concat(new [] {remainder[0] }).ToList(), maxLength);

    if (o1 > o2)
    {
        return o1;
    }
    return o2;
}

var p1 = joltages.Sum();
Console.WriteLine($"Part 1: {p1}");
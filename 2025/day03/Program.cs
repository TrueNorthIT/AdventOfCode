var banks = File.ReadAllLines("input.txt");

(var p1, var p2) = (0L, 0L);
foreach (var bank in banks)
{
    p1 += best(bank, [], 2);
    p2 += best(bank, [], 12);
}

long best(string remainder, List<char> digits, int maxLength)
{
    if (digits.Count == maxLength)
        return long.Parse(String.Join("", digits));

    for (char c = '9'; c >= '0'; c--)
    {
        var indexOf = remainder.IndexOf(c,0,remainder.Length - maxLength - digits.Count + 1);
        if (indexOf == -1)
            continue;

        return best(remainder[(indexOf + 1)..], [.. digits, c], maxLength);
    }
    throw new();
}

Console.WriteLine((p1,p2));

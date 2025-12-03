var banks = File.ReadAllLines("input.txt");

(var p1, var p2) = (0L, 0L);
foreach (var bank in banks)
{
    p1 += best(bank, [], 2);
    p2 += best(bank, [], 12);
}

long best(string remainder, List<char> digits, int L)
{
    if (digits.Count == L)
        return long.Parse(String.Join("", digits));

    var next = remainder[..^(L - digits.Count)].Index()
        .OrderByDescending(tp => tp.Item)
        .ThenBy(tp => tp.Index).First();

    return best(remainder[(next.Index + 1)..], [.. digits, next.Item], L);
}

Console.WriteLine((p1,p2));

var banks = File.ReadAllLines("input.txt");

(var p1, var p2) = (0L, 0L);
foreach (var bank in banks)
{
    p1 += best(bank, "", 2);
    p2 += best(bank, "", 12);
}

long best(string rem, string num, int L) => num.Length == L ?
    long.Parse(num)
    : rem[..^(L - num.Length - 1)]
        .Index()
        .OrderByDescending(tp => tp.Item)
        .ThenBy(tp => tp.Index)
        .First() switch {
            var next => best(rem[(next.Index + 1)..], num + next.Item, L)
        };

Console.WriteLine((p1,p2));

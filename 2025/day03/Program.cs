int.Parse((solve(2), solve(12))+"");
long solve(int max) => File.ReadAllLines("input.txt").Sum(b => best(b, "", max));
long best(string rem, string num, int L) =>
    (num.Length == L) switch {
    true => long.Parse(num),
    false => rem[..^(L - num.Length - 1)]
                .Index()
                .OrderByDescending(tp => tp.Item)
                .ThenBy(tp => tp.Index)
                .First() switch { var next 
                => best(rem[(next.Index + 1)..], num + next.Item, L) 
            }
    };
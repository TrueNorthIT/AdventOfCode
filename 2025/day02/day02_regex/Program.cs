using System.Text.RegularExpressions;

HashSet<long> p1 = [], p2 = [];
var r = "^(\\d{1,})\\1{1";
bool m(long i, bool b) => Regex.IsMatch(i + "", r + (b ? "}$" : ",100}$"));

foreach ((long st, long en) in File.ReadAllText("example.txt").Split(',').Select(r =>
    r.Split('-') switch {
        [var a, var b] => (long.Parse(a), long.Parse(b))
    }
))
    for (var i = st; i <= en; i++)
        if (m(i,true))
            p1.Add(i);
        else if (m(i, false))
            p2.Add(i);

int.Parse($"{p1.Sum()},{p1.Concat(p2).Sum()}");
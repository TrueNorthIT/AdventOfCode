using System.Text.RegularExpressions;

HashSet<long> p1 = [], p2 = [];
bool m(long i, bool b) => Regex.IsMatch(i + "", "^(\\d{1,})\\1{1" + (b ? "}$" : ",100}$"));

foreach (var arr in File.ReadAllText("example.txt").Split(',').Select(r =>
    r.Split('-').Select(long.Parse).ToArray()))
    for (var i = arr[0]; i <= arr[1]; i++)
        if (m(i,true))
            p1.Add(i);
        else if (m(i, false))
            p2.Add(i);

int.Parse($"{p1.Sum()},{p1.Concat(p2).Sum()}");
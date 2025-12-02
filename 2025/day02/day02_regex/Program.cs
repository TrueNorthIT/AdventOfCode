using System.Text.RegularExpressions;

HashSet<long> p1 = [], p2 = [];
bool m(long i, bool b) => Regex.IsMatch(i + "", @"^(\d{1,})\1{1" + (b ? "}$" : ",100}$"));

foreach (var s in File.ReadAllText("example.txt").Split(',').Select(r =>
    r.Split('-').Select(long.Parse).ToList()))
    for (var i = s[0]; i <= s[1]; i++)
        if (m(i,1>0))
            p1.Add(i);
        else if (m(i, 1<0))
            p2.Add(i);

int.Parse((p1.Sum(),p1.Sum()+p2.Sum())+"");
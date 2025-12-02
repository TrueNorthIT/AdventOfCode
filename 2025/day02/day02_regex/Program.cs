using System.Text.RegularExpressions;

(long start, long end)[] ranges = [.. File.ReadAllText("input.txt").Split(',').Select(range =>
{
    var sp = range.Split('-');
    return (long.Parse(sp[0]), long.Parse(sp[1]));
})];

const string template = "^({0})\\1";

var p1 = new HashSet<long>();
var p2 = new HashSet<long>();
foreach (var range in ranges)
{
    for (long i = range.start; i <= range.end; i++)
    {
        var st = i.ToString();

        for (int divisor = 2; divisor <= st.Length; divisor++)
        {
            if (st.Length % divisor != 0)
                continue;

            var size = st.Length / divisor;
            var regex = String.Format(template, String.Join("", Enumerable.Repeat("\\d", size))) + "{1,}$";
            var matches = new Regex(regex).Match(st);
            if (matches.Success)
            {
                if (divisor == 2)
                    p1.Add(i);
                p2.Add(i);
            }
        }
    }
}
Console.WriteLine($"{p1.Sum()},{p2.Sum()}");

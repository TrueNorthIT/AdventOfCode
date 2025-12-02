(long start, long end)[] ranges = File.ReadAllText("input.txt").Split(',').Select(range =>
{
    var sp = range.Split('-');
    return (long.Parse(sp[0]), long.Parse(sp[1]));
}).ToArray();

var invalid = new List<long>();
foreach (var range in ranges)
{
    for (long i = range.start; i <= range.end; i++)
    {
        var st = i.ToString();
        if (st.Length % 2 != 0)
            continue;

        var i1 = st.Substring(0, st.Length / 2);
        var i2 = st.Substring(st.Length / 2, st.Length / 2);
        if (i1 == i2)
        {
            invalid.Add(i);
        }
    }
}

var p1 = invalid.Sum();
Console.WriteLine(p1);

var invalidp2 = new List<long>();
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
            var first = st.Substring(0, size);
            for (int t = 1; t < divisor; t++)
            {
                var next = st.Substring(t * size, size);
                if (next != first)
                {
                    goto skip;
                }
            }
            invalidp2.Add(i);
            skip:;
        }
    }
}
var p2 = invalidp2.Distinct().Sum();
Console.WriteLine(p2);


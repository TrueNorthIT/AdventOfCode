var (c, a, b) = (50, 0, 0);
foreach (var s in File.ReadLines("i"))
{
    for (int i = 0; i < int.Parse(s[1..]); (i, c) = (i + 1, (c + (s[0] == 'R' ? 1 : -1)) % 100))
        if (c == 0) b++;
    if (c == 0) a++;
}
throw new((a,b)+"");
Console.WriteLine(File.ReadAllLines("i").Aggregate((c: 50, p1: 0, p2: 0), (a, s) =>
{
    for (int i = 0; i < int.Parse(s[1..]); i++)
    {
        a.c += s[0] == 'R' ? 1 : -1;
        if (a.c % 100 == 0) a.p2++;
    }
    return (a.c, a.p1 += a.c % 100 == 0 ? 1 : 0, a.p2);
}));
var(c, a, b) = (50, 0, 0);
foreach (var s in File.ReadAllLines("i"))
{
    for (int i = 0; i < int.Parse(s[1..]); i++)
    {
        c += s[0] == 'R' ? 1 : -1;
        if (c % 100 == 0) b++;
    }
    if (c % 100 == 0) a++;
}
Console.WriteLine((a,b));
using System.Numerics;

var grid = File.ReadAllText("input.txt").Split("\r\n")
        .SelectMany((line, r) => line.Select((ch, c) => (new Complex(r, c), ch)))
        .ToDictionary(tp => tp.Item1, tp => tp.ch);

System.Diagnostics.Stopwatch watch = System.Diagnostics.Stopwatch.StartNew();

var R = (int) grid.Max(kvp => kvp.Key.Real);
var C = (int) grid.Max(kvp => kvp.Key.Imaginary);

var start = grid.Where(kvp => kvp.Value == 'S').Single().Key;
var end = grid.Where(kvp => kvp.Value == 'E').Single().Key;
grid[start] = '.';
grid[end] = '.';

var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) }; //E, S, W, N

List<(int t, bool cheated)> p1Solutions = solve();

var regularFinish = p1Solutions.Single(tp => !tp.cheated).t;
int p1 = 0;
var savings = p1Solutions.GroupBy(tp => tp.t).Select(grp => (regularFinish - grp.Key, grp.Count())).OrderBy(tp => tp.Item1).ToList();
foreach (var cheat in savings)
{
    if (cheat.Item1 > 0)
    {
        Console.WriteLine($"There are {cheat.Item2} cheats thats save {cheat.Item1} picoseconds.");
    }
    if (cheat.Item1 >= 100)
    {
        p1 += cheat.Item2;
    }
}
//390 too low!
Console.WriteLine($"Part 1: {p1}");

List<(int t, bool cheated)> solve()
{
    var queue = new Queue<(Complex, int, (Complex? cS, Complex? cE)?)>();
    queue.Enqueue((start, 0, null));
    var visited = new HashSet<(Complex, (Complex? cS, Complex? cE)?)>();

    var solutions = new List<(int t, bool cheated)>();
    while (queue.TryDequeue(out (Complex pos, int t, (Complex? cS, Complex? cE)? cheat) curr))
    {
        if (visited.Contains((curr.pos, curr.cheat)))
            continue;

        if (curr.pos == end)
        {
            solutions.Add((curr.t, curr.cheat.HasValue));
            continue;
        }

        visited.Add((curr.pos, curr.cheat));

        foreach (var next in dirs.Select(dir => curr.pos + dir))
        {
            if (!grid.ContainsKey(next))
                continue;
            if (grid[next] != '#')
            {
                if (curr.cheat.HasValue && curr.cheat.Value.cS.HasValue)
                {
                    //we need to record the end of the cheat
                    queue.Enqueue((next, curr.t + 1, (curr.cheat.Value.cS, next)));
                }
                else
                {
                    queue.Enqueue((next, curr.t + 1, curr.cheat));
                }
            }
            else if (curr.cheat == null)
            {
                //we can move into a wall
                var cheat = (next, (Complex?) null);
                queue.Enqueue((next, curr.t + 1, cheat));
            }
        }
    }
    return solutions;
}

//bool inBounds(Complex point, int R, int C) => point switch
//{
//    var inBound when inBound.Real >= 0 && inBound.Real <= R && inBound.Imaginary >= 0 && inBound.Imaginary <= C => true,
//    _ => false,
//};

//void print(HashSet<Complex> route, Dictionary<Complex, int> bytes)
//{
//    var sb = new StringBuilder();
//    for (int y = 0; y <= Y; y++)
//    {
//        for (int x = 0; x <= X; x++)
//        {
//            var p = new Complex(x, y);
//            if (route.Contains(p))
//            {
//                sb.Append('O');
//            }
//            else if (bytes.ContainsKey(p))
//            {
//                sb.Append('#');
//            }
//            else
//            {
//                sb.Append('.');
//            }
//        }
//        sb.AppendLine();
//    }
//    Console.WriteLine(sb);
//}
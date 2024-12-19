using System.Numerics;
using System.Text;

System.Diagnostics.Stopwatch watch = System.Diagnostics.Stopwatch.StartNew();

#if FALSE
const int X = 6; const int Y = X;
var _bytes = File.ReadAllText("test.txt").Split("\r\n")
#elif FALSE
const int X = 70; const int Y = X;
var _bytes = File.ReadAllText("input.txt").Split("\r\n")
#elif TRUE
const int X = 212; const int Y = X;
var _bytes = File.ReadAllText("large.txt").Split("\r\n")
#endif
        .Select((line, r) => {
            var sp = line.Split(",").Select(int.Parse).ToArray();
            return (new Complex(sp[0], sp[1]), r);
        });

var bytes = new Dictionary<Complex, int>();
foreach (var  b in _bytes)
{
    if (!bytes.ContainsKey(b.Item1))
    {
        bytes.Add(b.Item1, b.Item2);
    }
}

var end = new Complex(X, Y);
var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) };

var cache = solve(bytes);
var route = new List<Complex>();
var curr = end;
while (curr != new Complex(0,0))
{
    route.Add(cache[curr]);
    curr = cache[curr];
}

var p2 = route.Where(bytes.ContainsKey).MinBy(point => bytes[point]);
watch.Stop();
Console.WriteLine($"Solution {p2} in {watch.ElapsedMilliseconds}ms");
Dictionary<Complex, Complex> solve(Dictionary<Complex,int> bytes)
{
    //queue is prioritised by the max t of a byte along its path (remember its a -'ve queue though)    
    var queue = new PriorityQueue<(Complex from, Complex to),int>();
    queue.Enqueue((new Complex(0, 0), new Complex(0, 0)), int.MinValue);
    var visited = new Dictionary<Complex, Complex>();
    while (queue.TryDequeue(out (Complex from, Complex to) move, out int priority))
    {
        if (!visited.TryAdd(move.to, move.from))
            continue;

        if (move.to == end)
            return visited;

        //print(curr.path.ToHashSet(), bytes, -priority);
        foreach (var d in dirs)
        {
            var next = move.to + d;
            if (next.Real < 0 || next.Real > X || next.Imaginary < 0 || next.Imaginary > Y)
                continue;

            queue.Enqueue((move.to, next),
                Math.Max(priority, -bytes.GetValueOrDefault(next, int.MaxValue))); //|MinValue| > |MaxValue|
        }
    }
    throw new();
}

bool inBounds(Complex point) => (point.Real, point.Imaginary) switch {
    ( >= 0 and <= X, >= 0 and <= Y) => true,
    _ => false,
};

void print(HashSet<Complex> route, Dictionary<Complex, int> bytes, int t)
{
    var sb = new StringBuilder();
    for (int y = 0; y <= Y; y++)
    {
        for (int x = 0; x <= X; x++)
        {
            var p = new Complex(x, y);
            if (route.Contains(p))
            {
                sb.Append('O');
            }
            else if (bytes.ContainsKey(p) && bytes[p] <= t)
            {
                sb.Append('#');
            }
            else
            {
                sb.Append('.');
            }
        }
        sb.AppendLine();
    }
    Console.WriteLine(sb);
}
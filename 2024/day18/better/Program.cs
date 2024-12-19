using System.Collections.Generic;
using System.Numerics;
using System.Text;
using static System.Net.Mime.MediaTypeNames;

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
            return ((sp[0], sp[1]), r);
        });

//reddit input had dupes so clean it up, kind of dumb!
var __bytes = new Dictionary<(int x, int y), int>();
foreach (var  b in _bytes)
    if (!__bytes.ContainsKey(b.Item1))
    {
        __bytes.Add(b.Item1, b.Item2);
    }

var bytes = new int[X + 1, Y + 1];
for (int x = 0; x <= X; x++)
    for (int y = 0; y <= Y; y++)
        bytes[x, y] = int.MaxValue;

foreach (var b in __bytes)
{
    bytes[b.Key.x, b.Key.y] = b.Value;
}


(int x, int y) end = (X, Y);
var dirs = new (int x, int y)[] { (0, 1), (1, 0), (0, -1), (-1, 0) };

//start timing now we have parsed the data
System.Diagnostics.Stopwatch watch = System.Diagnostics.Stopwatch.StartNew();

((int x, int y), int t) p2 = default;
List<(int x, int y)> route = null;
for (int a = 0; a < 10; a++)
{
    var cache = dijkstra(bytes);
    //back track through the cache to reconstruct the actual path
    route = new List<(int x, int y)>();
    var curr = end;
    while (curr != (0, 0))
    {
        var prev = cache[curr.x, curr.y];
        route.Add(prev);
        curr = prev;
    }   
    //find the point at which this path would no longer be possible
    p2 = route.Select(r => (r, bytes[r.x, r.y])).MinBy(tp => tp.Item2);
}
watch.Stop();

//find the time at which this path would no longer be possible so we can print the obstacles
print(route.ToHashSet(), bytes, p2.t);
Console.WriteLine($"Solution {p2.Item1} in {watch.ElapsedMilliseconds / 10}ms");

(int x, int y)[,] dijkstra(int[,] bytes)
{
    var visited = new bool[X + 1, Y + 1];
    var prev = new (int x, int y)[X + 1, Y + 1];
    for (int x = 0; x <= X; x++)
        for (int y = 0; y <= Y; y++)
            prev[x, y] = (-1,-1);

    //queue is prioritised by the max t of a byte along its path (remember its a -'ve queue though)    
    var queue = new PriorityQueue<((int x, int y) from, (int x, int y) to),int>();
    queue.Enqueue(((-1,-1),(0, 0)), int.MinValue);
    while (queue.TryDequeue(out ((int x,int y) from, (int x, int y) to) move, out int priority))
    {
        if (visited[move.to.x, move.to.y])
            continue;
        visited[move.to.x, move.to.y] = true;

        prev[move.to.x, move.to.y] = move.from;
        if (move.to == end)
            return prev;

        foreach (var d in dirs)
        {
            (int x, int y) next = (move.to.x + d.x, move.to.y + d.y);
            if (next.x < 0 || next.x > X || next.y < 0 || next.y > Y)
                continue;
            
            queue.Enqueue((move.to, next), Math.Max(priority, -bytes[next.x, next.y])); //|MinValue| > |MaxValue|
        }
    }
    throw new();
}

bool inBounds(Complex point) => (point.Real, point.Imaginary) switch {
    ( >= 0 and <= X, >= 0 and <= Y) => true,
    _ => false,
};

void print(HashSet<(int x, int y)> route, int[,] bytes, int t)
{
    var sb = new StringBuilder();
    for (int y = 0; y <= Y; y++)
    {
        for (int x = 0; x <= X; x++)
        {
            var p = (x, y);
            if (route.Contains(p))
            {
                sb.Append('O');
            }
            else if (bytes[x,y] <= t)
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
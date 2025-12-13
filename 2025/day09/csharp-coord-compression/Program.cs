using System.Diagnostics;
using Point = (long x, long y);

var watch = Stopwatch.StartNew();
var redTiles = File.ReadAllLines("input.txt")
        .Select(line => line.Split(',').Select(long.Parse) switch {
            var sp => (x: sp.First(), y: sp.Skip(1).First())
        })
    .ToArray();

//maps both ways for our compressed coordinates
var xMap = redTiles.Select(p => p.x).Distinct().OrderBy(x => x).Index().ToArray();
var invXMap = xMap.ToDictionary(tp => tp.Item, tp => tp.Index);
var yMap = redTiles.Select(p => p.y).Distinct().OrderBy(y => y).Index().ToArray();
var invYMap = yMap.ToDictionary(tp => tp.Item, tp => tp.Index);

var comp = redTiles.Select(p => new Point(invXMap[p.x], invYMap[p.y])).ToArray();

var grid = new int[xMap.Length, yMap.Length];

//draw the polygon on our compressed grid
for (int e = 0; e < comp.Length; e++)
{
    var next = comp[(e + 1) % comp.Length];
    if (next.x == comp[e].x)
    {
        for (var y = comp[e].y; y != next.y; y += Math.Sign(next.y - comp[e].y))
            grid[comp[e].x, y] = 1; //green
    }
    else
    {
        for (var x = comp[e].x; x != next.x; x += Math.Sign(next.x - comp[e].x))
            grid[x, comp[e].y] = 1; //green
    }
    grid[comp[e].x, comp[e].y] = 2; //red
}

#if DEBUG
Console.WriteLine($"Compressed grid:");
print(grid);
#endif

//for every point along the edge of our grid, start a flood fill
//we go along the edges just to avoid expanding our grid
//there must be somewhere to start an outside in flood fill
var queue = new Queue<Point>();
for (int x = 0; x < xMap.Length; x++)
{
    if (grid[x, 0] == 0)
        queue.Enqueue(new Point(x, 0));
    if (grid[x, yMap.Length - 1] == 0)
        queue.Enqueue(new Point(x, yMap.Length - 1));
}
for (int y = 0; y < yMap.Length; y++)
{
    if (grid[0, y] == 0)
        queue.Enqueue(new Point(0, y));
    if (grid[xMap.Length - 1, y] == 0)
        queue.Enqueue(new Point(xMap.Length - 1, y));
}
while (queue.Any())
{
    var curr = queue.Dequeue();
    grid[curr.x, curr.y] = -1;
    foreach (var neighbour in neighbours(curr))
    {
        if (grid[neighbour.x, neighbour.y] == 0)
        {
            grid[neighbour.x, neighbour.y] = -1; //outside
            queue.Enqueue(neighbour);
        }        
    }
}

#if DEBUG
Console.WriteLine($"Flood filled grid:");
print(grid);
#endif

var p2 = (
 from c1 in comp
 from c2 in comp
 where c1.x < c2.x || (c1.x == c2.x && c1.y < c2.y)
 let c1E = new Point(xMap[c1.x].Item, yMap[c1.y].Item)
 let c2E = new Point(xMap[c2.x].Item, yMap[c2.y].Item)
 select (c1, c2, c1E, c2E, expandedArea: rectArea(c1E, c2E)))
.OrderByDescending(tp => tp.expandedArea)
.First(tp =>
{
    //simple 4 corner check first speeds things up a little
    if (grid[tp.c1.x, tp.c1.y] == -1
       || grid[tp.c1.x, tp.c2.y] == -1
       || grid[tp.c2.x, tp.c1.y] == -1
       || grid[tp.c2.x, tp.c2.y] == -1
    ) return false;

    //simple loop over all rectangle points to find if there are any outside points
    for (var x = Math.Min(tp.c1.x, tp.c2.x); x <= Math.Max(tp.c1.x, tp.c2.x); x++)
    for (var y = Math.Min(tp.c1.y, tp.c2.y); y <= Math.Max(tp.c1.y, tp.c2.y); y++)
        if (grid[x, y] == -1)
            return false;

    return true;
});
watch.Stop();
Console.WriteLine((p2.c1E, p2.c2E, p2.expandedArea) + $" in {watch.ElapsedMilliseconds}ms");

List<Point> neighbours(Point point) => [.. new [] {
    new Point(point.x - 1, point.y - 1),
    new Point(point.x    , point.y - 1),
    new Point(point.x + 1, point.y - 1),
    new Point(point.x - 1, point.y    ),
    new Point(point.x + 1, point.y    ),
    new Point(point.x - 1, point.y + 1),
    new Point(point.x    , point.y + 1),
    new Point(point.x + 1, point.y + 1),
}.Where(p => p.x >= 0 && p.x < xMap.Length && p.y > 0 && p.y < yMap.Length)];

long rectArea(Point p1, Point p2) => (1 + Math.Abs(p2.x - p1.x)) * (1 + Math.Abs(p2.y - p1.y));

void print(int[,] arr)
{
    for (int y = 0; y < arr.GetLength(1); y++)
    {
        for (int x = 0; x < arr.GetLength(0); x++)
        {
            Console.Write(arr[x, y] switch {
                -1 => '_',
                0 => '.',
                1 => 'X',
                2 => '#',
            });
        }
        Console.WriteLine();
    }
    Console.WriteLine();
}
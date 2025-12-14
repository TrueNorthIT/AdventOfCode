using RBush;
using System.Diagnostics;

var watch = Stopwatch.StartNew();
var redTiles = File.ReadAllLines("input.txt")
        .Select(line => line.Split(',').Select(int.Parse) switch {
            var sp => (x: sp.First(), y: sp.Skip(1).First())
        })
    .ToArray();

//maps both ways for our compressed coordinates
var xMap = redTiles.Select(p => p.x).Distinct().OrderBy(x => x).Index().ToArray();
var invXMap = xMap.ToDictionary(tp => tp.Item, tp => tp.Index);
var yMap = redTiles.Select(p => p.y).Distinct().OrderBy(y => y).Index().ToArray();
var invYMap = yMap.ToDictionary(tp => tp.Item, tp => tp.Index);
var compressed = redTiles.Select(p => new Point(invXMap[p.x], invYMap[p.y])).ToArray();

watch.Stop();
Console.WriteLine($"Parsing complete by {watch.ElapsedMilliseconds}ms");
watch.Start();

var grid = new int[xMap.Length, yMap.Length];

//draw the polygon on our compressed grid
for (int e = 0; e < compressed.Length; e++)
{
    var next = compressed[(e + 1) % compressed.Length];
    if (next.x == compressed[e].x)
    {
        for (var y = compressed[e].y; y != next.y; y += Math.Sign(next.y - compressed[e].y))
            grid[compressed[e].x, y] = 1; //green
    }
    else
    {
        for (var x = compressed[e].x; x != next.x; x += Math.Sign(next.x - compressed[e].x))
            grid[x, compressed[e].y] = 1; //green
    }
    grid[compressed[e].x, compressed[e].y] = 2; //red
}

watch.Stop();
//print(grid);
Console.WriteLine($"Grid compressed by {watch.ElapsedMilliseconds}ms:");
watch.Start();

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

watch.Stop();
//print(grid);
Console.WriteLine($"Grid flood filled by {watch.ElapsedMilliseconds}ms:");
watch.Start();

////find all exterior points and put into a range tree
////then query the rectangles against that
//var rPoints = new List<RPoint>();
//var bush = new KDBush.KDBush<int>();
//var points = new List<KDBush.Point<int>>();
//for (int x = 0; x < xMap.Length; x++)
//    for (int y = 0; y < yMap.Length; y++)
//    {
//        if (grid[x, y] == -1)
//        {
//            rPoints.Add(new RPoint(new Envelope(x, y, x, y)));
//            points.Add(new KDBush.Point<int>(x, y));
//        }
//    }
//Console.WriteLine($"Found {points.Count} exterior points in {watch.ElapsedMilliseconds}ms");
//var tree = new RBush<RPoint>();
//tree.BulkLoad(rPoints);
//bush.Index(points);
//Console.WriteLine($"Indexed KDBush in {watch.ElapsedMilliseconds}ms");

var rand = new Random();
var p2 = (
 from c1 in compressed
 from c2 in compressed
 where c1.x < c2.x || (c1.x == c2.x && c1.y < c2.y)
 let c1E = new Point(xMap[c1.x].Item, yMap[c1.y].Item)
 let c2E = new Point(xMap[c2.x].Item, yMap[c2.y].Item)
 select (c1, c2, c1E, c2E, expandedArea: rectArea(c1E, c2E)))
.OrderByDescending(tp => tp.expandedArea)
.First(tp =>
{
    (var minY, var maxY) = tp.c1.y < tp.c2.y ? (tp.c1.y, tp.c2.y) : (tp.c2.y, tp.c1.y);
    if (true)
    {
        //4 corner check first speeds things up a little
        if (grid[tp.c1.x, tp.c1.y] == -1
           || grid[tp.c1.x, tp.c2.y] == -1
           || grid[tp.c2.x, tp.c1.y] == -1
           || grid[tp.c2.x, tp.c2.y] == -1
        ) return false;

        //loop over all rectangle points to find if there are any outside points
        for (var x = tp.c1.x; x <= tp.c2.x; x++)
            for (var y = minY; y <= maxY; y++)
                if (grid[x, y] == -1)
                    return false;
    }
    else if (false)
    {
        for (var x = Math.Min(tp.c1.x, tp.c2.x); x <= Math.Max(tp.c1.x, tp.c2.x); x++)
            for (var y = Math.Min(tp.c1.y, tp.c2.y); y <= Math.Max(tp.c1.y, tp.c2.y); y++)
            {
                if (grid[x, y] <= 0) //not a red tile or green edge which we have marekd
                {
                    var w = winding(new Point(x, y));
                    if (Math.Abs(w) < 1) //its an outside point
                        return false;
                }
            }
    }
    else
    {
        //not really any quicker using range trees, the cost to build it outweighs any slight gain in querying points vs looping over them all
        //var treePoints = tree.Search(new Envelope(tp.c1.x, Math.Min(tp.c1.y, tp.c2.y), tp.c2.x, Math.Max(tp.c1.y, tp.c2.y)));
        //var bushPoints =  bush.Query(tp.c1.x, Math.Min(tp.c1.y, tp.c2.y), tp.c2.x, Math.Max(tp.c1.y, tp.c2.y));
        //this is a new method I added that is just a shortcut version of Search
        //return !bush.Any(tp.c1.x, Math.Min(tp.c1.y, tp.c2.y), tp.c2.x, Math.Max(tp.c1.y, tp.c2.y));
    }

    return true;
});
watch.Stop();
Console.WriteLine($"Best found in {watch.ElapsedMilliseconds}ms");
Console.WriteLine(((p2.c1, p2.c2),(p2.c1E, p2.c2E), p2.expandedArea));

IEnumerable<Point> neighbours(Point point) => [.. new [] {
    new Point(point.x - 1, point.y - 1),
    new Point(point.x    , point.y - 1),
    new Point(point.x + 1, point.y - 1),
    new Point(point.x - 1, point.y    ),
    new Point(point.x + 1, point.y    ),
    new Point(point.x - 1, point.y + 1),
    new Point(point.x    , point.y + 1),
    new Point(point.x + 1, point.y + 1),
}.Where(p => p.x >= 0 && p.x < xMap.Length && p.y > 0 && p.y < yMap.Length)];

double winding(Point p1)
{
    //yeah this obviously isn't going to be correct you could get anything
    //need to be the delta of the angle between successive edges
    //and we need to be careful about the sign of these as ATan will only produce values form -90 to +90
    double res = 0;
    foreach (var c in compressed)
    {
        res += Math.Atan2(c.y - p1.y, c.x - p1.x);
    }
    return res;
}

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

class RPoint : ISpatialData
{
    public RPoint(Envelope envelope) => _envelope = envelope;
    private readonly Envelope _envelope;
    public ref readonly Envelope Envelope => ref _envelope;
}

record struct Point(int x, int y);
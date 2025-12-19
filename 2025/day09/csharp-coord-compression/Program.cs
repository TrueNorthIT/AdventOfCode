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
var comp = redTiles.Select(p => new Point(invXMap[p.x], invYMap[p.y])).ToArray();

Console.WriteLine($"Parsing complete by {watch.ElapsedMilliseconds}ms");

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

while (queue.TryDequeue(out Point curr))
{
    grid[curr.x, curr.y] = -1;
    foreach (var neighbour in neighbours(curr))
        if (grid[neighbour.x, neighbour.y] == 0)
        {
            grid[neighbour.x, neighbour.y] = -1; //outside
            queue.Enqueue(neighbour);
        }        
}

Console.WriteLine($"Grid flood filled by {watch.ElapsedMilliseconds}ms:");

//Using a Summed Area Table (https://en.wikipedia.org/wiki/Summed-area_table)
// Fill the grid in one pass using this recursion
// S(x,y) = i(x,y) + I(x,y-1) + I(x-1,y) - I(x-1,y-1)
// And calculate total points in a given bounding Box with:
// I(D) + I(A) - I(B) - I(C)
// = i(x1,y1) + i(x0 - 1,y0 - 1) - i(x0 - 1,y1) - i(x1, y0 - 1)

//start grid at 1 to provide a convenient 0 row / column that is all 0's
int[,] sums = new int[xMap.Length + 1, yMap.Length + 1];
for (int y = 1; y < yMap.Length + 1; y++)
    for (int x = 1; x < xMap.Length + 1; x++)
    {
        sums[x, y] = (grid[x - 1, y - 1] == -1) ? 1 : 0;
        sums[x, y] += sums[x, y - 1];
        sums[x, y] += sums[x - 1, y];
        sums[x, y] -= sums[x - 1, y - 1];
    }

watch.Stop();
Console.WriteLine($"Prefix sums calculated by {watch.ElapsedMilliseconds}ms");
watch.Start();

long best = 0;
for (int c1 = 0; c1 < comp.Length; c1++)
    for (int c2 = c1+1; c2 < comp.Length; c2++)
    {
        (var minY, var maxY) = comp[c1].y < comp[c2].y ? (comp[c1].y, comp[c2].y) : (comp[c2].y, comp[c1].y);
        if ((sums[comp[c2].x + 1, maxY + 1] + sums[comp[c1].x, minY ] 
            - sums[comp[c2].x + 1, minY] - sums[comp[c1].x, maxY + 1]) == 0)
        {
            best = Math.Max(best, rectArea(new Point(xMap[comp[c1].x].Item, yMap[comp[c1].y].Item), new Point(xMap[comp[c2].x].Item, yMap[comp[c2].y].Item)));
        }
    }

watch.Stop();
Console.WriteLine($"Best of {best} found in {watch.ElapsedMilliseconds}ms");

long rectArea(Point p1, Point p2) => (1 + Math.Abs(p2.x - p1.x)) * (1 + Math.Abs(p2.y - p1.y));
IEnumerable<Point> neighbours(Point point)
{
    for (int x = -1; x <= 1; x++)
        for (int y = -1; y <= 1; y++)
        {
            var neighbour = new Point(point.x + x, point.y + y);
            if (neighbour.x >= 0 && neighbour.x < xMap.Length && neighbour.y >= 0 && neighbour.y < yMap.Length)
                yield return neighbour;
        }
}

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
record struct Point(int x, int y);
using System.Diagnostics;
var watch = Stopwatch.StartNew();
var lines = File.ReadAllLines("input.txt");

var redTiles = new int[lines.Length, 2];
for (int l = 0; l < lines.Length; l++)
{
    var numbers = lines[l].Split(',');
    redTiles[l, 0] = int.Parse(numbers[0]);
    redTiles[l, 1] = int.Parse(numbers[1]);
}

Console.WriteLine($"Parsing complete by {watch.ElapsedMilliseconds}ms");

(var xMap, var yMap, var invXMap, var invYMap) = getCompressionMaps();

Console.WriteLine($"Compression complete by {watch.ElapsedMilliseconds}ms");

//create an array of the red tiles in the compressed coordinates
var comp = new int[lines.Length,2];
for (int l = 0; l < lines.Length; l++)
{
    comp[l, 0] = invXMap[redTiles[l, 0]];
    comp[l, 1] = invYMap[redTiles[l, 1]];
}

//draw the polygon on our compressed grid
var grid = new int[xMap.Length, yMap.Length];
for (int e = 0; e < lines.Length; e++)
{
    (var nextx, var nexty) = (comp[(e + 1) % lines.Length,0], comp[(e + 1) % lines.Length, 1]);
    if (nextx == comp[e,0])
        for (var y = comp[e,1]; y != nexty; y += Math.Sign(nexty - comp[e,1]))
            grid[comp[e,0], y] = 1; //green
    else
        for (var x = comp[e,0]; x != nextx; x += Math.Sign(nextx - comp[e,0]))
            grid[x, comp[e,1]] = 1; //green

    grid[comp[e,0], comp[e,1]] = 2; //red
}

Console.WriteLine($"Polygon drawn by {watch.ElapsedMilliseconds}ms");

//Try and start the flood fill in all 4 corners (obviously not guaranteed to be sufficient for all shapes)
var queue = new Queue<Point>([new Point(0,0), new Point(0, yMap.Length - 1), new Point(xMap.Length - 1, 0), new Point(xMap.Length - 1, yMap.Length - 1)]);
while (queue.TryDequeue(out Point curr))
{
    if (grid[curr.x, curr.y] != 0)
        continue;
        
    grid[curr.x, curr.y] = -1;
    foreach (var neighbour in neighbours(curr))
        queue.Enqueue(neighbour);
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
        sums[x, y] = ((grid[x - 1, y - 1] == -1) ? 1 : 0) + sums[x, y - 1] + sums[x - 1, y] - sums[x - 1, y - 1];

watch.Stop();
Console.WriteLine($"Prefix sums calculated by {watch.ElapsedMilliseconds}ms");
watch.Start();

long best = 0;
for (int c1 = 0; c1 < lines.Length; c1++)
    for (int c2 = c1+1; c2 < lines.Length; c2++)
    {
        int[] ys = comp[c1,1] < comp[c2,1] ? [comp[c1,1], comp[c2,1]] : [comp[c2,1], comp[c1,1]];
        if ((sums[comp[c2,0] + 1, ys[1] + 1] + sums[comp[c1,0], ys[0]] 
            - sums[comp[c2,0] + 1, ys[0]] - sums[comp[c1,0], ys[1] + 1]) == 0)
            best = Math.Max(best, rectArea(new Point(xMap[comp[c1,0]], yMap[comp[c1,1]]), new Point(xMap[comp[c2,0]], yMap[comp[c2,1]])));
    }

watch.Stop();
Console.WriteLine($"Best of {best} found in {watch.ElapsedMilliseconds}ms");

(int[] xMap, int[] yMap, Dictionary<int,int> invXMap, Dictionary<int, int> invYMap) getCompressionMaps()
{
    var xSet = new SortedSet<int>();
    var ySet = new SortedSet<int>();
    for (int l = 0; l < lines.Length; l++)
    {
        xSet.Add(redTiles[l, 0]);
        ySet.Add(redTiles[l, 1]);
    }
    var xMap = xSet.ToArray();
    var yMap = ySet.ToArray();

    //maps both ways for our compressed coordinates
    var invXMap = xMap.Index().ToDictionary(tp => tp.Item, tp => tp.Index);
    var invYMap = yMap.Index().ToDictionary(tp => tp.Item, tp => tp.Index);

    return (xMap, yMap, invXMap, invYMap);
}

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
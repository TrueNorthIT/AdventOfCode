using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
var watch = Stopwatch.StartNew();
var lines = File.ReadAllLines("input.txt");

(var redXs, var redYs)= parseRedTiles(lines);

Console.WriteLine($"Parsing complete by {watch.ElapsedMilliseconds}ms");

(var xMap, var X, var yMap, var Y, var invXMap, var invYMap) = compressionMaps();

Console.WriteLine($"Compression complete by {watch.ElapsedMilliseconds}ms");

//create an array of the red tiles in the compressed coordinates
var comp = new short[lines.Length,2];
for (int l = 0; l < lines.Length; l++)
{
    comp[l, 0] = invXMap[redXs[l]];
    comp[l, 1] = invYMap[redYs[l]];
}

//draw the polygon on our compressed grid
var grid = new sbyte[X, Y];
for (int e = 0; e < lines.Length; e++)
{
    (var nextx, var nexty) = (comp[(e + 1) % lines.Length,0], comp[(e + 1) % lines.Length, 1]);
    if (nextx == comp[e,0])
        for (var y = comp[e,1]; y != nexty; y += (short) Math.Sign(nexty - comp[e,1]))
            grid[comp[e,0], y] = 1; //green
    else
        for (var x = comp[e,0]; x != nextx; x += (short) Math.Sign(nextx - comp[e,0]))
            grid[x, comp[e,1]] = 1; //green

    grid[comp[e,0], comp[e,1]] = 2; //red
}

Console.WriteLine($"Polygon drawn by {watch.ElapsedMilliseconds}ms");

//Flood fill with fast scan line algorithm
floodFillScanLine(grid, 0, 0);
floodFillScanLine(grid, X - 1, 0);
floodFillScanLine(grid, 0, Y - 1);
floodFillScanLine(grid, X - 1, Y - 1);

Console.WriteLine($"Grid flood filled by {watch.ElapsedMilliseconds}ms:");

//Using a Summed Area Table (https://en.wikipedia.org/wiki/Summed-area_table)
// Fill the grid in one pass using this recursion
// S(x,y) = i(x,y) + I(x,y-1) + I(x-1,y) - I(x-1,y-1)
// And calculate total points in a given bounding Box with:
// I(D) + I(A) - I(B) - I(C)
// = i(x1,y1) + i(x0 - 1,y0 - 1) - i(x0 - 1,y1) - i(x1, y0 - 1)

//start grid at 1 to provide a convenient 0 row / column that is all 0's
int[,] sums = new int[X + 1, Y + 1];
for (int y = 1; y <= Y ; y++)
    for (int x = 1; x <= X ; x++)
        sums[x, y] = ((grid[x - 1, y - 1] == -1) ? 1 : 0) + sums[x, y - 1] + sums[x - 1, y] - sums[x - 1, y - 1];

Console.WriteLine($"Prefix sums calculated by {watch.ElapsedMilliseconds}ms");

long best = 0;
for (int c1 = 0; c1 < lines.Length; c1++)
    for (int c2 = c1+1; c2 < lines.Length; c2++)
    {
        (var minY, var maxY) = comp[c1,1] < comp[c2,1] ? (comp[c1,1], comp[c2,1]) : (comp[c2,1], comp[c1,1]);
        if ((sums[comp[c2,0] + 1, maxY + 1] + sums[comp[c1,0], minY] 
            - sums[comp[c2,0] + 1, minY] - sums[comp[c1,0], maxY + 1]) == 0)
            best = Math.Max(best, rectArea(new Point(xMap[comp[c1,0]], yMap[comp[c1,1]]), new Point(xMap[comp[c2,0]], yMap[comp[c2,1]])));
    }

watch.Stop();
Console.WriteLine($"Best of {best} found in {watch.ElapsedMilliseconds}ms");

void floodFillScanLine(sbyte[,] grid, int x, int y)
{
    //see second to last example for a fast scan-line based recursive flood fill
    //https://lodev.org/cgtutor/floodfill.html
    
    (int X, int Y) = (grid.GetLength(0), grid.GetLength(1));
    if (grid[x, y] != 0)
        return;

    //fill in right and left of our starting position
    int x1 = x;
    while (x1 < X && grid[x1,y] == 0)
    {
        grid[x1,y] = -1;
        x1++;
    }
    x1 = x - 1;
    while (x1 >= 0 && grid[x1, y] == 0)
    {
        grid[x1, y] = -1;
        x1--;
    }

    //test for new scan lines above
    x1 = x;
    while (x1 < X && grid[x1,y] == -1)
    {
        if (y > 0 && grid[x1,y-1] == 0)
            floodFillScanLine(grid, x1, y - 1);
        x1++;
    }
    x1 = x - 1;
    while (x1 >= 0 && grid[x1,y] == -1)
    {
        if (y > 0 && grid[x1, y - 1] == 0)
            floodFillScanLine(grid, x1, y - 1);
        x1--;
    }

    //test for new scan lines below
    x1 = x;
    while (x1 < X && grid[x1, y] == -1)
    {
        if (y < (Y-1) && grid[x1, y + 1] == 0)
            floodFillScanLine(grid, x1, y + 1);
        x1++;
    }
    x1 = x - 1;
    while (x1 >= 0 && grid[x1, y] == -1)
    {
        if (y < (Y-1) && grid[x1, y + 1] == 0)
            floodFillScanLine(grid, x1, y + 1);
        x1--;
    }
}

(int[] xMap, int X, int[] yMap, int Y, Dictionary<int, short> invXMap, Dictionary<int, short> invYMap) compressionMaps()
{
    (var xMap, var X) = fastCompress(redXs);
    (var yMap, var Y) = fastCompress(redYs); 

    (var invXMap, var invYMap) = (new Dictionary<int, short>(), new Dictionary<int, short>());
    for (short x = 0; x < X; x++)
        invXMap.TryAdd(xMap[x], x);
    for (short y = 0; y < Y; y++)
        invYMap.TryAdd(yMap[y], y);

    return (xMap, X, yMap, Y, invXMap, invYMap);
}

(int[], int) fastCompress(int[] coords)
{
    //fast sort and dedupe into a single array, up to index is the sorted set, beyond that are the dupes
    int[] elements = new int[coords.Length];
    for (int i  = 0; i < coords.Length; i++)
        elements[i] = coords[i];
    
    Array.Sort(elements);
    
    // As in SortedSet<T> source code when initialised with a collection
    // Overwrite duplicates while shifting the distinct elements towards
    // the front of the array
    int index = 1;
    for (int i = 1; i < elements.Length; i++)
        if (elements[i] != elements[i - 1])
            elements[index++] = elements[i];

    return (elements, index);
}

(int[] xs, int[] ys) parseRedTiles(string[] lines)
{
    var xs = new int[lines.Length];
    var ys = new int[lines.Length];
    for (int l = 0; l < lines.Length; l++)
    {
        var numbers = lines[l].Split(',');
        xs[l] = int.Parse(numbers[0]);
        ys[l] = int.Parse(numbers[1]);
    }
    return (xs,ys);
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
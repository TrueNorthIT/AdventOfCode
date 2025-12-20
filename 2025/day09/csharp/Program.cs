using System.Diagnostics;
using Point = (long x, long y);

var watch = Stopwatch.StartNew();
var points = File.ReadAllLines("input.txt")
                .Select(line => line.Split(',').Select(long.Parse) switch { 
                    var sp => (x: sp.First() * 2, y: sp.Skip(1).First() * 2) })
            .ToArray();

var rectangles = from c1 in points from c2 in points 
                 where c1.x < c2.x || ((c1.x == c2.x) && c1.y < c2.y)
                 select (sides: sides(c1,c2), size: size(c1,c2));

Console.WriteLine($"Part 1: {rectangles.Max(tp => tp.size)} in {watch.ElapsedMilliseconds}ms");

watch.Restart();

//we treat the tiles as being centred on the integer coordinates as specified
//the outside edge is therefore +-0.5 from there
//if we treat our test rectangles as being on the integer cordinates
//then our edge cases go away and we will always have a line crossing when
//going in or out of the grid
//so first step is to walk the outside of the polygon checking which way we are turning
//and storing its boundary offset by +-0.5 as appropriate
//turns are always +-90
//  ___
//  ###  two right turns, edge is +1 = 3
//  # #
//
//  __#
//  ###  right then left turn edge is +0 = 2
//  #
//
//  #_#  two left turns, edge is -1 = 1
//  ###


//find the top left point and start CLOCKWISE, check if this is true for real input!
(var startIndex, var startPoint) = points.Index().OrderBy(p => p.Item.y).ThenBy(p => p.Item.x).First();
//if we are the top most point we must have just made a right turn if we are going clockwise
var prevTurnRight = true;

List<Point> boundary = [(x: startPoint.x - 1, y: startPoint.y - 1)];
for (int c = 1; c < points.Length; c++)
{
    var pi = points[(c + startIndex - 1) % points.Length];
    var ci = points[(c + startIndex) % points.Length];
    var ni = points[(c + startIndex + 1) % points.Length];
    var currVector = (x: ci.x - pi.x, y: ci.y - pi.y);
    var nextVector = (x: ni.x - ci.x, y: ni.y - ci.y);

    bool nextTurnRight = crossproduct(currVector, nextVector) < 0;

    //the length of our curent side depends if we are going R-R (+1), L-R / R-L (+0), L-L (-1)
    int delta = nextTurnRight && prevTurnRight 
                ? 2 : nextTurnRight ^ prevTurnRight ? 0 : -2;

    if (currVector.x == 0)
        if (currVector.y > 0)
            currVector = (0, currVector.y + delta);
        else
            currVector = (0, currVector.y - delta);
    else
        if (currVector.x > 0)
            currVector = (currVector.x + delta, 0);
        else
            currVector = (currVector.x - delta, 0);

    prevTurnRight = nextTurnRight;
    boundary.Add((boundary.Last().x + currVector.x, boundary.Last().y + currVector.y));
}

long best = 0;
foreach (var rect in rectangles.OrderByDescending(tp => tp.size))
{    
    foreach (var side in rect.sides)
    {
        for (int p = 0; p < boundary.Count; p++)
        {
            if (crosses(side.p1, side.p2, boundary[p], boundary[(p + 1) % points.Length]))
                goto skip;
        }
    }
    Console.WriteLine($"Part 2: {rect.size} in {watch.ElapsedMilliseconds}ms");
    return;
skip:;
}

(Point p1, Point p2)[] sides(Point p1, Point p2) => [
    ((p1.x, p1.y), (p1.x, p2.y)),
    ((p1.x, p2.y), (p2.x, p2.y)),
    ((p2.x, p2.y), (p2.x, p1.y)),
    ((p2.x, p1.y), (p1.x, p1.y)),
];

long size(Point p1, Point p2) => (1 + Math.Abs(p2.x - p1.x) / 2) * (1 + Math.Abs(p2.y - p1.y) / 2);

bool crosses(Point p1, Point p2, Point l1, Point l2) =>
    l1.x == l2.x 
        ?   ((p1.x <= p2.x && p1.x < l1.x && p2.x > l2.x)
                || (p2.x < l1.x && p1.x > l2.x))
            && ((l1.y <= l2.y && p1.y > l1.y && p1.y < l2.y)
                || (p1.y > l2.y && p1.y < l1.y))        
        :   ((p1.y < p2.y && p1.y < l1.y && p2.y > l2.y)
                || (p2.y < l1.y && p1.y > l2.y))
            && ((l1.x < l2.x && p1.x >= l1.x && p1.x <= l2.x)
                || p1.x >= l2.x && p1.x <= l1.x);

long crossproduct(Point p, Point l2) => l2.x * p.y - l2.y * p.x;

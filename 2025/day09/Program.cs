using System;

List<(double x, double y)> points = File.ReadAllLines("input.txt").Select(line => line.Split(','))
            .Select(arr => (double.Parse(arr[0]), double.Parse(arr[1])))
            .ToList();

var p1ans = (from p1 in points
 from p2 in points
 select (p1,p2,(1 + Math.Abs(p2.Item1 - p1.Item1)) * (1 + Math.Abs(p2.Item2 - p1.Item2)))).ToList();

Console.WriteLine(p1ans.MaxBy(tp => tp.Item3).Item3);


var rectangles = from c1 in points
           from c2 in points
           select (c1, c2);

//we have 4 sides of a rectangle
//  (p1.x,p1.y) -> (p1.x,p2.y)
//  (p1.x,p2.y) -> (p2.x,p2.y)
//  (p2.x,p2.y) -> (p2.x,p1.y)
//  (p2.x,p1.y) -> (p1.x,p1.y)

//rectangle is entirely inside if no side of polygon crosses any side of the rectangle

var start = points.Index().OrderBy(p => p.Item.y).ThenBy(p => p.Item.x).First();
//we know start point is a TL corner
var prevP = (x: start.Item.x - 0.5, y: start.Item.y - 0.5);
var prevTurnRight = true;
//assume we are going CLOCKWISE, and we turned right prev, check this for real input!
var polygonBoundary = new List<(double x, double y)> {
    prevP
};
for (int c = 1; c < points.Count; c++)
{
    var pi = points[(c + start.Index - 1) % points.Count];
    var ci = points[(c + start.Index) % points.Count];
    var ni = points[(c + start.Index + 1) % points.Count];
    var currVector = (x: ci.x - pi.x, y: ci.y - pi.y);
    var nextVector = (x: ni.x - ci.x, y: ni.y - ci.y);

    bool nextTurnRight = crossproduct(currVector, (0,0), nextVector) < 0;

    int delta = nextTurnRight && prevTurnRight 
                    ? 1 : nextTurnRight ^ prevTurnRight 
                          ? 0 : -1;

    //if next turn is a right turn, we want to move one more than our vector
    //otherwise just move the length of our vector
    if (currVector.x == 0)
    {
        currVector = (0, currVector.y + delta * currVector.y / Math.Abs(currVector.y));
    }
    else
    {
        currVector = (currVector.x + delta * currVector.x / Math.Abs(currVector.x), 0);
    }

    prevTurnRight = nextTurnRight;
    prevP = (prevP.x + currVector.x, prevP.y + currVector.y);
    polygonBoundary.Add(prevP);
}

var found = new List<((double x, double y) c1, (double x, double y) c2, double )>();
foreach (var rectangle in rectangles)
{
    bool valid = true;
    var minx = Math.Min(rectangle.c1.x, rectangle.c2.x);
    var maxx = Math.Max(rectangle.c1.x, rectangle.c2.x);
    var miny = Math.Min(rectangle.c1.y, rectangle.c2.y);
    var maxy = Math.Max(rectangle.c1.y, rectangle.c2.y);
    var s1 = (minx, miny);
    var s2 = (minx, maxy);
    var s3 = (maxx, maxy);
    var s4 = (maxx, miny);

    var sides = new [] { (s1,s2), (s2,s3), (s3,s4), (s4,s1) };

    foreach (var side in sides)
    {
        for (int p = 0; p < polygonBoundary.Count; p++)
        {
            var p1 = polygonBoundary[p];
            var p2 = polygonBoundary[(p + 1) % points.Count];

            if (crosses(side.Item1, side.Item2, p1, p2))
            {
                valid = false;
                break;
            }
        }
    }
    if (valid)
    {
        found.Add((rectangle.c1, rectangle.c2, (1 + Math.Abs(rectangle.c2.x - rectangle.c1.x)) * (1 + Math.Abs(rectangle.c2.y - rectangle.c1.y))));
    }
}

var p2ans = found.MaxBy(tp => tp.Item3);
Console.WriteLine(p2ans);



bool crosses((double x, double y) p1, (double x, double y) p2, (double x, double y) l1, (double x, double y) l2)
{
    //we have a line from l1 to l2
    //is p1 on one side of the line, and p2 on the other
    //all lines are either vertical or horizontal
    if (l1.x == l2.x && p1.x == p2.x)
        //both vertical, cannot cross
        return false;
    if (l1.y == l2.y && p1.y == p2.y)
        //both horizontal, cannot cross
        return false;

    if (l1.x == l2.x)
    {
        //polygon side is vertical, so two points are on a horizontal
        var sortedx = new[] { p1.x, p2.x }.OrderBy(x => x).ToArray();
        if (sortedx[0] < l1.x && sortedx[1] > l2.x)
        {
            //the horizontal points cross
            //is the vertical range within the line (incl.)
            var sortedy = new[] { l1.y, l2.y }.OrderBy(x => x).ToArray();
            if (p1.y >= sortedy[0] && p1.y <= sortedy[1])
            {
                return true;
            }
        }
        return false;
    }
    if (l1.y == l2.y)
    {
        var sortedy = new[] { p1.y, p2.y }.OrderBy(y => y).ToArray();
        if (sortedy[0] < l1.y && sortedy[1] > l2.y)
        {
            var sortedx = new[] { l1.x, l2.x };
            if (p1.x >= sortedx[0] && p1.x <= sortedx[1])
            {
                return true;
            }
        }
        return false;
    }

    throw new();
}
double crossproduct((double x, double y) p, (double x, double y) l1, (double x, double y) l2)
{
    var fx = l2.x - l1.x;
    var fy = l2.y - l1.y;
    return fx * (p.y - l1.y) - fy * (p.x - l1.x);
}

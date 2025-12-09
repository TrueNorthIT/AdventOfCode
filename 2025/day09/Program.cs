var points = File.ReadAllLines("input.txt")
                .Select(line => line.Split(',').Select(double.Parse) switch { 
                    var sp => (x: sp.First(), y: sp.Skip(1).First()) })
            .ToArray();

var rectangles = from c1 in points from c2 in points where c1.x < c2.x || c1.y < c2.y select (c1, c2);
Console.WriteLine($"Part 1: {rectangles.Max(tp => (1 + Math.Abs(tp.c2.x - tp.c1.x)) * (1 + Math.Abs(tp.c2.y - tp.c1.y)))}");

//rectangle is entirely inside if no side of polygon crosses any side of the rectangle
//however we must ensure we are checking against the outside of the polygon
//so first step is to walk the outside of the polygon storing its boundary

//find the TL corner to start at
var start = points.Index().OrderBy(p => p.Item.y).ThenBy(p => p.Item.x).First();
//and assume we are going CLOCKWISE, 0check this for real input!
var prevTurnRight = true;
var polygonBoundary = new List<(double x, double y)> {
     (x: start.Item.x - 0.5, y: start.Item.y - 0.5)
};

for (int c = 1; c < points.Length; c++)
{
    var pi = points[(c + start.Index - 1) % points.Length];
    var ci = points[(c + start.Index) % points.Length];
    var ni = points[(c + start.Index + 1) % points.Length];
    var currVector = (x: ci.x - pi.x, y: ci.y - pi.y);
    var nextVector = (x: ni.x - ci.x, y: ni.y - ci.y);

    bool nextTurnRight = crossproduct(currVector, (0,0), nextVector) < 0;

    //the length of our curent side depends if we are going R-R (+1), L-R / R-L (+0), L-L (-1)
    int delta = nextTurnRight && prevTurnRight 
                ? 1 :   nextTurnRight ^ prevTurnRight 
                        ? 0 : -1;

    if (currVector.x == 0)
        currVector = (0, currVector.y + delta * currVector.y / Math.Abs(currVector.y));
    else
        currVector = (currVector.x + delta * currVector.x / Math.Abs(currVector.x), 0);

    prevTurnRight = nextTurnRight;
    polygonBoundary.Add((polygonBoundary.Last().x + currVector.x, polygonBoundary.Last().y + currVector.y));
}

Console.WriteLine("Outline found");

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
            var p2 = polygonBoundary[(p + 1) % points.Length];

            if (crosses(side.Item1, side.Item2, p1, p2))
            {
                valid = false;
                goto skip;
            }
        }
    }
    found.Add((rectangle.c1, rectangle.c2, (1 + Math.Abs(rectangle.c2.x - rectangle.c1.x)) * (1 + Math.Abs(rectangle.c2.y - rectangle.c1.y))));
skip:;
}

var p2ans = found.MaxBy(tp => tp.Item3);
Console.WriteLine(p2ans);

bool crosses((double x, double y) p1, (double x, double y) p2, (double x, double y) l1, (double x, double y) l2)
{
    if (l1.x == l2.x)
    {
        //polygon side is vertical, so two points are on a horizontal
        var sortedx = new[] { p1.x, p2.x }.OrderBy(x => x).ToArray();
        if (sortedx[0] < l1.x && sortedx[1] > l2.x)
        {
            //the horizontal points cross
            //is the vertical range within the line (incl.)
            var sortedy = new[] { l1.y, l2.y }.OrderBy(x => x).ToArray();
            if (p1.y > sortedy[0] && p1.y < sortedy[1])
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

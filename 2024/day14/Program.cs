using System.Collections.Generic;

var W = 101;
var H = 103;
//var W = 11;
//var H = 7;
var STEPS = 100;

var robots = File.ReadAllLines("input.txt").Select(line => string.Concat(line.Where(ch => char.IsDigit(ch) || ch == ' ' || ch == '-' || ch == ','))
    .Split([" ", ","], StringSplitOptions.RemoveEmptyEntries).Select(int.Parse).ToList())
    .Select(arr => arr switch
    {
        [var px, var py, var vx, var vy] => (px,py, vx, vy)
    }).ToList();

List<(int x, int y)> final = robots.Select(robot => ((robot.px + STEPS * (robot.vx + W)) % W,
                  (robot.py + STEPS * (robot.vy + H)) % H)).ToList();

var quadrants = new int[] { 0, 0, 0, 0, 0 };
foreach (var robot in final)
{
    if ((robot.x == (W / 2) || robot.y == H / 2))
        quadrants[4]++;
    if ((robot.x < (W / 2) && robot.y < H / 2))
        quadrants[0]++;
    if ((robot.x < (W / 2) && robot.y > H / 2))
        quadrants[1]++;
    if ((robot.x > (W / 2) && robot.y < H / 2))
        quadrants[2]++;
    if ((robot.x > (W / 2) && robot.y > H / 2))
        quadrants[3]++;
}

var part1 = quadrants.Take(4).Aggregate(1, (acc, n) => acc * n);
Console.WriteLine($"Part 1: {part1}");
using System.Numerics;
using CacheKey = (System.Numerics.Complex fromPos, System.Numerics.Complex fromDir, System.Numerics.Complex toPos, System.Numerics.Complex toDir);
using QueueKey = (System.Numerics.Complex position, System.Numerics.Complex direction);

var grid = File.ReadAllText("input.txt").Split("\r\n")
        .SelectMany((line, r) => line.Select((ch, c) => (new Complex(r, c), ch)))
        .ToDictionary(tp => tp.Item1, tp => tp.ch);

(var S, var E) = (grid.Single(kvp => kvp.Value == 'S').Key, grid.Single(kvp => kvp.Value == 'E').Key);
(grid[S], grid[E]) = ('.', '.');

(var ccw, var cw) = (new Complex(0, 1), new Complex(0, -1));
var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) }; //E, S, W, N

var cache = new Dictionary<QueueKey, (int, HashSet<Complex> routes)>();
var queue = new PriorityQueue<CacheKey, int>();

//add a cache entry for the start square, telling us how we got there
cache.Add((S + dirs[2], dirs[0]), (0, new HashSet<Complex>([S])));
//and queue up our first move, we came from west of S, heading East
queue.Enqueue((S + dirs[2], dirs[0], S, dirs[0]), 0);

while (queue.Count > 0)
{
    //queue is prioritised by score
    //route is every square we have taken to reach the current position
    //including the current position
    queue.TryDequeue(out CacheKey tp, out int currScore);

    (int bestScore, HashSet<Complex> bestRoute) score;
    if (cache.TryGetValue((tp.toPos, tp.toDir), out score))
    {
        if (score.bestScore == currScore)
        {
            //we have a new way of reaching the same (square,dir) with the same score
            //merge the current route, with the new route
            //we can't have processed this yet so we can let be processed when it is dequeued
            score.bestRoute.UnionWith(score.bestRoute.Union(cache[(tp.fromPos, tp.fromDir)].routes));
            score.bestRoute.Add(tp.fromPos);
            continue;
        }
        else if (score.bestScore < currScore)
        {
            //we have done better
            continue;
        }
    }
    //we have a new best score for this square
    //we can overwrite the cache with the route of the square we came from plus the current position
    cache[(tp.toPos, tp.toDir)] = (currScore, cache[(tp.fromPos, tp.fromDir)].routes.Union([tp.toPos]).ToHashSet());
    
    if (grid[tp.toPos + tp.toDir] != '#')
        queue.Enqueue((tp.toPos, tp.toDir, tp.toPos + tp.toDir, tp.toDir), currScore + 1);

    queue.EnqueueRange( new [] { cw, ccw }.Select(rot => ((tp.toPos, tp.toDir, tp.toPos, tp.toDir * rot), currScore + 1000)));
}

var p1 = cache.Where(kvp => kvp.Key.position == E).Min(kvp => kvp.Value.Item1);
var bestRoutes = cache.Where(kvp => kvp.Key.position == E && kvp.Value.Item1 == p1).ToList();
var p2 = bestRoutes.SelectMany(kvp => kvp.Value.routes).ToHashSet();

printGrid(grid, S, p1, p2);
Console.WriteLine($"Part 1: {p1}");
Console.WriteLine($"Part 2: {p2.Count}");

void printGrid(Dictionary<Complex, char> grid, Complex position, int bestScore, HashSet<Complex> route)
{
    Console.WriteLine($"Best Score: {bestScore}, route length {route.Count}");
    var output = grid.GroupBy(kvp => kvp.Key.Real).OrderBy(grp => grp.Key).Select(grp => grp.OrderBy(g => g.Key.Imaginary).ToArray()).ToArray();
    var result = new System.Text.StringBuilder();
    foreach (var arr in output)
    {
        foreach (var kvp in arr)
            result.Append(kvp.Key == position ? '@' : route.Contains(kvp.Key) ? 'O' : kvp.Value);
        result.AppendLine();
    }
    result.AppendLine();
    Console.WriteLine(result);
}
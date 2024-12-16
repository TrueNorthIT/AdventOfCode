    using System.Numerics;
    using QueueKey = (System.Numerics.Complex fromPos, System.Numerics.Complex fromDir, System.Numerics.Complex toPos, System.Numerics.Complex toDir);
    using CacheKey = (System.Numerics.Complex position, System.Numerics.Complex direction);
    using CacheVal = (int score, System.Collections.Generic.HashSet<System.Numerics.Complex> visited);

    var grid = File.ReadAllText("input.txt").Split("\r\n")
        .SelectMany((line, r) => line.Select((ch, c) => (new Complex(r, c), ch)))
        .ToDictionary(tp => tp.Item1, tp => tp.ch);

    var ends = grid.Where(kvp => Char.IsLetter(kvp.Value)).ToDictionary(kvp => kvp.Value, kvp=> kvp.Key);

    (var ccw, var cw) = (new Complex(0, 1), new Complex(0, -1));
    var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) }; //E, S, W, N

    var cache = new [] { (new CacheKey(ends['S'] + dirs[2], dirs[0]), new CacheVal(0, new [] { ends['S'] }.ToHashSet())) }.ToDictionary();
    var queue = new PriorityQueue<QueueKey, int>([((ends['S'] + dirs[2], dirs[0], ends['S'], dirs[0]), 0)]);
    while (queue.TryDequeue(out QueueKey tp, out int currScore))
    {
        if (cache.TryGetValue((tp.toPos, tp.toDir), out CacheVal best) 
            && best.score <= currScore)
        {
            if (best.score == currScore)
                best.visited.UnionWith([tp.fromPos,..best.visited.Union(cache[(tp.fromPos, tp.fromDir)].visited)]);
            continue;
        }
        cache[(tp.toPos, tp.toDir)] = (currScore, cache[(tp.fromPos, tp.fromDir)].visited.Union([tp.toPos]).ToHashSet());
    
        if (grid[tp.toPos + tp.toDir] != '#')
            queue.Enqueue((tp.toPos, tp.toDir, tp.toPos + tp.toDir, tp.toDir), currScore + 1);

        queue.EnqueueRange( new [] { cw, ccw }.Select(rot => ((tp.toPos, tp.toDir, tp.toPos, tp.toDir * rot), currScore + 1000)));
    }

    var p1 = cache.Where(kvp => kvp.Key.position == ends['E']).Min(kvp => kvp.Value.Item1);
    var p2 = cache.Where(kvp => kvp.Key.position == ends['E'] && kvp.Value.Item1 == p1).SelectMany(kvp => kvp.Value.visited).ToHashSet();
    Console.WriteLine((p1,p2.Count));

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
    using System.Numerics;
    using Position = (System.Numerics.Complex pos, System.Numerics.Complex dir);
    using QueueState = ((System.Numerics.Complex pos, System.Numerics.Complex dir) from, (System.Numerics.Complex pos, System.Numerics.Complex dir) to);
    using State = (int score, System.Collections.Generic.HashSet<System.Numerics.Complex> visited);

    var grid = File.ReadAllText("input.txt").Split("\r\n")
        .SelectMany((line, r) => line.Select((ch, c) => (new Complex(r, c), ch)))
        .ToDictionary(tp => tp.Item1, tp => tp.ch);
    var ends = grid.Where(kvp => Char.IsLetter(kvp.Value)).ToDictionary(kvp => kvp.Value, kvp=> kvp.Key);

    (var ccw, var cw) = (new Complex(0, 1), new Complex(0, -1));
    var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) }; //E, S, W, N

    var cache = new [] { (new Position(ends['S'] + dirs[2], dirs[0]), new State(0, new [] { ends['S'] }.ToHashSet())) }.ToDictionary();
    var queue = new PriorityQueue<QueueState, int>([(((ends['S'] + dirs[2], dirs[0]), new Position(ends['S'], dirs[0])), 0)]);
    
    while (queue.TryDequeue(out QueueState tp, out int currScore))
    {
        if (cache.TryGetValue(tp.to, out State best)  && best.score <= currScore)
        {
            if (best.score == currScore)
                best.visited.UnionWith(best.visited.Union(cache[tp.from].visited));
            continue;
        }
        cache[tp.to] = (currScore, cache[tp.from].visited.Union([tp.to.pos]).ToHashSet());
    
        if (grid[tp.to.pos + tp.to.dir] != '#')
            queue.Enqueue((tp.to, (tp.to.pos + tp.to.dir, tp.to.dir)), currScore + 1);

        queue.EnqueueRange( new [] { cw, ccw }.Select(rot => ((tp.to, (tp.to.pos, tp.to.dir * rot)), currScore + 1000)));
    }

    var p1 = cache.Where(kvp => kvp.Key.pos == ends['E']).Min(kvp => kvp.Value.Item1);
    var p2 = cache.Where(kvp => kvp.Key.pos == ends['E'] && kvp.Value.score == p1).SelectMany(kvp => kvp.Value.visited).ToHashSet();

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
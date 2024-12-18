    using System.Numerics;

    var bytes = File.ReadAllText("input.txt").Split("\r\n")
            .Select((line, r) => {
                var sp = line.Split(",").Select(int.Parse).ToArray();
                return (new Complex(sp[0], sp[1]), r);
            }).ToDictionary();

    var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) };
    const int take = 1024; const int X = 70; const int Y = 70; var end = new Complex(X, Y);

    Console.WriteLine(solve(bytes).Where(bytes.ContainsKey).MinBy(point => bytes[point]));

    List<Complex> solve(Dictionary<Complex,int> bytes)
    {
        //queue is prioritised by the max t of a byte along its path (remember its a -'ve queue though)    
        var queue = new PriorityQueue<(Complex pos, List<Complex> route),int>();
        queue.Enqueue((new Complex(0, 0), new List<Complex>([new Complex(0, 0)])), int.MinValue);
        var visited = new HashSet<Complex>();
        while (queue.TryDequeue(out (Complex position, List<Complex> path) curr, out int priority))
        {
            if (!visited.Add(curr.position))
                continue;

            if (curr.position == end)
                return curr.path;

            foreach (var next in dirs.Select(dir => curr.position + dir).Where(inBounds))
                queue.Enqueue((next, curr.path.Concat([next]).ToList()), 
                    Math.Max(priority, -bytes.GetValueOrDefault(next, int.MaxValue))); //|MinValue| > |MaxValue|
        }
        throw new();
    }

    bool inBounds(Complex point) => (point.Real, point.Imaginary) switch {
        ( >= 0 and <= X, >= 0 and <= Y) => true,
        _ => false,
    };
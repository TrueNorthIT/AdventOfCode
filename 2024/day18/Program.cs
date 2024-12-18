using System.Numerics;

const int take = 1024;
const int X = 70;
const int Y = 70;

var bytes = File.ReadAllText("input.txt").Split("\r\n")
        .Select(line => {
            var sp = line.Split(",").Select(int.Parse).ToArray();
            return new Complex(sp[0], sp[1]);
        }).ToList();

System.Diagnostics.Stopwatch watch = System.Diagnostics.Stopwatch.StartNew();

var end = new Complex(X, Y);

var dirs = new Complex[] { new(0, 1), new(1, 0), new(0, -1), new(-1, 0) }; //E, S, W, N

var part1 = solve(bytes.Take(take).ToHashSet());
Console.WriteLine($"Part 1: {part1.Count - 1} in {watch.ElapsedMilliseconds}ms");

//repeatedly remove the next byte that lands on a cell on the optimum path
var i = 0;
var currentSet = bytes.Take(i).ToHashSet();
do
{
    var optimum = solve(currentSet);
    //optimum is the optimum path after the first i bytes have fallen
    if (!optimum.Any())
    {
        //answer is the i'th byte
        Console.WriteLine($"Part 2: {bytes.Skip(i - 1).First()} in {watch.ElapsedMilliseconds}ms");
        break;
    }
    i = bytes.Index().FirstOrDefault(tp => optimum.Contains(tp.Item)).Index + 1;

    Console.WriteLine($"Skipping to consider byte {i}");
}
while (i != default);

List <Complex> solve(HashSet<Complex> bytes)
{
    var queue = new Queue<(Complex, List<Complex>)>();
    queue.Enqueue((new Complex(0, 0), new List<Complex>([new Complex(0,0)])));
    var visited = new HashSet<Complex>();
    while (queue.TryDequeue(out (Complex position, List<Complex> path) curr))
    {
        if (visited.Contains(curr.position))
            continue;

        if (curr.position == end)
            return curr.path;

        visited.Add(curr.position);

        foreach (var next in dirs.Select(dir => curr.position + dir))
        {            
            if (!bytes.Contains(next) && inBounds(next))
                queue.Enqueue((next, curr.path.Concat([next]).ToList()));
        }
    }
    return new List<Complex>();
}

bool inBounds(Complex point) => (point.Real, point.Imaginary) switch {
    (>= 0 and <= X, >=0 and <= Y) => true,
    _ => false,
};
using System.Text;

var input = File.ReadAllLines("input.txt").Select(line => line.Split(' ') switch
{
    var arr =>
        (arr.First(), arr.Skip(1).Take(arr.Length - 2).ToArray(), arr.Skip(arr.Length - 1).Single())
});

var lights = input.Select(tp => tp.Item1[1..^1]).ToArray();

var buttons = input.Select(tp => tp.Item2.Select(
        button => button[1..^1].Split(',')
            .Select(int.Parse).ToArray()).ToArray()).ToArray();

var joltages = input.Select(tp => tp.Item3[1..^1].Split(',').Select(int.Parse).ToArray()).ToArray();


long solve(int index)
{
    Dictionary<string, long> cache = new();
    Queue<(string state, long presses)> queue = new();
    var first = (empty(lights[index].Length), 0);
    queue.Enqueue(first);
    
    while (queue.Count > 0)
    {
        (var state, var presses) = queue.Dequeue();
        if (cache.ContainsKey(state))
        {
            continue;
        }
        cache[state] = presses;
        if (state == lights[index])
        {
            return presses;
        }
        long best = long.MaxValue;
        foreach (var button in buttons[index])
        {
            var newLights = press(state, button);
            queue.Enqueue((newLights, presses + 1));            
        }
    }
    throw new();
}

var fewest = Enumerable.Range(0, lights.Length).Select(i => solve(i)).ToArray();
var p1 = fewest.Sum();
Console.WriteLine(p1);

string empty(int length) => new string(Enumerable.Repeat('.', length).ToArray());
string press(string before, int[] button)
{
    var res = new StringBuilder(before);
    foreach(var toggle in button)
    {
        res[toggle] = res[toggle] == '#' ? '.' : '#';
    }
    return res.ToString();
}


Console.WriteLine();
record State(string lights, long presses);

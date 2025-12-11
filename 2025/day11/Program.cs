var graph = File.ReadAllLines("input.txt").Select(line => line.Split(": ")).ToDictionary(arr => arr[0], arr => arr[1].Split(' ').ToArray());

var cache = new Dictionary<(string node, bool dac, bool fft), long>();
Console.WriteLine(ways(("svr", false, false)));

long ways((string node, bool dac, bool fft) key)
{
    if (key.node == "out")
        return key.dac && key.fft ? 1 : 0;

    if (cache.ContainsKey(key))
        return cache[key];

    long total = 0;
    foreach (var next in graph[key.node])
    {
        var newKey = (next, key.dac || next == "dac", key.fft || next == "fft");
        total += ways(newKey);
    }

    cache[key] = total;
    return total;
}
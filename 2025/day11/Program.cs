var graph = File.ReadAllLines("input.txt").Select(line => line.Split(": ")).ToDictionary(arr => arr[0], arr => arr[1].Split(' ').ToArray());
var cache = new Dictionary<(string node, bool dac, bool fft), long>();
Console.WriteLine(ways(("svr", false, false)));
long ways((string node, bool dac, bool fft) key) => key.node switch {
    "out" => key.dac && key.fft ? 1 : 0,
    _ when cache.ContainsKey(key) => cache[key],
    _ => cache[key] = graph[key.node].Sum(next => ways((next, key.dac || next == "dac", key.fft || next == "fft"))),
};

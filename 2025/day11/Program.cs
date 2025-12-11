using System.Collections.Concurrent;
using State = (string node, bool dac, bool fft);

var graph = File.ReadAllLines("input.txt").Select(line => line.Split(": "))
    .ToDictionary(arr => arr[0], arr => arr[1].Split(' ').ToArray());

Console.WriteLine(
    (ways(new (), ("you", true, true)), 
     ways(new (), ("svr", false, false))));

long ways(ConcurrentDictionary<State, long> cache, State key) => key.node == "out"
    ? (key.dac && key.fft ? 1 : 0)
    : cache.GetOrAdd(key,
        _ => graph[key.node].Sum(next =>
            ways(cache, (next, key.dac || next == "dac", key.fft || next == "fft"))));
var graph = File.ReadAllLines("input.txt").Select(line => line.Split(": ")).ToDictionary(arr => arr[0], arr => arr[1].Split(' ').ToArray());

var cache = new Dictionary<string, long>();
Console.WriteLine(ways("you"));

long ways(string node)
{
    if (node == "out")
        return 1;

    if (cache.ContainsKey(node))
        return cache[node];

    long total = graph[node].Sum(next => ways(next));

    cache[node] = total;
    return total;
}

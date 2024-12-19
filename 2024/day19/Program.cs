var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
var patterns = files[0].Split(", ").ToArray();
var designs = files[1].Split("\r\n");

var cache = new Dictionary<string, long>();

Console.WriteLine($"Part 1: {designs.Where(d => possible(d) > 0).Count()}");
Console.WriteLine($"Part 2: {designs.Sum(possible)}");

long possibleCached (string design)
{
    var res = possible(design);
    cache.TryAdd(design,res);
    return res;
}
long possible(string design) => design switch
{
    var empty when String.IsNullOrEmpty(design) => 1,
    var seen when cache.ContainsKey(design) => cache[design],
    var other => patterns.Where(p => design.StartsWith(p)).Sum(p => possibleCached(design[p.Length..])),
};

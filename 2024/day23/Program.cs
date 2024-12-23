var pairs = File.ReadAllLines("input.txt").Select(str => str.Split('-').OrderBy(str => str).ToArray())
    .Select(arr => (arr[0], arr[1]));

var computers = pairs.SelectMany(tp => new[] { tp.Item1, tp.Item2 }).Distinct()
    .ToDictionary(str => str, _ => new HashSet<string>());

foreach (var pair in pairs)
{
    computers[pair.Item1].Add(pair.Item2);
    computers[pair.Item2].Add(pair.Item1);
}

var threeSets = new HashSet<(string c1, string c2, string c3)>();
foreach ((string comp, HashSet<string> connectedTo) in computers)
{
    if (!comp.StartsWith("t"))
        continue;

    //we can generate some number of 3 sets depending on how many computers we are connected to
    //essentially select two from the list, and check they are all connected to each other
    foreach (var arr in (from c1 in connectedTo
    from c2 in connectedTo
    where c1 != c2 && computers[c1].Contains(c2) && computers[c2].Contains(c1)
    select new [] {comp, c1, c2 }.OrderBy(str => str).ToArray()))
    {
        threeSets.Add((arr[0], arr[1], arr[2]));
    }
}

var p1 = threeSets.Where(set => set.c1.StartsWith("t") || set.c2.StartsWith("t") || set.c3.StartsWith("t")).ToList();
Console.WriteLine(p1.Count);

//each computer is connected to X other computers, which we have in our list
//we take a computer, enumerate all the computers it is connected to
//and try adding each one to the set, with the condition it must connect to everything in our list already
List<(string computer, HashSet<string> connected)> results = new();
foreach ((string comp, HashSet<string> connectedTo) in computers)
{
    var  connectedSet = new HashSet<string>();
    connectedSet.Add(comp);
    foreach (var connection in connectedTo)
    {
        if (connectedSet.All(existing => computers[connection].Contains(existing)))
            connectedSet.Add(connection);
    }
    results.Add((comp, connectedSet));
}
var p2 = results.MaxBy(tp => tp.connected.Count).connected.OrderBy(str => str).ToArray();
var p2Ans = String.Join(",", p2);
Console.WriteLine(p2Ans);

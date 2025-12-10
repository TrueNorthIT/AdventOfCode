using System.Numerics;
using System.Text.RegularExpressions;

var lines = File.ReadAllLines("input.txt");
//var lines = File.ReadAllLines("demo.txt");
var presses = new List<int>();

foreach (var line in lines)
{
    
    var targetMatch = Regex.Match(line, @"\[([.#]+)\]");
    string targetStr = targetMatch.Groups[1].Value;
    int target = 0;
    
    for (int i = 0; i < targetStr.Length; i++)
    {
        if (targetStr[i] == '#') target += (1 << i);
    }
    
    var buttonMatches = Regex.Matches(line, @"\(([0-9,]+)\)");
    var currentSwitches = new List<int>();

    foreach (Match match in buttonMatches)
    {
        var nums = match.Groups[1].Value.Split(',').Select(int.Parse);
        int switchMask = 0;
        foreach (var num in nums)
        {
            switchMask += (1 << num);
        }
        currentSwitches.Add(switchMask);
    }
    
    int maxBitsPerSwitch = currentSwitches.Max(s => BitOperations.PopCount((uint)s));
    
    var result = AStar(target, currentSwitches.ToArray(), maxBitsPerSwitch);
    
    presses.Add(result.Value);
    Console.WriteLine($"Target [{targetStr}]: Solved in {result.Value}");
}

Console.WriteLine($"Total Minimal Presses: {presses.Sum()}");

static int? AStar(int target, int[] switches, int maxBitsPerSwitch)
{
    var map = new PriorityQueue<(int currentVal, int steps), float>();
    var visited = new Dictionary<int, int>();

    map.Enqueue((0, 0), 0);
    visited[0] = 0;

    while (map.Count > 0)
    {
        var (currentVal, steps) = map.Dequeue();

        if (currentVal == target) return steps;

        if (visited.ContainsKey(currentVal) && visited[currentVal] < steps)
            continue;

        foreach (var s in switches)
        {
            int nextVal = currentVal ^ s;
            int nextSteps = steps + 1;

            if (!visited.ContainsKey(nextVal) || visited[nextVal] > nextSteps)
            {
                visited[nextVal] = nextSteps;
                
                float h = (float)BitOperations.PopCount((uint)(nextVal ^ target)) / maxBitsPerSwitch;
                map.Enqueue((nextVal, nextSteps), nextSteps + h);
            }
        }
    }
    return null;
}
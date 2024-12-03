var line = File.ReadAllText("input.txt");
Console.WriteLine($"Part 1: {part1(line)}");

(bool enabled, int total, string remainder) = (true, 0, line); 
while (remainder != null)
{
    (remainder, int score, enabled) = processSegment(remainder, enabled);
    total += score;
}

Console.WriteLine($"Part 2: {total}");

int part1(string segment) => new System.Text.RegularExpressions.Regex(@"(mul\((\d{1,3}),(\d{1,3})\))").Matches(segment).Sum(match => int.Parse(match.Groups[2].Value) * int.Parse(match.Groups[3].Value));

(string remainder, int score, bool enabled) processSegment(string segment, bool enabled)
{
    string token = enabled ? "don't()" : "do()";
    var indexOf = segment.IndexOf(token);
    if (indexOf == -1)
    {
        return (null, enabled ? part1(segment) : 0, !enabled);
    }
    return (segment[indexOf..], enabled ? part1(segment[0..(indexOf - 1 + token.Length)]) : 0, !enabled);
}

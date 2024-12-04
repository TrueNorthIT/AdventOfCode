var line = File.ReadAllText("input.txt");
Console.WriteLine($"Part 1: {part1(line)}");
Console.WriteLine($"Part 1: {part2(line, "don't()")}");

int part1(string segment) => new System.Text.RegularExpressions.Regex(@"(mul\((\d{1,3}),(\d{1,3})\))").Matches(segment).Sum(match => int.Parse(match.Groups[2].Value) * int.Parse(match.Groups[3].Value));

int part2(string segment, string token) => (segment.IndexOf(token), token == "don't()") switch
{
    (_ ,_) when segment is null => 0,
    (-1, var enabled) => enabled ? part1(segment) : 0,
    (var index, var enabled) => (enabled ? part1(segment[0..index]) : 0) + part2(segment[index..], enabled ? "do()" : "don't()")
};
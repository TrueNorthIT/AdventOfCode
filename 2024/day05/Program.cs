﻿var file = File.ReadAllText("input.txt").Split($"{Environment.NewLine}{Environment.NewLine}");

var rules = file[0].Split(Environment.NewLine).Select(rule => { var sp = rule.Split("|"); return (int.Parse(sp[0]), int.Parse(sp[1])); }).ToHashSet();
var updates = file[1].Split(Environment.NewLine).Select(update => update.Split(",").Select(int.Parse).ToArray()).ToArray();

(int part1, int part2) tp = updates.Zip(updates.Select(arr => arr.OrderBy(i => i, new PageComparer(rules)).ToArray()))
            .Aggregate((0, 0),
                ((int p1, int p2) acc, (int[] First, int[] Second) tp) => 
                tp.First.SequenceEqual(tp.Second)
                    ? (acc.p1 + tp.First[tp.First.Length / 2], acc.p2)
                    : (acc.p1, acc.p2 + tp.Second[tp.Second.Length / 2]));

Console.WriteLine($"Answers: {tp}");

public class PageComparer(HashSet<(int, int)> rules) : IComparer<int>
{
    HashSet<(int, int)> Rules => rules;
    public int Compare(int x, int y) => rules.Contains((x, y)) ? -1 : 1;
}
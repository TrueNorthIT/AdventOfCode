var reports = File.ReadAllLines("input.txt").Select(line => line.Split(" ").Select(int.Parse).ToArray()).ToArray();

Console.WriteLine($"Part1: {reports.Count(isSafe)}");
Console.WriteLine($"Part2: {reports.Count(report => Enumerable.Range(0, report.Length).Select(i => report[0..i].Concat(report[(i + 1)..]).ToArray()).Any(isSafe))}");

bool isSafe(int[] report)
{
    int sign = Math.Sign(report[1] - report[0]);
    for (int i = 1; i < report.Length; i++)
    {
        int diff = Math.Abs(report[i] - report[i - 1]);
        if (diff < 1 || diff > 3 || Math.Sign(report[i] - report[i - 1]) != sign) return false;
    }
    return true;
}
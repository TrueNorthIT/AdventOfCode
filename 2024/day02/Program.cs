var reports = File.ReadAllLines("input.txt").Select(line => line.Split(" ").Select(int.Parse).ToArray());

Console.WriteLine($"Part1: {reports.Count(isSafe)}");
Console.WriteLine($"Part2: {reports.Count(report => 
    Enumerable.Range(0, report.Length).Select(i => 
        report[0..i].Concat(report[(i + 1)..]).ToArray())
    .Any(isSafe))}");

bool isSafe(int[] report) => report.Skip(1).Aggregate<int, (bool success, int prev)>(
        (true, report[0]),
        (acc, next) =>
            (Math.Abs(next - acc.prev) >= 1 && Math.Abs(next - acc.prev) <= 3
            && Math.Sign(next - acc.prev) == Math.Sign(report[1] - report[0])
            && acc.success,
        next)).success;
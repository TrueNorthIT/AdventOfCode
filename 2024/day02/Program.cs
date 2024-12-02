namespace Day02
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var reports = File.ReadAllLines("input.txt").Select(line => line.Split(" ").Select(int.Parse).ToArray()).ToArray();

            Console.WriteLine($"Part1: {reports.Count(isSafe)}");

            Console.WriteLine($"Part2: {reports.Count(isSafe2)}");
        }

        static bool isSafe2(int[] report)
        {
            for (int i = 0; i < report.Length; i++)
            {
                var r2 = report.ToList();
                r2.RemoveAt(i);
                if (isSafe(r2.ToArray()) == true)
                    return true;
            }

            return false;
        }

        static bool isSafe(int[] report)
        {
            int sign = Math.Sign(report[1] - report[0]);
            for (int i = 1; i < report.Length; i++)
            {
                int diff = Math.Abs(report[i] - report[i - 1]);
                if (diff < 1 || diff > 3) return false;
                if (Math.Sign(report[i] - report[i - 1]) != sign) return false;
            }
            return true;
        }
    }
}

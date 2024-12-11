using System.Linq;
namespace day11
{
    internal class Program
    {
        static void Main()
        {
            var stones = File.ReadAllLines("input.txt").First().Split(' ').Select(long.Parse);
            for (int i = 0; i < 25; i++) stones = Blink(stones);
            Console.WriteLine(stones.Count());
        }

        static IEnumerable<long> Blink(IEnumerable<long> stones)
        {
            return stones.SelectMany(s =>
            {
                string stoneString = s.ToString();
                if (s == 0) return new[] { 1l };
                else if (Math.DivRem(stoneString.Length, 2, out int remainder) >= 0 && remainder == 0)
                {
                     return [
                        long.Parse(stoneString.Substring(0, stoneString.Length / 2)),
                        long.Parse(stoneString.Substring(stoneString.Length / 2))
                    ];
                }
                return [s * 2024l];
            });
        }
    }
}

using System.Linq;
namespace day11
{
    internal class Program
    {
        static void Main()
        {
            var stones = File.ReadAllLines("input.txt").First().Split(' ').Select(long.Parse).ToArray();
            for (int i = 0; i < 75; i++)
            {
                stones = Blink(stones).ToArray();
                Console.WriteLine("{2:HH:mm:ss} Blinked {0:00} times, stones {1}", i, stones.LongLength, DateTime.Now);
            }
            Console.WriteLine(stones.LongLength);
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

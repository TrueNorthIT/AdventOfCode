using System.Numerics;
using System.Reflection.Emit;
using System.Text;

namespace day21
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var codes = File.ReadAllLines("input.txt");

            var p1 = solve(2, codes);
            Console.WriteLine($"Part 1: {p1}");
            var p2 = solve(25, codes);
            Console.WriteLine($"Part 2: {p2}");
        }

        static long solve(int noDirPads, string[] codes)
        {
            long ans = 0;
            foreach (var code in codes)
            {
                long outerTotal = 0;
                var outerPrev = 'A';
                foreach (var digit in code)
                {
                    var keyPadMoves = getKeyPadMoves(outerPrev, digit);
                    long minPerSeries = long.MaxValue;
                    foreach (var keyPadSeries in keyPadMoves)
                    {
                        //for a particular series we could try on the keypad
                        long total = 0;
                        var prev = 'A';
                        foreach (var ch in keyPadSeries)
                        {
                            var cache = new Dictionary<(char from, char to, int level, int maxLevel), long>();
                            total += _solveMemoize(prev, ch, 1, noDirPads + 1, cache);
                            prev = ch;
                        }
                        //now total is the min to press perform this sequence of presses after which everything has reset
                        minPerSeries = Math.Min(minPerSeries, total);
                    }
                    outerPrev = digit;
                    outerTotal += minPerSeries;
                }
                var numeric = int.Parse(new string(code.Where(ch => char.IsDigit(ch)).ToArray()));
                ans += numeric * outerTotal;
            }

            return ans;
        }

        static long _solveMemoize(char from, char to, int level, int maxLevel, Dictionary<(char from, char to, int level, int maxLevel), long> cache)
        {
            var key = (from, to, level, maxLevel);
            if (!cache.ContainsKey(key))
            {
                cache[key] = _solve(from, to, level, maxLevel, cache);
            }
            return cache[key];
        }

        static long _solve(char from, char to, int level, int maxLevel, Dictionary<(char from, char to, int level, int maxLevel), long> cache)
        {
            //for example, we want to press <, regardless of what level we are
            //we have two ways of doing this
            // <v<A, v<<A
            //after pressing each character, all the dpads ABOVE us are fully reset
            //so we need find the minimum cost way of pressing this character, and then pass that up to level + 1
            if (level < maxLevel)
            {
                var moves = getDirPadMoves(from, to);
                //this is all the possibilities, we find the minimum way to make each of these on the next level UP
                long minPresses = long.MaxValue;
                if (!moves.Any())
                    return 0;
                foreach (var move in moves)
                {
                    long total = 0;
                    var prev = 'A';
                    foreach (var ch in move)
                    {
                        var next = _solveMemoize(prev, ch, level + 1, maxLevel, cache);
                        prev = ch;
                        total += next;
                    }
                    minPresses = Math.Min(minPresses, total);
                }
                //we always need one more press at any particular level because we need to press A again
                return minPresses;
            }
            else
            {
                //we are on the final key pad, every press just takes 1
                return 1;
            }
        }

        static List<List<char>> getMoves((int r, int c) start, (int r, int c) end, int aRow)
        {
            var h = end.c - start.c;
            var hStr = h < 0 ? Enumerable.Repeat('<', Math.Abs(h)) : Enumerable.Repeat('>', Math.Abs(h));
            var v = end.r - start.r;
            var vStr = v > 0 ? Enumerable.Repeat('v', Math.Abs(v)) : Enumerable.Repeat('^', Math.Abs(v));
            var vFirst = new string(vStr.Concat(hStr).ToArray());
            var hFirst = new string(hStr.Concat(vStr).ToArray());

            List<List<char>> res = null;
            //if we start on the A row and finish on the first col we cannot do too many h moves first
            if (start.r == aRow && end.c == 0)
            {
                if (aRow == 0)
                {
                }
                var cantStartWith = new String(Enumerable.Repeat(hFirst[0], start.c - end.c).ToArray());
                res = Permutations(vFirst).Where(str => !str.StartsWith(cantStartWith)).Distinct().Select(str => str.ToList()).ToList();
            }
            //and if we end on the A row and start on the first col we cannot do too many v moves first
            else if (end.r == aRow && start.c == 0)
            {
                if (aRow == 0)
                {
                }
                var cantStartWith = new String(Enumerable.Repeat(vFirst[0], Math.Abs(end.r - start.r)).ToArray());
                res = Permutations(hFirst).Where(str => !str.StartsWith(cantStartWith)).Distinct().Select(str => str.ToList()).ToList();                    
            }
            else if (aRow == 3)
            {
                res = Permutations(hFirst).Distinct().Select(str => str.ToList()).ToList();
            }
            else
            {
                res = Permutations(hFirst).Distinct().Select(str => str.ToList()).ToList();
            }
            return res;
        }

        private static List<string> Permutations(string set)
        {
            var output = new List<string>();
            if (set.Length == 1)
            {
                output.Add(set);
            }
            else
            {
                foreach (var c in set)
                {
                    var tail = set.Remove(set.IndexOf(c), 1);
                    foreach (var tailPerms in Permutations(tail))
                    {
                        output.Add(c + tailPerms);
                    }
                }
            }
            return output;
        }

        static List<List<char>> getDirPadMoves(char start, char end)
        {
            var moves = getMoves(dirPadCoords(start), dirPadCoords(end), 0).Select(str => str.Concat(['A']).ToList()).ToList();
            if (!moves.Any())
            {
                return new List<List<char>>(new [] {new List<char>() { 'A' } });
            }
            return moves;
        } 

        static List<List<char>> getKeyPadMoves(char start, char end)
            => getMoves(keyPadCoords(start), keyPadCoords(end), 3).Select(str => str.Concat(['A']).ToList()).ToList();

        static (int r, int c) keyPadCoords(char key) => key switch
        {
            '7' => (0, 0),
            '8' => (0, 1),
            '9' => (0, 2),
            '4' => (1, 0),
            '5' => (1, 1),
            '6' => (1, 2),
            '1' => (2, 0),
            '2' => (2, 1),
            '3' => (2, 2),
            '0' => (3, 1),
            'A' => (3, 2),
        };

        static (int r, int c) dirPadCoords(char key) => key switch
        {
            '^' => (0, 1),
            'A' => (0, 2),
            '<' => (1, 0),
            'v' => (1, 1),
            '>' => (1, 2),
        };
    }
}

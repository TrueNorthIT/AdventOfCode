using System.Reflection.Emit;
using System.Text;

namespace day21
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var codes = File.ReadAllLines("input.txt");
            var p1Solutions = solve(codes, 2);
            var p1Answer = p1Solutions.Sum(tp => tp.solution.Length * int.Parse(new string(tp.code.Where(ch => char.IsDigit(ch)).ToArray())));
            foreach (var sol in p1Solutions)
            {
                Console.WriteLine(sol);
            }
            Console.WriteLine($"Part 1: {p1Answer}");
            var p2Solutions = solve(codes, 5);
            var p2Answer = p2Solutions.Sum(tp => tp.solution.Length * int.Parse(new string(tp.code.Where(ch => char.IsDigit(ch)).ToArray())));
            Console.WriteLine($"Part 2: {p2Answer}");
        }

        static List<(string code, string solution)> solve(string[] codes, int noPads)
        {
            var solutions = new List<(string code, string solution)>();
            foreach (var code in codes)
            {
                var moves = expand(new List<string>() { code }, true);
                int l = 0;
                for (int pads = 0; pads < noPads; pads++)
                {
                    Console.WriteLine($"Expanding {pads}");
                    moves = expand(moves, false);
                    Console.WriteLine($"String length: {moves[0].Length}, moves count {moves.Count}");
                    l = moves.MinBy(str => str.Length).Length;
                    moves = moves.Where(str => str.Length == l).ToList();
                }
                moves = moves.Where(str => str.Length == l).ToList();
                solutions.Add((code, moves.First()));
            }
            return solutions;
        }

        static List<string> expand(List<string> moves, bool keyPad)
        {
            //level 1 example we start on A, we move to <, and we press it = <A
            //level 2 example we start on A, we move to < (v<<), we press it (A), we move to A (>>^), we press it (A)
            // -> V<<A>>^A
            var expanded = new List<string>();
            foreach (var move in moves)
            {
                //build the new list of possibilities to enter this move on the dir pad above
                //e.g. the first would be <A
                var newMoves = new List<StringBuilder>();
                var prevChar = 'A';
                foreach (var ch in move)
                {
                    var dirPadMoves = keyPad ? getKeyPadMoves(prevChar, ch) : getDirPadMoves(prevChar, ch);
                    if (!newMoves.Any())
                        newMoves.AddRange(dirPadMoves.Select(str => new StringBuilder(str)));
                    else if (dirPadMoves.Count > 1)
                    {
                        //we append these moves to the previous set
                        newMoves = newMoves.SelectMany(preMove => dirPadMoves.Select(newMove =>
                        {
                            var sb = new StringBuilder(preMove.ToString());
                            sb.Append(newMove);
                            return sb;
                        })).ToList();
                        Console.WriteLine($"Expanded {dirPadMoves.Count} options");
                    }
                    else
                    {
                        foreach (var sb in newMoves)
                        {
                            sb.Append(dirPadMoves[0]);
                        }
                    }
                    prevChar = ch;
                }
                expanded.AddRange(newMoves.Select(sb => sb.ToString()));
            }

            return expanded;
        }
        static List<string> getMoves((int r, int c) start, (int r, int c) end, int aRow)
        {
            var h = end.c - start.c;
            var hStr = h < 0 ? Enumerable.Repeat('<', Math.Abs(h)) : Enumerable.Repeat('>', Math.Abs(h));
            var v = end.r - start.r;
            var vStr = v > 0 ? Enumerable.Repeat('v', Math.Abs(v)) : Enumerable.Repeat('^', Math.Abs(v));
            var vFirst = new string(vStr.Concat(hStr).ToArray());
            var hFirst = new string(hStr.Concat(vStr).ToArray());

            //if we start on the A row and finish on the first col we must do the v moves first
            //and if we end on the bottom row and start on the first col we must do the > moves first
            if (start.r == aRow && end.c == 0)
                return [vFirst];
            else if (end.r == aRow && start.c == 0)
                return [hFirst];
            else if (aRow == 3)
                //otherwise we can do either
                //some might be make higher steps quicker so return both
                return new[] { hFirst, vFirst }.Distinct().ToList();
            else
                //order NEVER matters on a dirPad
                return new[] { hFirst }.Distinct().ToList();
        }

        static List<string> getDirPadMoves(char start, char end)
            => getMoves(dirPadCoords(start), dirPadCoords(end), 0).Select(str => $"{str}A").ToList();

        static List<string> getKeyPadMoves(char start, char end)
            => getMoves(keyPadCoords(start), keyPadCoords(end), 3).Select(str => $"{str}A").ToList();

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

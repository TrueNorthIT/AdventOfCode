namespace day21
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var codes = File.ReadAllLines("input.txt");
            int p1 = 0;
            foreach (var code in codes)
            {
                var moves1 = expand(new List<string>() { code }, true);
                var moves2 = expand(moves1, false);
                var moves3 = expand(moves2, false);
                var l = moves3.MinBy(str => str.Length).Length;
                var numeric = int.Parse(new string(code.Where(ch => char.IsDigit(ch)).ToArray()));
                p1 += numeric * l;
            }
            Console.WriteLine($"Part 1: {p1}");
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
                var newMoves = new List<string>();
                var prevChar = 'A';
                foreach (var ch in move)
                {
                    var dirPadMoves = keyPad ? getKeyPadMoves(prevChar, ch) : getDirPadMoves(prevChar, ch);
                    if (!newMoves.Any())
                        newMoves.AddRange(dirPadMoves);
                    else
                        //we append these moves to the previous set
                        newMoves = newMoves.SelectMany(preMove => dirPadMoves.Select(newMove => $"{preMove}{newMove}")).ToList();
                    prevChar = ch;
                }
                expanded.AddRange(newMoves);
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
            else
                //otherwise we can do either
                //some might be make higher steps quicker so return both
                return new [] { hFirst, vFirst }.Distinct().ToList();
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

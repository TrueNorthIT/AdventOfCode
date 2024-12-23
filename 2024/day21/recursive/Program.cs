using System.Collections.Concurrent;
var codes = File.ReadAllLines("input.txt");

ConcurrentDictionary<(char from, char to, int level, int maxLevel), long> cache = new();

var p1 = solve(2, codes);
Console.WriteLine($"Part 1: {p1}");
var p2 = solve(25, codes);
Console.WriteLine($"Part 2: {p2}");

long solve(int noDirPads, string[] codes) => codes.AsParallel().Select(code =>
        new[] { 'A' }.Concat(code).Zip(code).Sum(tp => _solveMemoize(tp.First, tp.Second, 0, noDirPads))
        * int.Parse(new string(code.Where(char.IsDigit).ToArray()))).Sum();

long _solveMemoize(char from, char to, int level, int maxLevel) 
    => cache.GetOrAdd((from, to, level, maxLevel), 
        _ => _solve(from, to, level, maxLevel));

long _solve(char from, char to, int level, int maxLevel) => level switch {
    var dirPad when level <= maxLevel 
        => (level == 0 ? getKeyPadMoves(from, to) : getDirPadMoves(from, to)) switch {
            var moves => moves.Any() ? moves.Min(move => new[] { 'A' }.Concat(move).Zip(move).Sum(tp => _solveMemoize(tp.First, tp.Second, level + 1, maxLevel))) : 0,
    },
    var keyPad => 1,
};

IEnumerable<IEnumerable<char>> getMoves((int r, int c) start, (int r, int c) end, int aRow)
{
    var h = end.c - start.c;
    var hStr = h < 0 ? Enumerable.Repeat('<', Math.Abs(h)) : Enumerable.Repeat('>', Math.Abs(h));
    var v = end.r - start.r;
    var vStr = v > 0 ? Enumerable.Repeat('v', Math.Abs(v)) : Enumerable.Repeat('^', Math.Abs(v));
    var moves = new string(vStr.Concat(hStr).ToArray());

    string cantStartWith = (start.r, end.r, start.c, end.c) switch
    {
        var vFirst when start.r == aRow && end.c == 0 => new String(Enumerable.Repeat(hStr.First(), Math.Abs(h)).ToArray()),
        var hFirst when end.r == aRow && start.c == 0 => new String(Enumerable.Repeat(vStr.First(), Math.Abs(v)).ToArray()),
        _ => "*",
    };
    return Permutations(moves).Where(str => !str.StartsWith(cantStartWith)).Distinct();
}

IEnumerable<IEnumerable<char>> getDirPadMoves(char start, char end) => 
    getMoves(dirPadCoords(start), dirPadCoords(end), 0).Select(str => str.Concat(['A'])) switch {
        var moves => !moves.Any() ? [['A']] : moves
    };

IEnumerable<IEnumerable<char>> getKeyPadMoves(char start, char end)
    => getMoves(keyPadCoords(start), keyPadCoords(end), 3).Select(str => str.Concat(['A']));

(int r, int c) keyPadCoords(char key) => key switch
{
    '7' or '8' or '9' => (0, key - '7'),
    '4' or '5' or '6' => (1, key - '4'),
    '1' or '2' or '3' => (2, key - '1'),
    '0' => (3, 1),
    'A' => (3, 2),
};

(int r, int c) dirPadCoords(char key) => key switch
{
    '^' => (0, 1),
    'A' => (0, 2),
    '<' => (1, 0),
    'v' => (1, 1),
    '>' => (1, 2),
};

//copied from stackoverflow as quite frankly I have written enough code for this one already!
List<string> Permutations(string set)
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

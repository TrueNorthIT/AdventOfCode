using System.Collections.Immutable; //because it's fluent...
using Point = (int r, int c);
using Move = ((int r, int c) from, (int r, int c) to, char ch);
using Grid = System.Collections.Immutable.ImmutableDictionary<(int r, int c), char>;
using KVP = System.Collections.Generic.KeyValuePair<(int r, int c), char>;

var dirs = "^v<>".Zip([(-1, 0), (1, 0), (0, -1), (0, 1)]).ToDictionary<char,Point>();
(var grid, var moves) = File.ReadAllText("input.txt").Split("\r\n\r\n")  switch { var files => 
    (files[0].Split("\r\n").SelectMany((line, r) => line.Select((ch, c) => new KVP((r, c), ch)))
        .ToImmutableDictionary(),
    files[1].ReplaceLineEndings(""))};

Console.WriteLine(
    (solve( grid: grid, 
            start: grid.Single(kvp => kvp.Value == '@').Key)
    .Sum(kvp => kvp.Value == 'O' ? 100 * kvp.Key.r + kvp.Key.c : 0), 
    solve(  grid: grid.SelectMany(kvp =>
                new KVP[] { new ((kvp.Key.r, kvp.Key.c * 2), kvp.Value == 'O' ? '[' : kvp.Value),
                            new ((kvp.Key.r, kvp.Key.c * 2 + 1), kvp.Value == 'O' ? ']' : kvp.Value)})
            .ToImmutableDictionary(),
            start: grid.Single(kvp => kvp.Value == '@').Key switch { var st => (st.r, st.c * 2) })
    .Sum(kvp => kvp.Value == '[' ? 100 * kvp.Key.r + kvp.Key.c : 0)));

Grid solve(Grid grid, Point start) 
    => moves.Aggregate((grid: grid.ToImmutableDictionary(), curr: start), (acc, m) 
    => step(acc.grid, acc.curr, m) switch { 
        (true, var next, var updates) => 
            (acc.grid.SetItems(updates.Select(tp => new KVP(tp.from, '.'))
            .Concat(updates.Select(tp => new KVP(tp.to, tp.ch)))), next),
        (false, var next, _) => (acc.grid, next)
    }, acc => acc.grid);

(bool success, Point position, List<Move> moves) step(Grid grid, Point start, char move) 
    => (start.r + dirs[move].r, start.c + dirs[move].c) switch { (int r, int c) next
    => grid[next] switch { var ch => ch switch {
    '.' or '@' => (true, next, [(start, next, grid[start])]),
        '#' => (false, start, []),
        var box when ch == 'O' || move == '>' || move == '<'
            => step(grid, next, move) switch { var st
            => st.success
                ? (true, next, [(start, next, grid[start]), .. st.moves])
                : (false, start, [])},
        '[' or ']'
            => step(grid, (r, c - (ch == ']' ? 1 : 0)), move) switch { var st1
            => step(grid, (r, c + (ch == '[' ? 1 : 0)), move) switch { var st2
            => st1.success && st2.success
                ? (true, next, [(start, (r, c), grid[start]), .. st1.moves, .. st2.moves])
                : (false, start, []) } } } } };
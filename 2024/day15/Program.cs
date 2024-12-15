using Point = (int r, int c);
using Move = ((int r, int c) from, (int r, int c) to, char ch);
using Grid = System.Collections.Generic.Dictionary<(int r, int c), char>;

var dirs = new Dictionary<char, (int r, int c)>() 
    { { '^', (-1, 0) }, { 'v', (1, 0) }, { '<', (0, -1) }, { '>', (0, 1) } };

(var grid, var moves) = File.ReadAllText("input.txt").Split("\r\n\r\n")  switch { var files => 
    (files[0].Split("\r\n").SelectMany((line, r) => line.Select((ch, c) => ((r, c), ch))).ToDictionary(),
    files[1].ReplaceLineEndings(""))};

Console.WriteLine((part1(), part2()));

double part1() => solve(grid, grid.Single(kvp => kvp.Value == '@').Key)
    .Where(kvp => kvp.Value == 'O').Sum(kvp => 100 * kvp.Key.r + kvp.Key.c);
    
double part2() => solve(
    grid: grid.SelectMany(kvp => 
    new[] { ((kvp.Key.r, kvp.Key.c * 2), kvp.Value == 'O' ? '[' : kvp.Value),
            ((kvp.Key.r, kvp.Key.c * 2 + 1), kvp.Value == 'O' ? ']' : kvp.Value)})
        .ToDictionary(kvp => kvp.Item1, kvp => kvp.Item2),
    start: grid.Single(kvp => kvp.Value == '@').Key switch { var st => (st.r, st.c * 2) })
.Where(kvp => kvp.Value == '[')
.Sum(kvp => 100 * kvp.Key.r + kvp.Key.c);

Grid solve(Grid grid, Point start) 
    => moves.Aggregate((grid: new Grid(grid), curr: start), (acc, m) 
    => step(acc.grid, acc.curr, m) switch { 
        (true, var next, var updates) => 
            (Update(acc.grid, updates.Select(tp => (tp.from, '.'))
            .Concat(updates.Select(tp => (tp.to, tp.ch)))), next),
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

Grid Update(Grid grid, IEnumerable<(Point, char)> items) {
    foreach (var item in items) grid[item.Item1] = item.Item2; return grid; }
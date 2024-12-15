﻿    using Point = (int r, int c);
    using Grid = System.Collections.Generic.Dictionary<(int r, int c), char>;

    var dirs = new Dictionary<char, (int r, int c)>() 
        { { '^', (-1, 0) }, { 'v', (1, 0) }, { '<', (0, -1) }, { '>', (0, 1) } };

    (var grid, var moves) = File.ReadAllText("input.txt").Split("\r\n\r\n")  switch { var files => 
        (files[0].Split("\r\n").SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => (tp.r, tp.c), tp => tp.ch),
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
        => moves.Aggregate((grid: new Grid(grid), curr: start), (acc, m) => {
        (var success, var next, var updates) = step(acc.grid, acc.curr, m);
            if (success)
            {
                foreach (var update in updates)
                    acc.grid[update.from] = '.';
                foreach (var update in updates)
                    acc.grid[update.to] = update.ch;
            }
            return (acc.grid, next);
        }, acc => acc.grid);

    (bool success, Point position, List<(Point from, Point to, char ch)> moves)
    step(Grid grid, Point start, char move) 
        => (start.r + dirs[move].r, start.c + dirs[move].c) switch { var next 
        => grid[next] switch { var ch => ch switch {
            '.' or '@' => (true, next, [(start, next, grid[start])]),
            '#' => (false, start, []),
            var box when ch == 'O' || move == '>' || move == '<'
                => step(grid, next, move) switch { var st
                => st.success
                    ? (true, next, [(start, next, grid[start]), .. st.moves])
                    : (false, start, [])
                },
            '[' or ']' 
                => step(grid, (next.Item1, next.Item2 - (ch == ']' ? 1 : 0)), move) switch { var st1
                => step(grid, (next.Item1, next.Item2 + (ch == '[' ? 1 : 0)), move) switch { var st2
                => st1.success && st2.success
                    ? (true, next, [(start, next, grid[start]), .. st1.moves, .. st2.moves])
                    : (false, start, [])}}}}};

//void showGrid(Dictionary<Complex,char> grid, Complex robot)
//{
//    var R = (int)grid.Max(kvp => kvp.Key.Real);
//    var C = (int)grid.Max(kvp => kvp.Key.Imaginary);
//    var output = new char[R + 1][];
//    for (int r = 0; r <= R; r++)
//        output[r] = new char[C + 1];

//    foreach (var square in grid)
//    {
//        output[(int)square.Key.Real][(int)square.Key.Imaginary] = square.Value;
//    }
//    output[(int)robot.Real][(int)robot.Imaginary] = '@';

//    var result = new System.Text.StringBuilder();
//    foreach (var arr in output)
//    {
//        foreach (var ch in arr)
//            result.Append(ch);
//        result.AppendLine();
//    }
//    result.AppendLine();
//    Console.WriteLine(result.ToString());
//}
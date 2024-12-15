    using System.Numerics;
    var dirs = new Dictionary<char, Complex>() 
        { { '^', new (-1, 0) }, { 'v', new (1, 0) }, { '<', new (0, -1) }, { '>', new (0, 1) } };

    var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
    (var initialGrid, var moves) = 
        (files[0].Split("\r\n")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch),
            files[1].ReplaceLineEndings(""));

    var start = initialGrid.Single(kvp => kvp.Value == '@').Key;
    initialGrid[start] = '.';

    Console.WriteLine((part1(), part2()));

    double part1() => solve(initialGrid, start)
        .Where(kvp => kvp.Value == 'O').Sum(kvp => 100 * kvp.Key.Real + kvp.Key.Imaginary);
    
    double part2() => solve(new Dictionary<Complex, char>(
        initialGrid.SelectMany(kvp => new KeyValuePair<Complex, char>[]
            {   new (new (kvp.Key.Real, kvp.Key.Imaginary * 2), kvp.Value switch { 'O' => '[', _ => kvp.Value }),
                new (new (kvp.Key.Real, kvp.Key.Imaginary * 2 + 1), kvp.Value switch { 'O' => '[', _ => kvp.Value })})), 
        new (start.Real, start.Imaginary * 2))
    .Where(kvp => kvp.Value == '[')
    .Sum(kvp => 100 * kvp.Key.Real + kvp.Key.Imaginary);

    Dictionary<Complex, char> solve(Dictionary<Complex, char> initialGrid, Complex start)
    {
        var grid = new Dictionary<Complex, char>(initialGrid);
        var curr = start;
        foreach (var m in moves)
        {
            (var succ, curr, var updates) = step(grid, curr, m);
            if (succ)
            {
                foreach (var update in updates)
                    grid[update.from] = '.';
                foreach (var update in updates)
                    grid[update.to] = update.ch;
            }
        }
        return grid;
    }

    (bool success, Complex next, List<(Complex from, Complex to, char ch)> moves)
        step(Dictionary<Complex, char> grid, Complex start, char move) 
        => (start + dirs[move]) switch { var next => grid[next] switch { var chNext => chNext switch {
            '.' => (true, next, [(start, next, grid[start])]),
            '#' => (false, start, []),
            var box when chNext == 'O' || move == '>' || move == '<'
                => step(grid, next, move) switch { var moves
                => moves.success
                    ? (true, next, [(start, next, grid[start]), .. moves.moves])
                    : (false, start, [])
                },
            '[' or ']' 
                => step(grid, next - (chNext == ']' ? new Complex(0, 1) : 0), move) switch { var move1
                => step(grid, next + (chNext == '[' ? new Complex(0, 1) : 0), move) switch { var move2 
                => move1.success && move2.success
                    ? (true, next, [(start, next, grid[start]), .. move1.moves, .. move2.moves])
                    : (false, start, [])
            }}}}};

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
using System.Numerics;
var dirs = new Complex[] { new(-1, 0), new(1, 0), new(0, -1), new(0, 1) };

var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
var parseGrid = () => files[0].Split("\r\n")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var grid = parseGrid();
Complex start = grid.Single(kvp => kvp.Value == '@').Key; 
grid[start] = '.';
var moves = files[1].ReplaceLineEndings("");

solve(start);
var p1 = grid.Where(kvp => kvp.Value == 'O').Sum(kvp => 100 * kvp.Key.Real + kvp.Key.Imaginary);
Console.WriteLine($"Part 1: {p1}");

grid = parseGrid();
grid[start] = '.';

var newGrid = new Dictionary<Complex, char>();
foreach (var kvp in grid)
{
    switch (kvp.Value)
    {
        case '#':
        case '.':
            newGrid.Add(new Complex(kvp.Key.Real, kvp.Key.Imaginary * 2), kvp.Value);
            newGrid.Add(new Complex(kvp.Key.Real, kvp.Key.Imaginary * 2 + 1), kvp.Value);
            break;
        case 'O':
            newGrid.Add(new Complex(kvp.Key.Real, kvp.Key.Imaginary * 2), '[');
            newGrid.Add(new Complex(kvp.Key.Real, kvp.Key.Imaginary * 2 + 1), ']');
            break;
    }
}
start = new Complex(start.Real, start.Imaginary * 2);
grid = newGrid;
solve(start);

void solve(Complex start)
{
    var curr = start;
    foreach (var m in moves)
    {
        (var success, curr, var updates) = move2(curr, m);
        if (success)
        {
            foreach (var update in updates)
                grid[update.from] = '.';
            foreach (var update in updates)
                grid[update.to] = update.ch;
        }
    }
}

var R = grid.MaxBy(kvp => kvp.Key.Real).Key.Real;
var C = grid.MaxBy(kvp => kvp.Key.Imaginary).Key.Imaginary;
var p2 = grid.Where(kvp => kvp.Value == '[').Sum(kvp =>
{
    return 100 * kvp.Key.Real + kvp.Key.Imaginary;
});

Console.WriteLine($"Part 2: {p2}");

(bool success, Complex next, List<(Complex from, Complex to, char ch)> moves) move2(Complex start, char move)
{
    var dir = move switch
    {
        '^' => dirs[0],
        'v' => dirs[1],
        '<' => dirs[2],
        '>' => dirs[3],
    };

    var horizontal = move switch
    {
        '>' or '<' => true,
        _ => false
    };

    //i is the start of our chain, and starting chain length is 1
    switch (grid[start + dir])
    {
        //the end of our chain has been pushed into free space
        //start would move forward one, end forward one
        case '.':
            //the start of our chain moves forward
            //the free space gets replaced by whatever was before it
            return (true, start + dir, [(start, start + dir, grid[start])]);
        case '#':
            //we have hit an obstruction, no moves to add
            return (false, start, []);
        case 'O':
        case var box when horizontal:
            //we are pushing on a length of wall horizontally
            //no moves to add as only start and end of a chain of walls ever move   .OOO. -> ..OOO   ..[][]..[].. -> ...[][].[].
            var moves = move2(start + dir, move);
            if (moves.success)
            {
                return (true, start + dir, [(start, start + dir, grid[start]), .. moves.moves]);
            }
            return (false, start, []);
        case '[':
            {
                //we are pushing vertically on the lhs of a box
                var moves1 = move2(start + dir, move);
                var moves2 = move2(start + dir + new Complex(0, 1), move);
                if (moves1.success && moves2.success)
                    return (true, start + dir, [(start, start + dir, grid[start]), .. moves1.moves, .. moves2.moves]);

                return (false, start, []);
            }
        case ']':
            {
                //we are pushing vertically on the rhs of a box
                var moves1 = move2(start + dir - new Complex(0, 1), move);
                var moves2 = move2(start + dir, move);
                if (moves1.success && moves2.success)
                    return (true, start + dir, [(start, start + dir, grid[start]), .. moves1.moves, .. moves2.moves]);

                return (false, start, []);
            }
        default: throw new();
    }
}

//void showGrid(Complex robot)
//{
//    var R = (int)grid.Max(kvp => kvp.Key.Real);
//    var C = (int)grid.Max(kvp => kvp.Key.Imaginary);
//    var output = new char[R+1][];
//    for (int r = 0; r <= R; r++)
//        output[r] = new char[C+1];

//    foreach (var square in grid)
//    {
//        output[(int)square.Key.Real][(int)square.Key.Imaginary] = square.Value;
//    }
//    output[(int) robot.Real][(int) robot.Imaginary] = '@';

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
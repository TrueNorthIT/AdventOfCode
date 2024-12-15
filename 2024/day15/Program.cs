using System.Numerics;

//(^ for up, v for down, < for left, > for right)
var dirs = new Complex[] { new(-1, 0), new(1, 0), new(0, -1), new(0, 1) };

var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
var grid = files[0].Split("\r\n")
            .SelectMany((line, r) => line.Select((ch, c) => (r, c, ch)))
            .ToDictionary(tp => new Complex(tp.r, tp.c), tp => tp.ch);

var start = grid.Single(kvp => kvp.Value == '@').Key; 
grid[start] = '.';

var moves = files[1].ReplaceLineEndings("");
Console.WriteLine($"Initial grid:");
showGrid(start);

var curr = start;
foreach (var m in moves)
{
    curr = move(curr, m);
}

Console.WriteLine();
Console.WriteLine($"Final grid:");
showGrid(curr);
var p1 = grid.Where(kvp => kvp.Value == 'O').Sum(kvp => 100 * kvp.Key.Real + kvp.Key.Imaginary);
Console.WriteLine($"Part 1: {p1}");


// Returns the new robot position
// and pushes boxes in the global grid
Complex move(Complex start, char move)
{
    var dir = move switch
    {
        '^' => dirs[0],
        'v' => dirs[1],
        '<' => dirs[2],
        '>' => dirs[3],
    };
    var length = 1;
    Complex i = start;
    while (true)
    {
        switch (grid[i + length*dir])
        {
            case '.': i += dir; goto exit; //we have moved
            case '#': goto exit; //we have hit an obstruction
            case 'O': length++;  //we are pushing on a length of wall
                continue;
            default: throw new();
        }
    }
exit:;    
    //we now know from start to i is completely clear (.'s)
    for (var clear = start; clear != i; clear += dir)
        grid[clear] = '.';

    //and these are all O's
    for (var os = i + dir; os != i + length * dir; os += dir)
        grid[os] = 'O';

    //return the new start position
    return i;
}

void showGrid(Complex robot)
{
    var R = (int)grid.Max(kvp => kvp.Key.Real);
    var C = (int)grid.Max(kvp => kvp.Key.Imaginary);
    var output = new char[R+1][];
    for (int r = 0; r <= R; r++)
        output[r] = new char[C+1];

    foreach (var square in grid)
    {
        output[(int)square.Key.Real][(int)square.Key.Imaginary] = square.Value;
    }
    output[(int) robot.Real][(int) robot.Imaginary] = '@';

    var result = new System.Text.StringBuilder();
    foreach (var arr in output)
    {
        foreach (var ch in arr)
            result.Append(ch);
        result.AppendLine();
    }
    result.AppendLine();
    Console.WriteLine(result.ToString());
}
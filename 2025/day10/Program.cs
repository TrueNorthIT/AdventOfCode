using System.Diagnostics;

var input = File.ReadAllLines("input.txt").Select(line => line.Split(' ') switch {
    var arr => (    arr.First(), 
                    arr[1..^1].ToArray(),
                arr.Skip(arr.Length - 1).Single())
});

var lights = input.Select(tp => tp.Item1[1..^1]).ToArray();
var buttons = input.Select(tp => tp.Item2.Select(
        button => button[1..^1].Split(',')
            .Select(int.Parse).ToArray()).ToArray()).ToArray();
var joltages = input.Select(tp => tp.Item3[1..^1].Split(',').Select(int.Parse).ToArray()).ToArray();

var stopwatch = Stopwatch.StartNew();
var p1 = Enumerable.Range(0, lights.Length).Select(solveP1).Sum();
Console.WriteLine($"Part 1: {p1} in {stopwatch.ElapsedMilliseconds}ms");
stopwatch.Restart();
var p2 = Enumerable.Range(0, lights.Length).Select(reduceAndBackSubstitute).Sum();
Console.WriteLine($"Part 2: {p2} in {stopwatch.ElapsedMilliseconds}ms");

long reduceAndBackSubstitute(int index)
{
    (int R, int C) = (joltages[index].Length, buttons[index].Length);

    //create our matrix, Ax = b
    int[][] A = new int[R][];
    for (int r = 0; r < R; r++)
    {
        //make an extra col. for the b values
        A[r] = new int[C+1];
        A[r][C] = joltages[index][r];
    }
    foreach (var button in buttons[index].Index())
        foreach (var toggle in button.Item)
            A[toggle][button.Index] = 1;

    //we are going to reduce out matrix as much as possible
    for (int r = 0; r < R && r < C; r++)
    {
        //for row i, we need to reduce column i if required
        int pivot = -1;
        for (int p = r; p < R; p++)
            if (A[p][r] != 0)
                pivot = p;

        if (pivot == -1)
            //column is all zeroes already so we are done
            continue;

        //swap our pivot row (and values)
        swap(A, pivot, r);
        //and reduce all the rows below our pivot row
        for (int p = r + 1; p < R; p++)
        {
            if (A[p][r] == 0)
                continue;

            //make sure we keep our maths to integers!
            (var deltaNom, var deltaDen) = (A[p][r], A[r][r]);
            for(int c = 0; c < C; c++)
            {
                A[p][c] = deltaDen * A[p][c] - A[r][c] * deltaNom;
            }
            A[p][C] = A[p][C] * deltaDen - A[r][C] * deltaNom;
        }
        //we have fully reduced from r+1 to the end
    }   
    //now we have to start substituting in
    //and if we get stuck start brute forcing the parameters
    return backSub(index, R, C, A);
}

int backSub(int index, int R, int C, int[][] A)
{
    var maximums = buttons[index].Select(toggles => toggles.Min(bi => joltages[index][bi])).ToArray();

    int best = int.MaxValue;
    Stack<(int row, Dictionary<int, int> pressed)> stack = new ();

    stack.Push((R - 1, new Dictionary<int, int>()));
    while (stack.Any())
    {
        (var row, var pressed) = stack.Pop();

        if (row < 0)
        {
            //we've reached the end with no failures, this must be a solution
            best = Math.Min(pressed.Sum(kvp => kvp.Value), best);
            Console.WriteLine($"#{index} in {best} total: {String.Join(", ", pressed.Select(kvp => $"b{kvp.Key}={kvp.Value}").ToArray())}");
            continue;
        }

        //we have a row of the form x0 + x1 + x2 ... = br
        //we need to sub in any values we know and then start brute forcing the rest
        int rowTotal = A[row][C];
        for (int c = 0; c < C; c++)
            if (A[row][c] != 0)
                if (pressed.ContainsKey(c))
                    rowTotal-= A[row][c] * pressed[c];                    
                else
                    goto bruteForce;

        //1) rowTotal = 0, the row is consistent and all values are specified, move to next row
        //2) rowTotal != 0, this was a failed substitution so quit this path
        if (rowTotal == 0)
            stack.Push((row - 1, pressed));
        continue;
    bruteForce:;
        //we need to choose our next value
        //so push all the options to test
        var param = A[row].Index().Where(tp => tp.Index != C && tp.Item != 0 && !pressed.ContainsKey(tp.Index)).First();
        //upper bound of our choice is confusing because of -'ve numbers in the matrix
        //so just use an easily calculated pre-computed max
        var max = maximums[param.Index];
        for (int p = max; p >= 0; p--)
        {
            var newPressed = pressed.ToDictionary();
            newPressed[param.Index] = p;
            stack.Push((row, newPressed));
        }
    }
    Console.WriteLine($"#{index}: {best}");
    return best;
}

void swap<T>(T[] arr, int i0, int i1)
{
    var tmp = arr[i0];
    arr[i0] = arr[i1];
    arr[i1] = tmp;
}
void print(int[][] arr)
{
    foreach (var a in arr)
    {
        Console.WriteLine(String.Join("", a[0..^1].Select(d => $"{(Math.Sign(d) >= 0 ? "+" : "")}{d}     ").ToArray()) + $" = {a.Last()}");
    }
    Console.WriteLine();
}

long solveP1(int index)
{
    Dictionary<string, long> cache = new();
    Queue<(string state, long presses)> queue = new();
    var first = (empty(lights[index].Length), 0);
    queue.Enqueue(first);
    
    while (queue.Count > 0)
    {
        (var state, var presses) = queue.Dequeue();
        if (cache.ContainsKey(state))
        {
            continue;
        }
        cache[state] = presses;
        if (state == lights[index])
        {
            return presses;
        }
        foreach (var button in buttons[index])
        {
            var newLights = press(state, button);
            queue.Enqueue((newLights, presses + 1));            
        }
    }
    throw new();
}

string empty(int length) => new string(Enumerable.Repeat('.', length).ToArray());
string press(string before, int[] button)
{
    var res = new System.Text.StringBuilder(before);
    foreach(var toggle in button)
    {
        res[toggle] = res[toggle] == '#' ? '.' : '#';
    }
    return res.ToString();
}
record State(string lights, long presses);

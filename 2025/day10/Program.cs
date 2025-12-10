using System.Text;

var input = File.ReadAllLines("example.txt").Select(line => line.Split(' ') switch
{
    var arr =>
        (arr.First(), arr.Skip(1).Take(arr.Length - 2).ToArray(), arr.Skip(arr.Length - 1).Single())
});

var lights = input.Select(tp => tp.Item1[1..^1]).ToArray();

var buttons = input.Select(tp => tp.Item2.Select(
        button => button[1..^1].Split(',')
            .Select(int.Parse).ToArray()).ToArray()).ToArray();

var joltages = input.Select(tp => tp.Item3[1..^1].Split(',').Select(int.Parse).ToArray()).ToArray();

var fewest = Enumerable.Range(0, lights.Length).Select(solve).ToArray();
var p1 = fewest.Sum();
Console.WriteLine(p1);

//solvep2(131);
fewest = Enumerable.Range(0, lights.Length).Select(solvep2).ToArray();
var p2 = fewest.Sum();
Console.WriteLine(p2);

long solvep2(int index)
{
    int R = joltages[index].Length;
    int C = buttons[index].Length;
    double[][] arr = new double[R][];
    for (int r = 0; r < joltages[index].Length; r++)
    {
        arr[r] = new double[C];
    }
    foreach (var button in buttons[index].Index())
    {
        foreach (var toggle in button.Item)
        {
            arr[toggle][button.Index] = 1;
        }
    }

    //print(arr);
    var b = joltages[index].Select(i => (double) i).ToArray();
    //we are going to reduce out matrix as much as possible
    for (int r = 0; r < R && r < C; r++)
    {
        //first row, we need to reduce the first column if possible
        int pivot = -1;
        for (int p = r; p < R; p++)
        {
            if (arr[p][r] != 0)
            {
                pivot = p;
                break;
            }
        }
        if (pivot == -1)
        {
            //everything is 0 here so just continue to the next row
            continue;
        }
        else if (pivot == r)
        {
            //nothing to do
        }
        else
        {
            //swap our pivot row into place
            var tmpA = arr[pivot];
            arr[pivot] = arr[r];
            arr[r] = tmpA;
            //and swap our values
            var tmpV = b[pivot];
            b[pivot] = b[r];
            b[r] = tmpV;
        }

        //if we got here we can reduce all the remaining rows
        for (int p = r+1; p < R; p++)
        {
            if (arr[p][r] != 0)
            {
                var delta = arr[p][r] / arr[r][r];
                for(int c = 0; c < C; c++)
                {
                    arr[p][c] -= delta * arr[r][c];
                }
                b[p] -= delta * b[r];
            }
        }
        //we have fully reduced from r+1 to the end
    }

    //print(arr);
    //Console.WriteLine($"b: {String.Join(", ", b)}");

    //now we have to start substituting in
    //and if we get stuck start brute forcing the parameters

    return backSub(index, arr, b);
}

int backSub(int index, double[][] arr, double[] b)
{
    int best = int.MaxValue;
    HashSet<string> cache = new HashSet<string>();
    Stack<(int row, Dictionary<int, int> pressed)> queue = new ();

    int bestRow = int.MaxValue;
    //start on last non 0 row
    //var si = arr.Index().Last(arr => arr.Item.Any(d => d != 0)).Index;
    queue.Push((arr.Length - 1, new Dictionary<int, int>()));
    while (queue.Any())
    {
        (var row, var pressed) = queue.Pop();
        if (row < 0) continue;

        var cacheKey = $"R:{row}-" + String.Join(",", Enumerable.Range(0, buttons[index].Length).Select(i => pressed.ContainsKey(i) ? pressed[i] : -1).ToArray());

        if (row == bestRow)
            Console.WriteLine(cacheKey);

        if (row < bestRow)
        {
            bestRow = row;
            Console.WriteLine($"Reached row {row}");
            Console.WriteLine(cacheKey);
        }
        if (cache.Contains(cacheKey))
            continue;

        cache.Add(cacheKey);
        
        //we have a row of the form x0 + x1 + x2 ... = br
        //we need to sub in any values we know and then start brute forcing the rest
        bool allKnown = true;
        double checkSum = b[row];
        for (int c = 0; c < arr[0].Length; c++)
        {
            if (arr[row][c] != 0)
            {
                if (pressed.ContainsKey(c))
                {
                    checkSum-= arr[row][c] * pressed[c];                    
                }
                else
                {
                    allKnown = false;
                }
            }
        }
        //if the whole row is 0, we have two options
        //1) b[row] = 0, this row has passed, moved onto the next
        //2) b[row] != 0, this was a failed substitution so stop

        if (allKnown)
        {
            if (checkSum == 0)
            {
                if (pressed.Count == buttons[index].Length)
                {
                    //we are done
                    var ans = pressed.Sum(kvp => kvp.Value);
                    best = Math.Min(ans, best);
                    Console.WriteLine($"#{index} in {best} presses: {String.Join(", ", pressed.Select(kvp => $"key:{kvp.Key}={kvp.Value}").ToArray())}");
                }
                queue.Push((row - 1, pressed));
            }
            continue;
        }

        //we have at least one value left over
        //so queue up all the options for it
        var param = arr[row].Index().Where(tp => tp.Item != 0 && !pressed.ContainsKey(tp.Index)).First();
        {
            //max that this parameter can be
            var max = Math.Ceiling(checkSum / arr[row][param.Index]);
            //var max = Math.Abs(checkSum);
            for (int p = (int) max; p >= 0; p--)
            {
                var newPressed = pressed.ToDictionary();
                newPressed[param.Index] = p;                
                queue.Push((row, newPressed));
            }
        }
    }

    return best;
}

void print(double[][] arr)
{
    foreach (var a in arr)
    {
        Console.WriteLine(String.Join("", a.Select(d => $"{(Math.Sign(d) >= 0 ? "+" : "")}{d}     ").ToArray()));
    }
    Console.WriteLine();
}

long solve(int index)
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
        long best = long.MaxValue;
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
    var res = new StringBuilder(before);
    foreach(var toggle in button)
    {
        res[toggle] = res[toggle] == '#' ? '.' : '#';
    }
    return res.ToString();
}


record State(string lights, long presses);

using System.Collections.Concurrent;
using System.Diagnostics;

ThreadPool.SetMinThreads(Environment.ProcessorCount, 1000);
Process.GetCurrentProcess().PriorityClass = ProcessPriorityClass.High;

string[] lines = File.ReadAllLines("input.txt");
//string[] lines = File.ReadAllLines("demo.txt");
int rows = lines.Length;
int cols = lines[0].Length;

char[,] grid = new char[rows, cols];

ConcurrentDictionary<(int, int), long> asSeenOnTV = [];

for (int r = 0; r < rows; r++)
{
    for (int c = 0; c < cols; c++)
    {
        grid[r, c] = lines[r][c];
    }
}

int startPos = 0;

for (int j = 0; j < grid.GetLength(1); j++)
{
    if (grid[0, j] == 'S')
    {
        startPos = j;
    }
}

ParallelOptions options = new ParallelOptions
{
    MaxDegreeOfParallelism = Environment.ProcessorCount,
};

long timelineTotal = SimulateTimeline(0, startPos);

Console.WriteLine($"Timeline count: {timelineTotal}");
return;

long SimulateTimeline(int newI, int j)
{
    
    //Console.WriteLine($"Simulating timeline at position ({newI}, {j})");
    if (asSeenOnTV.ContainsKey((newI, j)))
    {
        return asSeenOnTV[(newI, j)];
    }

    for (int i = newI; i < grid.GetLength(0); i++)
    {
        if (grid[i, j] == '^')
        {
            long leftResult = 0;
            long rightResult = 0;
            
            Parallel.Invoke( options,
                () => rightResult = SimulateTimeline(i + 1, j + 1),
                () => leftResult = SimulateTimeline(i + 1, j - 1)
            );
            
            long totalResult = leftResult + rightResult;
            asSeenOnTV[(newI, j)] = totalResult;
            return totalResult;
        }
    }
    
    asSeenOnTV[(newI, j)] = 1;
    return 1;
}
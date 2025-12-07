string[] lines = File.ReadAllLines("input.txt");
//string[] lines = File.ReadAllLines("demo.txt");
int rows = lines.Length;
int cols = lines[0].Length;

char[,] grid = new char[rows, cols];

for (int r = 0; r < rows; r++)
{
    for (int c = 0; c < cols; c++)
    {
        grid[r, c] = lines[r][c];
    }
}

long splitCounter = 0;

HashSet<int> beamPositions = [];
HashSet<int> newBeamPositions = [];
HashSet<int> removeBeamPositions = [];

for (int i = 0; i < grid.GetLength(0); i++)
{
    for (int j = 0; j < grid.GetLength(1); j++)
    {
        if (grid[i, j] == 'S')
        {
            beamPositions.Add(j);
        }
        else if (grid[i, j] == '^')
        {
            if (beamPositions.Contains(j))  splitCounter++;
            removeBeamPositions.Add(j);
            newBeamPositions.Add(j + 1);
            newBeamPositions.Add(j - 1);
        }
    }
    beamPositions.UnionWith(newBeamPositions);
    beamPositions.ExceptWith(removeBeamPositions);
    removeBeamPositions.Clear();
    newBeamPositions.Clear();
}

Console.WriteLine($"Split count: {splitCounter}");
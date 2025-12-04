var grid = File.ReadAllLines("input.txt").Index().SelectMany(tpr => tpr.Item.Index().Select(tpc => ((tpr.Index, tpc.Index), tpc.Item)))
    .ToDictionary(tp => tp.Item1, tp => tp.Item2);

var offsets = new (int r, int c)[] { (-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) };

bool accessible((int r, int c) tp) => offsets.Where(os => grid.ContainsKey((tp.r + os.r, tp.c + os.c)) && grid[(tp.r + os.r, tp.c + os.c)] == '@').Count() < 4;

var p1 = grid.Keys.Where(key => grid[key] == '@').Count(accessible);
Console.WriteLine(p1);

int removed = 0;
int p2 = 0;
do
{
    var toRemove = grid.Keys.Where(key => grid[key] == '@').Where(accessible).ToArray();
    removed = toRemove.Count();
    p2 += removed;
    foreach (var item in toRemove)
    {
        grid[item] = '.';
    }
}
while (removed > 0);

Console.WriteLine(p2);

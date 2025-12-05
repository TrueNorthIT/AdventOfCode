using System.Numerics;

var grid = File.ReadAllLines("input.txt").Index().SelectMany(tpr => tpr.Item.Index().Select(tpc => (new Complex(tpr.Index, tpc.Index), tpc.Item)))
    .ToDictionary(tp => tp.Item1, tp => tp.Item2);

var offsets = 
    from r in Enumerable.Range(-1, 3)
    from c in Enumerable.Range(-1, 3)
    where !(r == 0 && c == 0)
    select new Complex(r, c);

bool accessible(Complex p) => offsets.Where(os => grid.TryGetValue(p + os, out char c) && c == '@').Count() < 4;

var removed = new List<List<Complex>>();
do
{
    removed.Add([]);
    foreach (var c in grid.Keys.Where(key => grid[key] == '@').Where(accessible).ToArray())
    {
        removed.Last().Add(c);
        grid[c] = '.';
    }
}
while (removed.Last().Count > 0);
Console.WriteLine((removed.First().Count, removed.Sum(l => l.Count)));

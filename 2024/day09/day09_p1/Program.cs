var tmp = File.ReadAllText("input.txt");
if (tmp.Length % 2 == 1) tmp = $"{tmp}0";

List<int> disk = new List<int>();
int fileId = 0;
foreach (var grp in tmp.Select((ch, i) => (ch, i)).GroupBy(tp => tp.i / 2))
{
    var size = int.Parse($"{grp.First().ch}");
    var free = int.Parse($"{grp.Skip(1).First().ch}");
    for (var s = 0; s < size; s++) disk.Add(fileId);
    for (var f = 0; f < free; f++) disk.Add(-1);
    fileId++;
}

int last = disk.Count - 1;
int first = 0;
while (first < last)
{
    while (disk[first] != -1) first++;
    if (disk[last] != -1)
    {
        disk[first] = disk[last];
        disk[last] = -1;
    }
    last--;
}
exit:;

var part1 = disk.Where(i => i != -1).Select((id, index) => (id, index)).Sum(tp => (long) tp.id * tp.index);
Console.WriteLine($"Part 1: {part1}");
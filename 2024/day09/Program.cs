var blocks = new LinkedList<(int id, int size, int free)>(
            File.ReadAllText("input.txt").Concat(['0'])
                .Index().GroupBy(tp => tp.Index / 2)
                .Select(grp => (grp.Key, grp.First().Item - '0', grp.Skip(1).First().Item - '0')));

var part1 = () => {
    var disk = blocks.SelectMany(block => Enumerable.Repeat(block.id, block.size)
        .Concat(Enumerable.Repeat(-1, block.free))).ToList();

    (int first, int last) = (0, disk.Count - 1);
    while (first < last)
    {
        while (disk[first] != -1)
            first++;
        if (disk[last] != -1)
            (disk[first], disk[last]) = (disk[last], -1);
        last--;
    }
    return disk.Where(i => i != -1).Index().Sum(tp => (long)tp.Item * tp.Index);
};
Console.WriteLine($"Part 1: {part1()}");

var part2 = () => {
    foreach (var move in AsNodeEnumerable(blocks).Reverse().ToArray())
    {
        var target = blocks.First;
        while (target != move && target.Value.free < move.Value.size)
            target = target.Next;

        if (target == move)
            continue;

        move.Previous.ValueRef.free = move.Previous.Value.free + move.Value.size + move.Value.free;
        move.ValueRef.free = target.Value.free - move.Value.size;
        blocks.Remove(move);
        target.ValueRef.free = 0;
        target.List.AddAfter(target, move);
    }

    return blocks.Aggregate((0L, 0L),
        ((long total, long i) acc, (int id, int size, int free) block) =>
            (acc.total + block.id * (acc.i * block.size + (block.size * (block.size - 1) / 2))
            , acc.i + block.size + block.free),
        tp => tp.Item1);
};
Console.WriteLine($"Part 2: {part2()}");

IEnumerable<LinkedListNode<T>> AsNodeEnumerable<T>(LinkedList<T> list)
{
    for (var node = list.First; node != null; node = node.Next)
        yield return node;
}
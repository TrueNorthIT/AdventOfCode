var blocks = new LinkedList<(int id, int size, int free)>(
        File.ReadAllText("test.txt").Concat(['0'])
            .Index().GroupBy(tp => tp.Index / 2)
            .Select(grp => (grp.Key, 
                grp.First().Item - '0', grp.Skip(1).First().Item - '0')));

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

var part2 = blocks.Aggregate((0L, 0),
        (acc, block) =>
            (acc.Item1 + block.id * (acc.Item2 * block.size + ((long)block.size * (block.size - 1) / 2))
            , acc.Item2 + block.size + block.free),
        tp => tp.Item1);

Console.WriteLine($"Part 2: {part2}");

IEnumerable<LinkedListNode<T>> AsNodeEnumerable<T>(LinkedList<T> list)
{
    for (var node = list.First; node != null; node = node.Next)
        yield return node;
}
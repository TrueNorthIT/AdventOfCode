var blocks = new LinkedList<(int id, int size, int free)>(
        File.ReadAllText("test.txt").Concat(['0'])
            .Index().GroupBy(tp => tp.Index / 2)
            .Select(grp => (grp.Key, 
                grp.First().Item - '0', grp.Skip(1).First().Item - '0')));

var answers = new[] { true, false }.Select(p1 =>
        solve(blocks, p1).Aggregate((0L, 0),
        (acc, block) =>
            (acc.Item1 + block.id * (acc.Item2 * block.size + ((long)block.size * (block.size - 1) / 2))
            , acc.Item2 + block.size + block.free),
        tp => tp.Item1)).ToArray();

Console.WriteLine($"Part 1: {answers[0]}");
Console.WriteLine($"Part 2: {answers[1]}");

LinkedList<(int id, int size, int free)> solve(LinkedList<(int id, int size, int free)> blocks, bool part1)
{
    blocks = new LinkedList<(int id, int size, int free)>(blocks);
    foreach (var move in AsNodeEnumerable(blocks).Reverse().ToArray())
    {
        var target = blocks.First;
        if (part1)
        {
            while (target != move)
            {
                if (target.Value.free > 0)
                {
                    var toMove = Math.Min(target.Value.free, move.Value.size);
                    move.ValueRef.size -= toMove;
                    move.ValueRef.free += toMove;

                    blocks.AddAfter(target, (move.Value.id, toMove, target.Value.free - toMove));
                    target.ValueRef.free = 0;
                }
                if (move.Value.size == 0)
                {
                    move.Previous.ValueRef.free += move.Value.free;
                    blocks.Remove(move);
                    break;
                }
                target = target.Next;
            }
        }
        else
        {
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
    }
    return blocks;
}

IEnumerable<LinkedListNode<T>> AsNodeEnumerable<T>(LinkedList<T> list)
{
    for (var node = list.First; node != null; node = node.Next)
        yield return node;
}
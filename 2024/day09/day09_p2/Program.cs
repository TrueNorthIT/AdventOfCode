var tmp = File.ReadAllText("input.txt");
if (tmp.Length % 2 == 1) tmp = $"{tmp}0";

var blocks = new LinkedList<Block>();
int id = 0;
foreach (var grp in tmp.Select((ch, i) => (ch, i)).GroupBy(tp => tp.i / 2))
{
    var size = int.Parse($"{grp.First().ch}");
    var free = int.Parse($"{grp.Skip(1).First().ch}");

    var block = new Block() { id = id, size = size, free = free};
    blocks.AddLast(block);    
    id++;
}

//no way to enumerate the nodes so this is a bit clunky
//but we need to copy them as blockToMove.Previous becomes invalid in the loop
var reversed = new List<LinkedListNode<Block>>();
for (var blockToMove = blocks.Last; blockToMove != null; blockToMove = blockToMove.Previous)
{
    reversed.Add(blockToMove);
}

foreach (var movingBlock in reversed)
{
    //step through from first block trying to find enough free space to fit this block
    var targetBlock = blocks.First;
    while (targetBlock != movingBlock && targetBlock.Value.free < movingBlock.Value.size)
        targetBlock = targetBlock.Next;

    if (targetBlock != movingBlock)
    {
        //we can move a block so add its space to the previous block
        //(there must be one we never move the first block)
        movingBlock.Previous.ValueRef.free = movingBlock.Previous.Value.free + movingBlock.Value.size + movingBlock.Value.free;
        
        //our new block has any extra free space from the block we have moved it into
        movingBlock.ValueRef.free = targetBlock.Value.free - movingBlock.Value.size;

        //target block we are merging into now has 0 free space, it has been given to the new block
        targetBlock.ValueRef.free = 0;

        //remove the deleted node, and add the new one after the block we merged into
        blocks.Remove(movingBlock);
        targetBlock.List.AddAfter(targetBlock, movingBlock);
    }
}

int index = 0;
long part2 = 0;
for (var iterator = blocks.First; iterator != null; iterator = iterator.Next)
{
    part2 += iterator.Value.id * (index * iterator.Value.size + ((long) iterator.Value.size * (iterator.Value.size - 1) / 2));
    index += iterator.Value.size + iterator.Value.free;
}

Console.WriteLine($"Part 2: {part2}");

struct Block()
{
    public int id;
    public int size;
    public int free;

    public override string ToString() => $"id:{id},size:{size},free:{free}";
}

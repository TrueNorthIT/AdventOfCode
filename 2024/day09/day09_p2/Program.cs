var tmp = File.ReadAllText("input.txt");
if (tmp.Length % 2 == 1) tmp = $"{tmp}0";

Block firstBlock = null;
Block lastBlock = null;
{
    Block forwardIterator = null;
    int fileId = 0;
    foreach (var grp in tmp.Select((ch, i) => (ch, i)).GroupBy(tp => tp.i / 2))
    {
        var size = int.Parse($"{grp.First().ch}");
        var free = int.Parse($"{grp.Skip(1).First().ch}");

        var block = new Block() { id = fileId, size = size, free = free, prev = forwardIterator };
        if (firstBlock == null)
        {
            firstBlock = block;
            forwardIterator = firstBlock;
        }
        else
        {
            forwardIterator.next = block;
            forwardIterator = block;
        }

        fileId++;
    }
    lastBlock = forwardIterator;
}


for (var blockToMove = lastBlock; blockToMove != null; blockToMove = blockToMove.prev)
{
    //step through from first block trying to find enough free space to fit this block
    var blockToMergeInto = firstBlock;
    while (blockToMergeInto != blockToMove && blockToMergeInto.free < blockToMove.size)
    {
        blockToMergeInto = blockToMergeInto.next;
    }
    if (blockToMergeInto != blockToMove)
    {
        //we can move a block
        //remove it completely and add its space to the previous block
        //(there must be one we never move the first block)
        blockToMove.prev.free = blockToMove.prev.free + blockToMove.size + blockToMove.free;
        blockToMove.prev.next = blockToMove.next;

        //if the removed block pointed to something, repoint it
        if (blockToMove.next != null)
        {
            blockToMove.next.prev = blockToMove.prev;
        }

        //out new block has any extra free space from the block we have moved it into
        var movedBlock = new Block() { 
            id = blockToMove.id, 
            size = blockToMove.size, 
            free = blockToMergeInto.free - blockToMove.size, 
            next = blockToMergeInto.next, 
            prev = blockToMergeInto };

        //target block we are merging into now has 0 free space, it has been given to the new block
        blockToMergeInto.free = 0;

        //target block must have pointed to something, as we never move to the last block
        // so repoint it to this block
        blockToMergeInto.next.prev = movedBlock;

        //target block now points to the new block
        blockToMergeInto.next = movedBlock;
    }
}

int index = 0;
long part2 = 0;
for (var iterator = firstBlock; iterator !=null; iterator = iterator.next)
{
    for (int i = 0; i < iterator.size; i++)
    {
        part2 += index * iterator.id;
        index++;
    }
    index += iterator.free;
}

Console.WriteLine($"Part 2: {part2}");
class Block ()
{
    public int id;
    public int size;
    public int free;
    public Block prev;
    public Block next;

    public override string ToString()
    {
        return $"id:{id}, size:{size}, free:{free}";
    }
}

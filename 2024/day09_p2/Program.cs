
var tmp = File.ReadAllText("input.txt");
if (tmp.Length % 2 == 1) tmp = $"{tmp}0";

Block firstBlock = null;
Block firstIterator = null;
int fileId = 0;
foreach (var grp in tmp.Select((ch, i) => (ch, i)).GroupBy(tp => tp.i / 2))
{
    var size = int.Parse($"{grp.First().ch}");
    var free = int.Parse($"{grp.Skip(1).First().ch}");

    var block = new Block() { id = fileId, size = size, free = free, prev = firstIterator };
    if (firstBlock == null)
    {
        firstBlock = block;
        firstIterator = firstBlock;
    }
    else
    {
        firstIterator.next = block;
        firstIterator = block;
    }

    fileId++;
}

var lastBlock = firstIterator;
var lastIterator = lastBlock;
while (lastIterator.prev != null)
{
    //step through from first block trying to find enough free space to fit this block
    firstIterator = firstBlock;
    while (firstIterator != null && firstIterator != lastIterator && firstIterator.free < lastIterator.size)
    {
        firstIterator = firstIterator.next;
    }
    if (firstIterator != null && firstIterator != lastIterator)
    {
        //remove the last block completely
        if (lastIterator.prev != null)
        {
            lastIterator.prev.free = lastIterator.prev.free + lastIterator.size + lastIterator.free;
            lastIterator.prev.next = lastIterator.next;
        }
        if (lastIterator.next != null)
        {
            lastIterator.next.prev = lastIterator.prev;
        }
        var movedBlock = new Block() { 
            id = lastIterator.id, 
            size = lastIterator.size, 
            free = firstIterator.free - lastIterator.size, 
            next = firstIterator.next, 
            prev = firstIterator };

        firstIterator.free = 0;
        if (firstIterator.next != null)
        {
            firstIterator.next.prev = movedBlock;
        }
        firstIterator.next = movedBlock;
    }
    lastIterator = lastIterator.prev;
}

firstIterator = firstBlock;
int index = 0;
long part2 = 0;
while (firstIterator != null)
{
    for (int i = 0; i < firstIterator.size; i++)
    {
        part2 += index * firstIterator.id;
        index++;
    }
    index += firstIterator.free;
    firstIterator = firstIterator.next;
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

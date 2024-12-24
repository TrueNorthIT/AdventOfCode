var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
(string x, string y, string z, string operation)[] originalGates = files[1].Split("\r\n").Select(line => line.Split(" -> ")).Select(arr =>
{
    var sp2 = arr[0].Split(" ");
    return ((sp2[0], sp2[2], arr[1], sp2[1]));

}).ToArray();

{   //Part 1
    var part1Outputs = files[0].Split("\r\n").Select(line => line.Split(": ")).Select(arr => (arr[0], arr[1] == "1")).ToDictionary();
    var p1Gates = originalGates.GroupBy(tp => tp.x).Concat(originalGates.GroupBy(tp => tp.y)).GroupBy(grp => grp.Key).ToDictionary(grp => grp.Key, grp => grp.SelectMany(grp => grp).ToArray());
    var bits = String.Join("", solve(part1Outputs.ToDictionary(), p1Gates).Select(b => b ? "1" : "0").ToArray());
    var dec = Convert.ToUInt64(bits, 2);
    Console.WriteLine($"Part 1: {(bits, dec)}");
}

//Part 2
//swap 1
var p2Swaps = new (int, int)[] { (75, 144), (9, 86), (37, 49), (0, 107) };
foreach (var swap in p2Swaps)
{
    Console.WriteLine($"Swapping : {swap.Item1},{swap.Item2}");
    var g1z = originalGates[swap.Item1].z;
    var g2z = originalGates[swap.Item2].z;
    originalGates[swap.Item1].z = g2z;
    originalGates[swap.Item2].z = g1z;
}

var p2 = String.Join(",", p2Swaps.SelectMany(tp => new[] { originalGates[tp.Item1].z, originalGates[tp.Item2].z }).OrderBy(str => str).ToArray());
//fvw,grf,mdb,nwq,wpq,z18,z22,z36

int inputSize = 45;
var rand = new Random();
int bitFailedAt = 5;
for (int g1 = 0; g1 < originalGates.Length; g1++)
    for (int g2 = 0; g2 < originalGates.Length; g2++)
    {
        if (g2 < g1)
            continue;

        //either no swap, or swap a gate
        //clone our array with any swaps we had already made
        var gates = originalGates.ToArray();
        var g1Val = gates[g1];
        var g2Val = gates[g2];
        gates[g1] = (g1Val.x, g1Val.y, g2Val.z, g1Val.operation);
        gates[g2] = (g2Val.x, g2Val.y, g1Val.z, g2Val.operation); ;

        var _gates = gates.GroupBy(tp => tp.x).Concat(gates.GroupBy(tp => tp.y)).GroupBy(grp => grp.Key).ToDictionary(grp => grp.Key, grp => grp.SelectMany(grp => grp).ToArray());

        for (int bit = 0; bit < inputSize; bit++)
        {
            long x = (1L << bit) - 1L;
            long y = 1;
            var xStr = Convert.ToString(x, 2).PadLeft(inputSize, '0');
            var yStr = Convert.ToString(y, 2).PadLeft(inputSize, '0');
            var outputs = getOutputs(x, y);

            //output bits should always be one more than input bits
            var compBits = solve(outputs, _gates);
            var compSum = getDecimal(compBits);
            var actualSum = x + y;
            var actualBits = getOutputBits(actualSum);

            if (compSum != actualSum)
            {
                if (bit > bitFailedAt)
                {
                    var failedAtStr = Convert.ToString(x, 2).PadLeft(inputSize + 1, '0');
                    Console.WriteLine($"swapping gates {g1},{g2} Failed at {x} / {failedAtStr}");
                    bitFailedAt = bit;
                }
                goto failed;
            }
        }
        Console.WriteLine($"*** Swapping gates {g1},{g2} No failure!");
        break;
    failed:;
    }

Console.WriteLine();

Dictionary<string, bool> getOutputs(long x, long y)
{
    var outputs = new Dictionary<string, bool>();
    foreach (var ch in new[] { 'x', 'y' })
    {
        long input;
        if (ch == 'x') input = x; else input = y;

        var binaryStr = Convert.ToString(input, 2).PadLeft(inputSize, '0');
        for (int digit = binaryStr.Length - 1; digit >= 0; digit--)
        {
            var indexStr = (binaryStr.Length - 1 - digit).ToString("D2");
            if (binaryStr[digit] == '1')
            {
                outputs.Add($"{ch}{indexStr}", true);
            }
            else
            {
                outputs.Add($"{ch}{indexStr}", false);
            }
        }
    }

    return outputs;
}
bool[] getOutputBits(long a) => Convert.ToString(a, 2).PadLeft(inputSize + 1, '0').Select(ch => ch == '1').ToArray();
long getDecimal(bool[] bits) => (long) Convert.ToUInt64(String.Join("", bits.Select(b => b ? "1" : "0").ToArray()), 2);

bool[] solve(Dictionary<string, bool> outputs, Dictionary<string, (string x, string y, string z, string operation)[]> gates)
{
    var queue = new Queue<string>(outputs.Keys);
    while (queue.TryDequeue(out var next))
    {
        if (!gates.ContainsKey(next))
            //must be an output gate
            continue;
        foreach (var g in gates[next])
        {
            if (outputs.ContainsKey(g.x) && outputs.ContainsKey(g.y) && !outputs.ContainsKey(g.z))
            {
                switch (g.operation)
                {
                    case "AND":
                        outputs[g.z] = outputs[g.x] && outputs[g.y];
                        break;
                    case "OR":
                        outputs[g.z] = outputs[g.x] || outputs[g.y];
                        break;
                    case "XOR":
                        outputs[g.z] = outputs[g.x] ^ outputs[g.y];
                        break;
                }
                queue.Enqueue(g.z);
            }
        }
    }

    return outputs.Where(tp => tp.Key.StartsWith("z")).OrderByDescending(tp => tp.Key).Select(kvp => kvp.Value).ToArray();
}
var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
(string x, string y, string z, string operation)[] originalGates = files[1].Split("\r\n").Select(line => line.Split(" -> ")).Select(arr =>
{
    var sp2 = arr[0].Split(" ");
    return (sp2[0], sp2[2], arr[1], sp2[1]);

}).ToArray();

{   //Part 1
    var part1Outputs = files[0].Split("\r\n").Select(line => line.Split(": ")).Select(arr => (arr[0], arr[1] == "1")).ToDictionary();
    var p1Gates = originalGates.GroupBy(tp => tp.x).Concat(originalGates.GroupBy(tp => tp.y)).GroupBy(grp => grp.Key).ToDictionary(grp => grp.Key, grp => grp.SelectMany(grp => grp).ToArray());
    var bits = String.Join("", solve(part1Outputs.ToDictionary(), p1Gates).Select(b => b ? "1" : "0").ToArray());
    var dec = Convert.ToUInt64(bits, 2);
    Console.WriteLine($"Part 1: {(bits, dec)}");
}

int inputSize = 45;

//Part 2
var p2Swaps = new List<(int g1, int g2)>();
while (p2Swaps.Count < 4)
{
    int bitFailedAt = 5;
    (int g1, int g2) best = (-1, -1);
    for (int g1 = 0; g1 < originalGates.Length; g1++)
        for (int g2 = 0; g2 < originalGates.Length; g2++)
        {
            if (g1 < g2) continue;
            var gates = originalGates;
            swap(gates, g1, g2);

            //need to fix this so we don't need a copy would be must faster
            var _gates = gates.GroupBy(tp => tp.x).Concat(gates.GroupBy(tp => tp.y)).GroupBy(grp => grp.Key).ToDictionary(grp => grp.Key, grp => grp.SelectMany(grp => grp).ToArray());

            for (int bit = 0; bit < inputSize; bit++)
            {
                long x = (1L << bit) - 1L;
                long y = 1;
                var inputs = getInputs(x, y);

                //output bits should always be one more than input bits
                var compBits = solve(inputs, _gates);
                var compSum = getDecimal(compBits);
                var actualSum = x + y;
                var actualBits = getOutputBits(actualSum);

                if (compSum != actualSum)
                {
                    if (bit > bitFailedAt)
                    {
                        var failedAtStr = Convert.ToString(x, 2).PadLeft(inputSize + 1, '0');
                        Console.WriteLine($"New best candidate ({g1},{g2}). First {bit-1} bits are fixed - failed at {failedAtStr}");
                        best = (g1, g2);
                        bitFailedAt = bit;
                    }
                    goto failed;
                }
            }
            best = (g1, g2);
            goto done;
        failed:;

            swap(gates, g2, g1);
        }

    done:;
    Console.WriteLine($"Choosing best swap {best}");
    p2Swaps.Add((best.g1, best.g2));
    swap(originalGates, best.g1, best.g2);
}

var p2 = String.Join(",", p2Swaps.SelectMany(tp => new[] { originalGates[tp.Item1].z, originalGates[tp.Item2].z }).OrderBy(str => str).ToArray());
Console.WriteLine($"Part 2: {p2}");

void swap((string x, string y, string z, string operation)[] gates, int g1, int g2)
{
    (var g1z, var g2z) = (gates[g1].z, gates[g2].z);
    (gates[g1].z, gates[g2].z) = (g2z, g1z);
}

Dictionary<string, bool> getInputs(long x, long y)
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
string print(long a) => Convert.ToString(a, 2).PadLeft(inputSize, '0');

bool[] solve(Dictionary<string, bool> inputs, Dictionary<string, (string x, string y, string z, string operation)[]> gates)
{
    var queue = new Queue<string>(inputs.Keys);
    while (queue.TryDequeue(out var next))
    {
        if (!gates.ContainsKey(next))
            //must be an output gate
            continue;
        foreach (var g in gates[next])
        {
            if (inputs.ContainsKey(g.x) && inputs.ContainsKey(g.y) && !inputs.ContainsKey(g.z))
            {
                switch (g.operation)
                {
                    case "AND":
                        inputs[g.z] = inputs[g.x] && inputs[g.y];
                        break;
                    case "OR":
                        inputs[g.z] = inputs[g.x] || inputs[g.y];
                        break;
                    case "XOR":
                        inputs[g.z] = inputs[g.x] ^ inputs[g.y];
                        break;
                }
                queue.Enqueue(g.z);
            }
        }
    }

    return inputs.Where(tp => tp.Key.StartsWith("z")).OrderByDescending(tp => tp.Key).Select(kvp => kvp.Value).ToArray();
}
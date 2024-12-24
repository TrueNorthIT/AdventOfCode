var files = File.ReadAllText("input.txt").Split("\r\n\r\n");
(string x, string y, string z, string operation)[] gates = files[1].Split("\r\n").Select(line => line.Split(" -> ")).Select(arr =>
{
    var sp2 = arr[0].Split(" ");
    return ((sp2[0], sp2[2], arr[1], sp2[1]));

}).ToArray();

{   //Part 1
    var part1Outputs = files[0].Split("\r\n").Select(line => line.Split(": ")).Select(arr => (arr[0], arr[1] == "1")).ToDictionary();
    var p1Gates = gates.GroupBy(tp => tp.x).Concat(gates.GroupBy(tp => tp.y)).GroupBy(grp => grp.Key).ToDictionary(grp => grp.Key, grp => grp.SelectMany(grp => grp).ToArray());
    var bits = String.Join("", solve(part1Outputs.ToDictionary(), p1Gates).Select(b => b ? "1" : "0").ToArray());
    var dec = Convert.ToUInt64(bits, 2);
    Console.WriteLine($"Part 1: {(bits, dec)}");
}

//Part 2
//swap 1
foreach (var swap in new (int,int)[] { })
{
    Console.WriteLine($"Swapping : {swap.Item1},{swap.Item2}");
    var g1z = gates[swap.Item1].z;
    var g2z = gates[swap.Item2].z;
    gates[swap.Item1].z = g2z;
    gates[swap.Item2].z = g1z;
}
int bitFailedAt = 0;
Console.WriteLine($"Last failed at {bitFailedAt}");

int inputSize = 45;
var rand = new Random();
Dictionary<(int g1, int g2), double> averages = new Dictionary<(int g1, int g2), double>();
for (int g1 = 0; g1 < gates.Length; g1++)
    for (int g2 = 0; g2 < gates.Length; g2++)
    {
        //swap a gate, we have to swap the outputs! not the gates :(
        var g1z = gates[g1].z;
        var g2z = gates[g2].z;
        gates[g1].z = g2z;
        gates[g2].z = g1z;

        var _gates = gates.GroupBy(tp => tp.x).Concat(gates.GroupBy(tp => tp.y)).GroupBy(grp => grp.Key).ToDictionary(grp => grp.Key, grp => grp.SelectMany(grp => grp).ToArray());

        for (int bit = bitFailedAt; bit < inputSize; bit++)
        {
            long x = (1L << bit) - 1L;
            long y = 1;
            var xStr = Convert.ToString(x, 2).PadLeft(inputSize, '0');

            var outputs = new Dictionary<string, bool>();
            foreach (var ch in new[] { 'x', 'y' })
            {
                //random
                //var max = (1L << inputSize);
                //var input = rand.NextInt64(max);
                //if (ch == 'x') x = input; else y = input;

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

            //output bits is always one more than input bits
            var compBits = solve(outputs, _gates);
            var compSum = getDecimal(compBits);
            var actualSum = x + y;
            var actualBits = getOutputBits(actualSum);

            if (compSum != actualSum)
            {
                if (bit > bitFailedAt)
                {
                    var failedAtStr = Convert.ToString(x, 2).PadLeft(inputSize + 1, '0');
                    Console.WriteLine($"Failed at {x} / {failedAtStr}, swapping gates {g1},{g2}");
                    bitFailedAt = bit;
                }
                break;
            }

            var numberMatchingBits = compBits.Zip(actualBits).Count(tp => tp.First == tp.Second);
            //averages.Add((g1, g2), numberMatchingBits);
            //totalMatchingBits += numberMatchingBits;
        }

        //swap back!
        gates[g1].z = g1z;
        gates[g2].z = g2z;
    }

var results = averages.OrderByDescending(a => a.Value).ToList();
var results2 = averages.OrderBy(a => a.Value).ToList();

Console.WriteLine();

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
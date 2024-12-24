var files = File.ReadAllText("test.txt").Split("\r\n\r\n");
var outputs = files[0].Split("\r\n").Select(line => line.Split(": ")).Select(arr => (arr[0], arr[1] == "1")).ToDictionary();
(string a, string b, string c, string operation)[] gates = files[1].Split("\r\n").Select(line => line.Split(" -> ")).Select(arr =>
{
    var sp2 = arr[0].Split(" ");
    return ((sp2[0], sp2[2], arr[1], sp2[1]));

}).ToArray();

bool finished;
do
{
    finished = true;
    foreach (var g in gates)
    {
        if (outputs.ContainsKey(g.a) && outputs.ContainsKey(g.b) && !outputs.ContainsKey(g.c))
        {
            switch (g.operation)
            {
                case "AND":
                    outputs[g.c] = outputs[g.a] && outputs[g.b];
                    break;
                case "OR":
                    outputs[g.c] = outputs[g.a] || outputs[g.b];
                    break;
                case "XOR":
                    outputs[g.c] = outputs[g.a] ^ outputs[g.b];
                    break;
            }
            finished = false;
        }
    }
} while (!finished);


var bits = String.Join("", outputs.Where(tp => tp.Key.StartsWith("z")).OrderByDescending(tp => tp.Key).Select(kvp => kvp.Value ? "1" : "0").ToArray());
var dec = Convert.ToUInt64(bits, 2);


Console.WriteLine((bits, dec));
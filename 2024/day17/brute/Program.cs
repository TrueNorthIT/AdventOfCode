using System.Diagnostics;

//var file = File.ReadAllText("input.txt").Split("\r\n\r\n");
//var p1Registers = file[0].Split("\r\n").Select(line => line.Split(' ')).Select(arr => long.Parse(arr[2])).ToArray();
//var program = file[1].Split(" ")[1].Split(',').Select(long.Parse).ToArray();

int[] program = [2, 4, 1, 5, 7, 5, 4, 3, 1, 6, 0, 3, 5, 5, 3, 0];
Stopwatch watch = Stopwatch.StartNew();
const long limit = (long)105734774294938 + 1;
const int MaxDOP = 32;
Parallel.For(1L, limit, new ParallelOptions() { MaxDegreeOfParallelism = MaxDOP }, t =>
{
    for (int o = 0; o < program.Length; o++)
    {
        long a = (t * 8 + 1);
        long b = a % 8;
        b = b ^ 5;
        var c = a / (1L << (int)b);
        b = b ^ c;
        b = b ^ 6;
        a = a / 8;
        if ((b % 8) != program[o])
        {
            goto cont;
        }
    }
    Console.WriteLine($"Answer is {t*8 + 1}");
cont:;
});

Console.WriteLine($"Processed {limit} in {watch.ElapsedMilliseconds}ms ({limit/watch.ElapsedMilliseconds} per ms, MaxDOP={MaxDOP})");

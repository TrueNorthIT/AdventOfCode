using System.Diagnostics;
Stopwatch watch = Stopwatch.StartNew();
const int MaxDOP = 32;

int[] program = [2, 4, 1, 5, 7, 5, 4, 3, 1, 6, 0, 3, 5, 5, 3, 0];
var min = 1L << (15 * 3);
var max = 1L << (16 * 3);
Parallel.For(min, max, new ParallelOptions() { MaxDegreeOfParallelism = MaxDOP }, (t, ls) =>
{
    long a = t;
    for (int o = 0; o < program.Length; o++)
    {
        long b = a % 8;
        b = b ^ 5;
        long c = a / (1L << (int) b);
        b = b ^ c;
        b = b ^ 6;
        a = a / 8;
        if ((b % 8) != program[o])
        {
            goto cont;
        }
    }
    Console.WriteLine($"*********************");
    Console.WriteLine($"Answer is {t}");
    Console.WriteLine($"*********************");
    ls.Stop();
cont:;
});

Console.WriteLine($"Processed {max - min} in {watch.ElapsedMilliseconds}ms ({(max - min) / watch.ElapsedMilliseconds} per ms, MaxDOP={MaxDOP})");

var file = File.ReadAllText("input.txt").Split("\r\n\r\n");
var p1Registers = file[0].Split("\r\n").Select(line => line.Split(' ')).Select(arr => long.Parse(arr[2])).ToArray();
var program = file[1].Split(" ")[1].Split(',').Select(long.Parse).ToArray();

long combo(long[] registers, long value) => value switch
{
    >= 0 and <= 3 => value,
    var reg => registers[reg - 4],
};

IEnumerable<long> run(long[] program, long a)
{
    var registers = new long[3];
    registers[0] = a;
    long ip = 0;    
    while (ip < program.Length)
    {
        var opCode = (OpCode)program[ip];
        var operand = program[ip + 1];
        switch (opCode)
        {
            case OpCode.adv:
                var num = registers[0];
                var den = 1L << (int) combo(registers, operand);
                registers[0] = num / den;
                ip += 2;
                break;
            case OpCode.bxl:
                registers[1] = registers[1] ^ operand;
                ip += 2;
                break;
            case OpCode.bst:
                registers[1] = combo(registers, operand) % 8;
                ip += 2;
                break;
            case OpCode.jnz:
                if (registers[0] != 0)
                {
                    ip = operand;
                }
                else
                {
                    ip += 2;
                }
                break;
            case OpCode.bxc:
                registers[1] = registers[1] ^ registers[2];
                ip += 2;
                break;
            case OpCode.output:
                yield return combo(registers, operand) % 8;
                ip += 2;
                break;
            case OpCode.bdv:
                registers[1] = registers[0] / (1L << (int) combo(registers, operand));
                ip += 2;
                break;
            case OpCode.cdv:
                registers[2] = registers[0] / (1 << (int) combo(registers, operand));
                ip += 2;
                break;
        }
    }
}

long current = 0;
for (int word = program.Length - 1; word >= 0; word -= 1)
{
    for (int digit = 0; digit < int.MaxValue; digit++)
    {
        var testing = current + (long)Math.Pow(2, word * 3) * digit;
        var output = run(program, testing);
        if (output.Skip(word).SequenceEqual(program.Skip(word)))
        {
            current = testing;
            Console.WriteLine($"Success at word {word}, digit {digit}, current ={Convert.ToString(testing, 8)} (octal), looking for {program[word]}");
            Console.WriteLine($"Output: [{String.Join(", ", output)}]");
            Console.WriteLine($"Current is now {Convert.ToString(current, 8)} (octal)");
            break;
        }
    }
}
Console.WriteLine($"Part 1: {String.Join(',',run(program, p1Registers[0]))}");
Console.WriteLine($"Part 2: {current} (not in octal!)");

enum OpCode
{
    adv = 0,
    bxl = 1,
    bst = 2,
    jnz = 3,
    bxc = 4,
    output = 5,
    bdv = 6,
    cdv = 7,
}


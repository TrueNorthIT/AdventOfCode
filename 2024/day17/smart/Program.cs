var file = File.ReadAllText("input.txt").Split("\r\n\r\n");
var p1Registers = file[0].Split("\r\n").Select(line => line.Split(' ')).Select(arr => long.Parse(arr[2])).ToArray();
var program = file[1].Split(" ")[1].Split(',').Select(long.Parse).ToArray();

long current = 0;
for (int digit = program.Length - 1; digit >= 0; digit -= 1)
{
    for (int i = 0; i < int.MaxValue; i++)
    {
        var testing = current +  (1L << (digit * 3)) * i;
        var output = run(program, testing, 0, 0);
        if (output.Skip(digit).SequenceEqual(program.Skip(digit)))
        {
            current = testing;
            Console.WriteLine($"Success finding digit {digit} = {program[digit]}, i={Convert.ToString(i, 8)} (octal)");
            Console.WriteLine($"Output: [{String.Join(", ", output)}]");
            Console.WriteLine($"Current is now {Convert.ToString(current, 8)} (octal)");
            break;
        }
    }
}

Console.WriteLine($"Part 1: {String.Join(',', run(program, p1Registers[0], p1Registers[1], p1Registers[2]))}");
Console.WriteLine($"Part 2: {current} / {Convert.ToString(current, 8)} (decimal / octal)");

long combo(long[] registers, long value) => value switch {
    >= 0 and <= 3 => value,
    var reg => registers[reg - 4],
};

IEnumerable<long> run(long[] program, long a, long b, long c)
{
    var registers = new long []{ a, b, c };
    long ip = 0;    
    while (ip < program.Length)
    {
        var opCode = (OpCode)program[ip];
        var operand = program[ip + 1];
        switch (opCode)
        {
            case OpCode.adv:
                registers[0] = registers[0] / (1L << (int) combo(registers, operand));
                break;
            case OpCode.bxl:
                registers[1] = registers[1] ^ operand;
                break;
            case OpCode.bst:
                registers[1] = combo(registers, operand) % 8;
                break;
            case OpCode.jnz:
                if (registers[0] != 0)
                {
                    ip = operand;
                    ip -= 2;
                }
                break;
            case OpCode.bxc:
                registers[1] = registers[1] ^ registers[2];
                break;
            case OpCode.output:
                yield return combo(registers, operand) % 8;
                break;
            case OpCode.bdv:
                registers[1] = registers[0] / (1 << (int) combo(registers, operand));
                break;
            case OpCode.cdv:
                registers[2] = registers[0] / (1 << (int) combo(registers, operand));
                break;
        }
        ip += 2;
    }
}

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


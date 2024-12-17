var file = File.ReadAllText("test.txt").Split("\r\n\r\n");
var registers = file[0].Split("\r\n").Select(line => line.Split(' ')).Select(arr => int.Parse(arr[2])).ToArray();
var program = file[1].Split(" ")[1].Split(',').Select(int.Parse).ToArray();

var ip = 0;

int combo(int value) => value switch
{
    >= 0 and <= 3 => value,
    var reg => registers[reg - 4],
};

var output = new List<int>();
while (true)
{
    if (ip >= program.Length)
    {
        //terminated?
        break;
    }
    var opCode = (OpCode) program[ip];
    var operand = program[ip+1];
    switch (opCode)
    {
        case OpCode.adv:
            var num = registers[0];
            var den = 1 << combo(operand);
            registers[0] = num / den;
            ip += 2;
            break;
        case OpCode.bxl:
            registers[1] = registers[1] ^ operand;
            ip += 2;
            break;
        case OpCode.bst:
            registers[1] = combo(operand) % 8;
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
            output.Add(combo(operand) % 8);
            ip += 2;
            break;
        case OpCode.bdv:
            registers[1] = registers[0] / (1 << combo(operand));
            ip += 2;
            break;
        case OpCode.cdv:
            registers[2] = registers[0] / (1 << combo(operand));
            ip += 2;
            break;
    }
}

Console.WriteLine(String.Join(",", output));

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


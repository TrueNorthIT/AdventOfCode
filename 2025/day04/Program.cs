namespace day04
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var lines = File.ReadAllLines("input.txt");
            string padder = new('.', lines[0].Length + 2);
            var modifiedLines = new[] { padder }.Concat(lines.Select(s => $".{s}.")).Concat([padder]).ToArray();
            Console.WriteLine(modifiedLines.Skip(1).Take(lines.Length).Select((string line, int index) => {
                var modifiedIndex = index + 1;
                return line.Skip(1).Take(lines[0].Length).Select((char chr, int chrIndex) =>
                {
                    var modifiedChrIndex = chrIndex + 1;
                    if (chr == '.') return 0;
                    return $"{modifiedLines[modifiedIndex - 1].Substring(modifiedChrIndex - 1, 3)}{modifiedLines[modifiedIndex].Substring(modifiedChrIndex - 1, 1)}{modifiedLines[modifiedIndex].Substring(modifiedChrIndex + 1, 1)}{modifiedLines[modifiedIndex + 1].Substring(modifiedChrIndex - 1, 3)}".Count(c => c == '.') > 4 ? 1 : 0;
                }).Sum();
            }).Sum());
        }
    }
}

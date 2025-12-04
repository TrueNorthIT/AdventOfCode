using System.Text;

namespace day04
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var lines = File.ReadAllLines("input.txt");
            string[] modifiedLines = Pad(lines);
            int totalRemoved = 0;
            int removedThisTime = 0;
            do
            {
                var linesBuilder = new List<string>();
                removedThisTime = modifiedLines.Skip(1).Take(lines.Length).Select((string line, int index) =>
                {
                    var modifiedIndex = index + 1;
                    var lineBuilder = new StringBuilder();
                    int numToRemove = line.Skip(1).Take(lines[0].Length).Select((char chr, int chrIndex) =>
                    {
                        var modifiedChrIndex = chrIndex + 1;
                        if (chr == '.')
                        {
                            lineBuilder.Append(".");
                            return 0;
                        }
                        bool canRemove = $"{modifiedLines[modifiedIndex - 1].Substring(modifiedChrIndex - 1, 3)}{modifiedLines[modifiedIndex].Substring(modifiedChrIndex - 1, 1)}{modifiedLines[modifiedIndex].Substring(modifiedChrIndex + 1, 1)}{modifiedLines[modifiedIndex + 1].Substring(modifiedChrIndex - 1, 3)}".Count(c => c == '.') > 4;
                        if (canRemove) lineBuilder.Append(".");
                        else lineBuilder.Append("@");
                        return canRemove ? 1 : 0;
                    }).Sum();
                    linesBuilder.Add(lineBuilder.ToString());
                    return numToRemove;
                }).Sum();
                totalRemoved += removedThisTime;
                modifiedLines = Pad(linesBuilder.ToArray());
            } while (removedThisTime > 0);
            Console.WriteLine(totalRemoved);
        }

        private static string[] Pad(string[] lines)
        {
            string padder = new('.', lines[0].Length + 2);
            var modifiedLines = new[] { padder }.Concat(lines.Select(s => $".{s}.")).Concat([padder]).ToArray();
            return modifiedLines;
        }
    }
}

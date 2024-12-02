// See https://aka.ms/new-console-template for more information
using System.Linq;

long Puzzle1()
{
    var list1Builder = new List<int>();
    var list2Builder = new List<int>();
    foreach (var item in File.ReadLines("Input1.txt").Select(s => s.Split(" ", StringSplitOptions.RemoveEmptyEntries)))
    {
        list1Builder.Add(int.Parse(item[0]));
        list2Builder.Add(int.Parse(item[1]));
    }
    long total = 0;
    foreach (var tupleItem in list1Builder.Order().Zip(list2Builder.Order()))
    {
        total += Math.Abs(tupleItem.First - tupleItem.Second);
    }
    return total;
}
long Puzzle2()
{
    var list1Builder = new List<int>();
    var list2Builder = new List<int>();
    foreach (var item in File.ReadLines("Input1.txt").Select(s => s.Split(" ", StringSplitOptions.RemoveEmptyEntries)))
    {
        list1Builder.Add(int.Parse(item[0]));
        list2Builder.Add(int.Parse(item[1]));
    }
    var list2Grouped = list2Builder.GroupBy(item => item).ToDictionary(group => group.Key, group => group.Count());
    long total = 0;
    foreach (var group in list1Builder.GroupBy(item => item))
    {
        if (list2Grouped.TryGetValue(group.Key, out int count))
        { 
            total += group.Key * group.Count() * count;
        }
    }
    return total;
}

Console.WriteLine(Puzzle2());
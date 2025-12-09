var points = File.ReadAllLines("input.txt").Select(line => line.Split(',')).Select(arr => (long.Parse(arr[0]), long.Parse(arr[1])));

var p1ans = (from p1 in points
 from p2 in points
 select (p1,p2,(1 + Math.Abs(p2.Item1 - p1.Item1)) * (1 + Math.Abs(p2.Item2 - p1.Item2)))).ToList();

Console.WriteLine(p1ans.MaxBy(tp => tp.Item3).Item3);
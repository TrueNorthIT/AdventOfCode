namespace day08
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var vectors = File.ReadAllLines("input.txt").Select(s => { var parts = s.Split(","); return new Vector { X = int.Parse(parts[0]), Y = int.Parse(parts[1]), Z = int.Parse(parts[2]) }; }).ToArray();
            var spacings = vectors.Take(vectors.Length - 1).SelectMany((vector, index) => {
                return vectors.Skip(index + 1).Select((vector2, index2) => new Spacing { Idx1 = index, Idx2 = index2 + index + 1, Distance = vector.DistanceFrom(vector2) });
            }).OrderBy(sp => sp.Distance).ToArray();
            var connections = new Dictionary<int, List<int>>();
            foreach (var spacing in spacings.Take(1000))
            {
                Console.WriteLine("Distance {0} connecting {1} and {2}", spacing.Distance, spacing.Idx1, spacing.Idx2);
                if (!connections.TryGetValue(spacing.Idx1, out var connectedTo))
                {
                    connectedTo = new List<int>();
                }
                connectedTo.Add(spacing.Idx2);
                connections[spacing.Idx1] = connectedTo;
                if (!connections.TryGetValue(spacing.Idx2, out var connected2To))
                {
                    connected2To = new List<int>();
                }
                connected2To.Add(spacing.Idx1);
                connections[spacing.Idx2] = connected2To;
            }
            var count = 0;
            var accountFor = new HashSet<int>();
            var circuitSizes = new List<int>();
            for (var i = 0; i < vectors.Length; i++)
            {
                if (!accountFor.Contains(i))
                {
                    var circuitElements = new HashSet<int>(i);
                    count++;
                    accountFor.Add(i);
                    AddElements(connections, circuitElements, i);
                    foreach (var element in circuitElements) accountFor.Add(element);
                    circuitSizes.Add(circuitElements.Count);
                    Console.WriteLine(string.Join(", ", circuitElements));
                }
            }
            Console.WriteLine("{0} circuits", count);
            Console.WriteLine(circuitSizes.OrderByDescending(i => i).Take(3).Aggregate((i, j) => i * j));
        }

        static void AddElements(Dictionary<int, List<int>> connections, HashSet<int> thisSet, int i)
        {
            if (connections.TryGetValue(i, out var connectedTo))
            {
                var explore = new List<int>();
                foreach (var connection in connectedTo)
                {
                    if (!thisSet.Contains(connection))
                    {
                        explore.Add(connection);
                        thisSet.Add(connection);
                    }
                }
                foreach (var connection in explore)
                {
                    AddElements(connections, thisSet, connection);
                }
            }

        }

        private class Vector
        {
            public double X { get; set; }
            public double Y { get; set; }
            public double Z { get; set; }

            public double DistanceFrom(Vector other)
            {
                return Math.Sqrt(Math.Pow(this.X - other.X, 2) + Math.Pow(this.Y - other.Y, 2) + Math.Pow(this.Z - other.Z, 2));
            }
        }

        private class Spacing
        {
            public int Idx1 { get; set; }
            public int Idx2 { get; set; }
            public double Distance { get; set; }
        }
    }
}

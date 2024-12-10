namespace day10
{
    internal class Program
    {
        static void Main()
        {
            var results = new List<Trail>();
            var points = File.ReadAllLines("input.txt").Select((l, yIndex) => l.Select((c, xIndex) => new Point { Height = int.Parse(c.ToString()), X = xIndex, Y = yIndex }).ToArray()).ToArray();
            for (var yIndex = 0; yIndex < points.Length; yIndex++)
            {
                var pointsLine = points[yIndex];
                for (var xIndex = 0; xIndex < pointsLine.Length; xIndex++)
                {
                    var point = pointsLine[xIndex];
                    if (point.Height == 0)
                    {
                        foreach (var ninePoint in FindDestinations(points, point, new List<Point>())) results.Add(new Trail { Destination = ninePoint, Origin = point });
                    }
                }
            }
            Console.WriteLine(results.Count);
        }

        private static T FindDestinations<T>(Point[][] allPoints, Point current, T addTo)
            where T: ICollection<Point>
        {
            void CheckPoint(Point point, int x_delta, int y_delta)
            {
                if (point.X + x_delta < 0 || point.X + x_delta  >= allPoints[0].Length || point.Y + y_delta < 0 || point.Y + y_delta >= allPoints.Length) return;

                var nextPoint = allPoints[current.Y + y_delta][current.X + x_delta];
                if (nextPoint.Height == point.Height + 1)
                {
                    if (current.Height == 8) addTo.Add(nextPoint);
                    else FindDestinations(allPoints, nextPoint, addTo);
                }
            }

            CheckPoint(current, -1, 0);
            CheckPoint(current, 1, 0);
            CheckPoint(current, 0, -1);
            CheckPoint(current, 0, 1);

            return addTo;
        }

        private class Trail
        {
            public Point Origin { get; set; }

            public Point Destination { get; set; }

            public override int GetHashCode()
            {
                return Origin.GetHashCode() ^ Destination.GetHashCode();
            }

            public override bool Equals(object? obj)
            {
                var castObject = obj as Trail;
                return Origin.Equals(castObject.Origin) && Destination.Equals(castObject.Destination);
            }
        }

        private class Point
        { 
            public int X; 
            public int Y;
            public int Height;

            public override int GetHashCode()
            {
                return X.GetHashCode() ^ Y.GetHashCode();
            }

            public override bool Equals(object? obj)
            {
                var castObject = obj as Point;
                return castObject?.X == this.X && castObject?.Y == this.Y;
            }
        }
    }
}

//C# Pattern Matchingor
{
    //Switch Expression
    var answer = new double[] { 10, 20, 30, 40, 150, 90 } switch { 
        [var x1, var y1, var x2, var y2, var xp, var yp] 
            => (yp * x2 - xp * y2 / (y1 * x2 - x1 * y2)) switch { var a
            => ((xp - a * x1) / x2) switch {  var b
            => (a, b)           
            }},
        _ => throw new Exception($"Expected 6 elements in the array")};

    Console.WriteLine($"a={answer.a}, b={answer.b}");
    Console.WriteLine($"a={answer.a}, b={answer.b}");
}
{
    //Ternary style
    var answer = new double[] { 10, 20, 30, 40, 150, 90 }
        is [var x1, var y1, var x2, var y2, var xp, var yp]
            ? (yp * x2 - xp * y2 / (y1 * x2 - x1 * y2)) is var a
            ? ((xp - a * x1) / x2) is var b
            ? (a, b) 
            : default : default : 
        throw new Exception($"Expected 6 elements in the array");
    
    Console.WriteLine($"a={answer.a}, b={answer.b}");
    Console.WriteLine($"a={answer.a}, b={answer.b}");
}

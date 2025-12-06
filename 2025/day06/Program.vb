Imports System.IO

Module Program
    Function Splitter(line As String) As Long()
        Return line.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(Of Long)(Function(s) Long.Parse(s)).ToArray()
    End Function

    Sub Main(args As String())
        Dim lines() As String = File.ReadAllLines("input.txt")
        Dim nums() = lines.Take(lines.Length - 1).Select(Function(s) Splitter(s)).ToArray()
        Dim ops() As String = lines.TakeLast(1).First().Split(" ", StringSplitOptions.RemoveEmptyEntries).ToArray()
        Dim total As Long = 0
        For index = 0 To ops.Length - 1
            If ops(index) = "+" Then
                Dim colSum As Long = nums.Sum(Function(arr) arr(index))
                Console.WriteLine("Sum {0}", colSum)
                total = total + colSum
            ElseIf ops(index) = "*" Then
                Dim colProduct As Long = nums.Skip(1).Aggregate(nums(0)(index), Function(soFar, element) soFar * element(index))
                Console.WriteLine("Prd {0}", colProduct)
                total = total + colProduct
            End If
        Next index

        Console.WriteLine(total)
    End Sub
End Module

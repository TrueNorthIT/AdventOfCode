Imports System.IO

Module Program
    Function Splitter(line As String) As Long()
        Return line.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(Of Long)(Function(s) Long.Parse(s)).ToArray()
    End Function

    Sub Main(args As String())
        Dim lines() As String = File.ReadAllLines("input.txt")
        Dim numsBuilderBuilder As List(Of Long()) = New List(Of Long())
        Dim numsBuilder As List(Of Long) = New List(Of Long)
        Dim numStr As String
        For builderIndex = 0 To lines(0).Length - 1
            numStr = String.Join("", lines.Take(lines.Length - 1).Select(Function(line) line.Substring(builderIndex, 1)))
            If numStr.Trim() = "" Then
                numsBuilderBuilder.Add(numsBuilder.ToArray())
                numsBuilder = New List(Of Long)
            Else
                numsBuilder.Add(Long.Parse(numStr))
            End If
        Next
        If numsBuilder.Any() Then
            numsBuilderBuilder.Add(numsBuilder.ToArray())
        End If
        Dim ops() As String = lines.TakeLast(1).First().Split(" ", StringSplitOptions.RemoveEmptyEntries).ToArray()
        Dim total As Long = 0
        For index = 0 To ops.Length - 1
            If ops(index) = "+" Then
                Dim colSum As Long = numsBuilderBuilder(index).Sum()
                Console.WriteLine("Sum {0}", colSum)
                total = total + colSum
            ElseIf ops(index) = "*" Then
                Dim colProduct As Long = numsBuilderBuilder(index).Skip(1).Aggregate(numsBuilderBuilder(index)(0), Function(soFar, element) soFar * element)
                Console.WriteLine("Prd {0}", colProduct)
                total = total + colProduct
            End If
        Next index

        Console.WriteLine(total)
    End Sub
End Module

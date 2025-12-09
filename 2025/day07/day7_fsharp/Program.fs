let lines = System.IO.File.ReadAllLines("input.txt")
let R, C = lines.Length, lines[0].Length
let mutable p1 = 0L
let (p2Totals : int64 array array) = [| for _ in 1 .. R -> [| for _ in 1 .. C -> 0L|]|]

for c = 0 to lines[0].Length - 1 do
    p2Totals[0][c] <- if lines[0][c] = 'S' then 1 else 0
    p2Totals[0][c] <- if lines[0][c] = 'S' then 1 else 0

for r = 1 to lines.Length - 1 do
    for c = 0 to lines[0].Length - 1 do
        p2Totals[r][c] =
            match lines[r][c] with
                | '.' -> if c - 1 > 0 && lines[r][c-1] = '^' then p2Totals[r-1][c-1] else 0
                        + if c + 1 < lines[0].Length && lines[r][c+1] = '^' then p2Totals[r-1][c+1] else 0
                        + p2Totals[r-1][c]
                | _ -> 0
        |> ignore;
        p1 <- p1 + if p2Totals[r-1][c] > 0 && lines[r][c] = '^' then 1L else 0

let mutable p2 = 0L
for c = 0 to lines[0].Length - 1 do
    p2 <- p2 + p2Totals[lines.Length - 1][c]

printfn $"Part 1: {p1}";
printfn $"Part 2: {p2}";

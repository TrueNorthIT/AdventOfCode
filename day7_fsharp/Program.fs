let lines = System.IO.File.ReadAllLines("input.txt")
let (totals : int64 array2d) = Array2D.zeroCreate lines.Length lines[0].Length

for c = 0 to lines[0].Length - 1 do
    Array2D.set totals 0 c (if lines[0][c] = 'S' then 1 else 0)

for r = 1 to lines.Length - 1 do
    for c = 0 to lines[0].Length - 1 do
        let v = match lines[r][c] with
                | '.' -> if c - 1 > 0 && lines[r][c-1] = '^' then totals[r-1,c-1] else 0
                        + if c + 1 < lines[0].Length && lines[r][c+1] = '^' then totals[r-1,c+1] else 0
                        + totals[r-1,c]
                | _ -> 0;
        Array2D.set totals r c v

let mutable p2 = 0L
for c = 0 to lines[0].Length - 1 do
    p2 <- p2 + totals[lines.Length - 1,c]

printfn $"Part 2: {p2}";

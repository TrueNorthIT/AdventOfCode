let equations = System.IO.File.ReadAllLines("input.txt")
                |> Array.map  
                    (fun str -> 
                        let sp = str.Split(": ")
                        (int64 sp[0], Array.map int64 (sp[1].Split(' '))))

let concat (a : int64) (b : int64) = a * pown 10L (double b + 1.0 |> log10 |> ceil |> int) |> int64 |> (+) b

let rec possible (target, ops : _ array) total i p2 = 
    if i >= ops.Length 
    then total = target
    else  ( possible (target, ops) (total + ops[i]) (i + 1) p2
            || possible (target, ops) (total * ops[i]) (i + 1) p2
            || (p2 && possible (target, ops) (concat total ops[i]) (i + 1) p2))

let solve p2 =  Array.filter (fun (target, ops) -> possible (target, ops) ops[0] 1 p2) equations 
                |> Array.sumBy fst

printfn $"Part 1: {solve false}";
printfn $"Part 2: {solve true}";
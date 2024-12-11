main = do
  contents <- readFile "input.txt"
  let value = read $ head $ lines contents::Int 
  print value
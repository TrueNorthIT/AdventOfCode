import Data.Function.Memoize
fj (Just a) = a
main = do
 content <- readFile "input.txt"
 print $ count' content (0::Int) "svr"

count' = memoize3 count
count ct s "out" = if s == 3 then 1 else 0 
count ct s node  = foldr (\a n -> n + count' ct (s + if node == "dac" then 1 else if node == "fft" then 2 else 0)  a) 0 (fj $ lookup node $  map ((\(s:ss) -> (init s,ss)) . words) (lines ct))
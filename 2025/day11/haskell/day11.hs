import Data.Function.Memoize
main = do
    content <- readFile "input.txt"    
    let parsed = map (\(s:ss) -> (init s,ss)) $ map words $ lines content
    let next node = snd $ head $ filter (\(key,values) -> key == node) parsed
    let count' = memoize3 count where
        count dac fft "out" = if dac && fft then 1 else 0
        count dac fft node  = foldr (\a n -> n + count' (dac || (node == "dac")) (fft || (node == "fft"))  a) 0 (next node)
    print $ count' False False "svr"
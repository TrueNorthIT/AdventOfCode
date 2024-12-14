import Data.List
main = do
    content <- readFile "input.txt"
    let ls = map (\[s1,s2] -> (read s1, read s2)) $ map words $ lines content
    let p1 = sum $ map abs $ zipWith (-) (sort $ map fst ls) (sort $ map snd ls)
    print p1
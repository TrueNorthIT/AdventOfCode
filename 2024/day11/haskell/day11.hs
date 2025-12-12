import Data.Function.Memoize
main = do
    content <- readFile "input.txt"
    print [sum $ map (memoized_count s) $ map read $ words content | s <- [25, 75]]

memoized_count :: Integer -> Integer -> Integer        
memoized_count = memoize2 count where 
    count 0 _ = 1
    count step 0 = memoized_count (step - 1) 1
    count step tile
        |   mod (decimalLength tile) 2 == 0,
            let (div,rem) = halves tile
            = sum $ map (memoized_count (step-1)) [div, rem]
        | otherwise = memoized_count (step-1) $ tile * 2024

decimalLength a  = toInteger $ ceiling $ logBase 10 $ fromIntegral a + 1
halves a = divMod a $ (^) 10 $ fst $ divMod (decimalLength a) 2
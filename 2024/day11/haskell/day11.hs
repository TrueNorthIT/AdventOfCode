    import Data.Function.Memoize
    main = do
        content <- readFile "input.txt"
        print [sum $ map (memoized_count s) $ map read $ words content | s <- [25, 75]]

    memoized_count :: Integer -> Integer -> Integer        
    memoized_count = memoize2 count where 
        count 0 _ = 1
        count step 0 = memoized_count (step - 1) 1
        count step tile
            |   mod (digits tile) 2 == 0
                = sum $ map (memoized_count (step-1)) $ split tile
            | otherwise = memoized_count (step-1) $ tile * 2024

    digits a  = toInteger $ ceiling $ logBase 10 $ fromIntegral a + 1
    split a =  [div,rem] where (div,rem) = divMod a $ (^) 10 $ fst $ divMod (digits a) 2
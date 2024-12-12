    import Data.Function.Memoize
    main = do
        content <- readFile "input.txt"
        print [sum $ map (memoizedCount s . read) $ words content | s <- [25, 75]]

    memoizedCount :: Integer -> Integer -> Integer
    memoizedCount = memoize2 count where
        count 0 _ = 1
        count step 0 = descend step 1
        count step tile
            |   even $ length $ show tile
                = sum . map (descend step) $ split tile
            | otherwise = descend step $ tile * 2024
        descend = memoizedCount . flip (-) 1
    
    split i = map (\f -> read $ f l str) [take, drop] 
        where str = show i; l = length str `div` 2
    
    --digits a  = toInteger $ ceiling $ logBase 10 $ fromIntegral a + 1
    --split a =  [div,rem] where (div,rem) = divMod a $ (^) 10 $ fst $ divMod (digits a) 2
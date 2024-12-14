main = do
    content <- readFile "input.txt"
    map $ words content
    print 0

count 0 _ = 1
count step 0 = descend step 1
count step (tile :: Int)
    |   even $ length $ show tile
        = sum . map (descend step) $ split tile
    | otherwise = descend step $ tile * 2024
descend = count . flip (-) 1

split i = map (\f -> read $ f l str) [take, drop] 
    where str = show i; l = length str `div` 2
    
    --digits a  = toInteger $ ceiling $ logBase 10 $ fromIntegral a + 1
    --split a =  [div,rem] where (div,rem) = divMod a $ (^) 10 $ fst $ divMod (digits a) 2
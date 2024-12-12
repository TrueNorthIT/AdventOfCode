import Data.Function.Memoize
main = do
 f <- readFile "input.txt"
 print [sum $ map (r s . read) $ words f | s <- [25 :: Int, 75]]
r = memoize2 c where
 c 0 _ = 1
 c p 0 = d p 1
 c p (t :: Int) | even $ length $ show t = sum . map (d p) $ s t
 c p t = d p $ t * 2024
 d = r . flip (-) 1
 s i = map (\f -> read $ f l h) [take, drop] where h = show i; l = length h `div` 2
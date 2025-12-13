import Data.Function.Memoize
f (Just a) = a
main = do
 c<-readFile "input.txt"
 print$p c(0::Int)"svr"

p = memoize3 q
q c s "out"=if s==3 then 1 else 0 
q c s d  = foldr (\a n->n+p c(s+if d=="dac" then 1 else if d=="fft" then 2 else 0)a)0$f$lookup d$map((\(s:t)->(init s,t)).words)$lines c
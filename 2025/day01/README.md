# Day 01
## I used  Godot Game engine and its Gdscript language (it's python like)

# Star 1 
- Used modulus arithmetic (Its 100 not 99 )
- Count how many times value % 100 = 0

# Star 2
- Made own modulus counting function so I know how many revolutions were made with a single transformartion (start=50,R1000 would equal 10 revolutions)
- Needed to also take into account moving from - to + numbers as that also counts as a 'revolution'
- Needed to make sure I don't count going to 0 twice. eg start=50,R50 would equal 1 revolution. Before I counted going pass 0 and staying as 0 TWICE which resulted in too big of a number
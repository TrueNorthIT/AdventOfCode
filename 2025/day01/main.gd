extends Node2D
var begining = 50
var count = 0


#MODULO BUT WE ARE RANGING FROM -100 TO 100
# We need to be able to count how many times we perform either + or -
func own_modulo(current,next):
	var revolution_count = 0
	var new_current = current + next
	## We need to add 1 if the revolution changes sign with the first operation
	if (((current < 0) and (new_current > 0)) 
		or ((current > 0) and (new_current < 0))):
		revolution_count += 1

	if new_current <= -100:
		while new_current <= -100:
			if new_current == -100:
				##Im counting 0 twice in some cases
				revolution_count -=1
			new_current += 100
			revolution_count +=1
			
	elif new_current >= 100:
		while new_current >= 100:
			if new_current == 100:
					##Im counting 0 twice in some cases
				revolution_count -=1
			new_current -=100
			revolution_count+=1
	if new_current == 0:
		revolution_count += 1
	#print("R:",new_current," Number:",revolution_count)
	return revolution_count
	

func load_from_file():
	var file = FileAccess.open("res://input.txt", FileAccess.READ)
	return file

func read_text(file):
	while not file.eof_reached():
		var content = file.get_csv_line()
		strip_instruction(content)
	return
	
func strip_instruction(input):
	#print(input[0])
	var code : String = input[0]
	if code.begins_with("R"):
		var sub_s = code.lstrip("R").to_int()
		math(begining,sub_s)
	elif code.begins_with("L"):
		var sub_s = code.lstrip("L").to_int()
		math(begining,-sub_s)
	return
	
	
func math(current:int, next:int):
	var expression = Expression.new()
	expression.parse("(x + y) % 100",["x","y"])
	var result = expression.execute([current,next])
	
	##Number of revolutions per translation
	var revolution = own_modulo(current,next)
	count += revolution
	
	begining = result
	if begining == 0:
		pass
		#count+=1
	print(result)
	

	
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	var file = load_from_file()
	read_text(file)
	print("C:",count)
	### Im not counting transformations when we go from -50 to 50 (That is still one rotation) (Done)
	#own_modulo(50,50)
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

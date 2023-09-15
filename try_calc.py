from sum_of_two_integer import Interpreter

interpreter = Interpreter(text="1+3")

print(interpreter.get_next_token(),
      interpreter.get_next_token(),
      interpreter.get_next_token(),
      interpreter.get_next_token())

print("Hello123")

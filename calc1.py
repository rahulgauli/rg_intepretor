#token types
#
#EOF (End-of-file) token is used to indicate that 
# there is no more input left for lexical analysis
#IGNORE token is used to indicate that 
#this is a white space and can be ignore during calculation

INTEGER, PLUS, MINUS, MULTIPLY, EOF, IGNORE = "INTEGER", "PLUS", "MINUS", "MULTIPLY", "EOF", "IGNORE"

class Token(object):
    def __init__(self, type, value):
        #token type: INTEGER, PLUS, MINUS, EOF or IGNORE
        self.type = type 
        #token value: 0,1,2,3,4,5,6,7,8,9,+,-, or None
        self.value = value 

    def __str__(self):
        """
            String Representation of the class Instance.
        """
        return 'TOKEN({type}, {value})'.format(
            type = self.type,
            value=repr(self.value)
        )

class Interpreter(object):
    def __init__(self, text):
        self.text = text 
        #client string input e.g "3+5"
        self.pos = 0
        #current token instance 
        self.current_token = None 
    
    def error(self):
        raise Exception("Error Parsing Input")

    def get_next_token(self):
        """Lexical Analyzer Also known as scanner or Tokenizer
        This method is responsible for breaking a sentence apart into tokens. 
        One token at a time.
        """
        text = self.text

        #is self.pos index past the end of the self.text?
        #if so, then reutnr EOF token because there is no more input
        #left to convert into tokens
        if self.pos > len(text) -1:
            return Token(EOF, None)
        #get a character at the position self.pos and decide what 
        #token to create based on the single character 
        current_char = text[self.pos]

        #if the character is a digit then convert it to 
        #integer, create an Integer Token, increment self.pos 
        #index to point to the next character after the digit 
        #and return the integer token 

        if current_char.isdigit():
            token = Token(INTEGER, current_char)
            self.pos += 1 
            return token 
        
        if current_char == "+":
            token = Token(PLUS, current_char)
            self.pos += 1 
            return token 
        
        if current_char == "-":
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == " ":
            token = Token(IGNORE, current_char)
            self.pos += 1
            return self.get_next_token() 
        
        if current_char == "*":
            token = Token(MULTIPLY, current_char)
            self.pos += 1
            return token

        self.error()
    
    def eat(self, token_type):
        #compare the current token type with the passed token 
        #type and if they match then "eat" the current token
        #and assign the next token to the self.current_token
        #otherwise raise an exception
        #helper method

        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def _opr(self, to_op, left_integer, right_integer):        
        if to_op.type == PLUS:
            return (left_integer + right_integer)
        elif to_op.type == MINUS:
            return (left_integer - right_integer)
        elif to_op.type == MULTIPLY:
            return (left_integer * right_integer)

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # we expect the current token to be a single-digit integer
        left_integer = ""
        while self.current_token.type == INTEGER:
            if left_integer == "":
                left_integer = self.current_token.value
            else:
                left_integer = left_integer + self.current_token.value 
            self.eat(INTEGER)

        # we expect the current token to be a '+' token
        op = self.current_token
        to_op = op
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        elif op.type == MULTIPLY:
            self.eat(MULTIPLY)

        # we expect the current token to be a single-digit integer
        right_integer = ""
        while self.current_token.type == INTEGER:
            if right_integer == "":
                right_integer = self.current_token.value
            else:
                right_integer = right_integer + self.current_token.value
            self.eat(INTEGER)
        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectively interpreting client input
        result = self._opr(to_op, int(left_integer), int(right_integer))
        return result

def main():
    while True:
        try:
            #To run under python3 replace "raw_input" call 
            #with "input"
            text = input("calc1> ")
        except EOFError:
            break 
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
    
if __name__ == '__main__':
    main()

"""
Notes: 
A token is an object that has a type and a value.
The process of breaking the input string into tokens
is called lexical analysis
Read the input and convert it into a stream of tokens.
The part of the interpreter that does it is called a lexical analyzer
lexer, scanner, or tokenizer

"""
from lark import Lark

sEBNF= '''start: "(" values (values | start)* ")"

         values: operators
            | NUMBER
            | "true" -> true
            | "null" -> null
            | "false" -> false
            | "var" -> var
            | "set" -> set
            | "block" -> block
            | "while" -> while
            | "if" -> if
            | STRING
            | WORD

         operators: "+" -> plus
               | "-" -> minus
               | "*" -> multiply
               | "/" -> divide
               | "%" -> modulous
               | "!=" -> not_equal 
               | "==" -> equal
               | "<=" -> less_than_equal 
               | "<" -> lesser
               | ">=" -> greater_than_equal 
               | ">" -> greater 

         %import common.WORD
         %import common.WS_INLINE
         %import common.ESCAPED_STRING -> STRING
         %import common.NUMBER
         %import common.WS
         %ignore WS
'''

l = Lark('''start: INT "+" INT ";"
           
            %import common.INT   // imports from terminal library
            %ignore " "           // Disregard spaces in text
         ''')

print( l.parse("1 + 2;").pretty())

p = Lark(sEBNF)
print(p.parse("(var sum (>= 1 2))"))
print(p.parse('(var sum "sum")'))
print(p.parse('(var sum true)'))
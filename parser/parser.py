from lark import Lark, Transformer, Visitor

sEBNF= '''start: "(" values (values | start)* ")"

         values: operators
            | special
            | NUMBER
            | STRING
            | WORD

         special:  "true" -> true
            | "null" -> null
            | "false" -> false
            | "var" -> var
            | "set" -> set
            | "block" -> block
            | "while" -> while
            | "if" -> if

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

class V(Visitor):
   pass

class T(Transformer):
   NUMBER = float
   WORD = str
   STRING = str
   def start(self, children):
      print(f"Inside start{children} \n{self.__dict__} \n")
      #   from IPython import start_ipython
      #   start_ipython(argv=[], user_ns=locals())
      if len(children) == 3:
         return [i[0] if len(i) == 1 else i for i in [self.transform(children[0]), self.transform(children[1]), self.transform(children[2]) ]]
      elif len(children) == 1:
         return self.transform(children[0])
      else:
         raise Exception(f"The number of children are not 3 but {len(children)}")
      
   def plus(self, children):
      print(f"Inside plus {children} \n")
      return '+'
   
   def var (self, c):
      print(f"Inside var {c} \n")
      return "var"
 
   def values(self,v):
      return v
    

print( l.parse("1 + 2;").pretty())

p = Lark(sEBNF)
pt = Lark(sEBNF, parser="lalr", transformer=T())
print(p.parse("(var sum (>= 1 2))"))
# print(pt.parse("(var sum (>= 1 2))"))
print(pt.parse("(2)"))
print(pt.parse("(var sum (+ 2 1))"))
# print(p.parse('(var sum "sum")'))
# print(p.parse('(var sum true)'))
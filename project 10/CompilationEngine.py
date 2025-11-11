
import typing
from JackTokenizer import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output_stream = output_stream



    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.output_stream.write("<class>" + "\n")
        self.tokenizer.advance()  # Consume 'class' keyword
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")
        self.tokenizer.advance()  # Consume class name identifier
        self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
        self.tokenizer.advance()  # Consume '{'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()

        while self.tokenizer.keyword() in ["static", "field"]:
            self.compile_class_var_dec()

        # Compile subroutineDec*
        while self.tokenizer.keyword() in ["constructor", "function", "method"]:
            #print(self.tokenizer.keyword())
            self.compile_subroutine()

        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.output_stream.write("</class>" + "\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.output_stream.write("<classVarDec>" + "\n")
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # static or field
        self.tokenizer.advance()  # Consume type (int, char, boolean, or className)
        self.compile_type()
          # Consume varName
        self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
        self.tokenizer.advance()
        # Compile (',' varName)*
        while self.tokenizer.symbol() == ',':
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")  # ,
            self.tokenizer.advance()  # Consume varName
            self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
            self.tokenizer.advance()

        # Consume ';'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        self.output_stream.write("</classVarDec>" + "\n")


    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.output_stream.write("<subroutineDec>" + "\n")
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # constructor, function, or method
        self.tokenizer.advance()  # Consume return type (void, int, char, boolean, or className)

        self.compile_type()

        self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
        self.tokenizer.advance()  # Consume '('

        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        self.compile_parameter_list()
         # Consume ')'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        self.compile_subroutine_body()
        self.output_stream.write("</subroutineDec>" + "\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        # Your code goes here!
        self.output_stream.write("<parameterList>" + "\n")
        # Check if there are parameters
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ')':
            #self.tokenizer.advance()  # Consume type
            self.compile_type()
            # Consume varName
            self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
            self.tokenizer.advance()
            # Compile (',' type varName)*
            while self.tokenizer.symbol() == ',':
                self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")  # ,
                self.tokenizer.advance()  # Consume type
                self.compile_type()
                 # Consume varName
                self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
                self.tokenizer.advance()

        self.output_stream.write("</parameterList>" + "\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.output_stream.write("<varDec>\n")
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # var
        self.tokenizer.advance()  # Consume type
        self.compile_type()
        # Consume varName
        self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
        self.tokenizer.advance()
        # Compile (',' varName)*
        while self.tokenizer.symbol() == ',':
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")  # ,
            self.tokenizer.advance()  # Consume varName
            self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
            self.tokenizer.advance()

          # Consume ';'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.output_stream.write("</varDec>" + "\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.output_stream.write("<statements>" + "\n")

        while self.tokenizer.keyword() in ["let", "if", "while", "do", "return"]:
            if self.tokenizer.keyword() == "if":
                self.compile_if()
            else:
                if self.tokenizer.keyword() == "let":
                    self.compile_let()
                
                if self.tokenizer.keyword() == "while":
                    self.compile_while()
                if self.tokenizer.keyword() == "do":
                    self.compile_do()
                if self.tokenizer.keyword() == "return":
                    self.compile_return()

                self.tokenizer.advance()
                

        self.output_stream.write("</statements>" + "\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.output_stream.write("<doStatement>" + "\n")
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # do
        self.tokenizer.advance()  # Consume subroutineCall
        self.compile_subroutine_call()
          # Consume ';'

        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.output_stream.write("</doStatement>" + "\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.output_stream.write("<letStatement>\n")
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # let
        self.tokenizer.advance()  # Consume varName
        self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
        self.tokenizer.advance()
        # Check if it's an array access
        if self.tokenizer.symbol() == "[":
            #self.tokenizer.advance()  # Consume '['
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()
            self.compile_expression() # Consume ']'
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()
            
          # Consume '='
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        
        self.compile_expression()  # Consume ';'
        
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.output_stream.write("</letStatement>" + "\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.output_stream.write("<whileStatement>\n")
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # while
        self.tokenizer.advance()  # Consume '('
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        self.compile_expression()  # Compile expression inside '(' ')'
         # Consume ')'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()  # Consume '{'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        self.compile_statements()  # Compile statements inside '{' '}'
          # Consume '}'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        
        self.output_stream.write("</whileStatement>" + "\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.output_stream.write("<returnStatement>" + "\n")

        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # return
        self.tokenizer.advance()
        # Compile expression if present
        if self.tokenizer.symbol() != ';':
            self.compile_expression()

          # Consume ';'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.output_stream.write("</returnStatement>" + "\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause.
        - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?"""
        
        # Your code goes here!
        self.output_stream.write("<ifStatement>" + "\n")
        self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")  # if
        self.tokenizer.advance()  # Consume '('
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()

        self.compile_expression()  # Compile expression inside '(' ')'
        # Consume ')'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")

        self.tokenizer.advance()  # Consume '{'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()

        self.compile_statements()  # Compile statements inside '{' '}'
         # Consume '}'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()

        # Check for optional 'else' clause
        if self.tokenizer.keyword() == "else":
            self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")
            self.tokenizer.advance()  # Consume '{'
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()
            self.compile_statements()
              # Compile statements inside '{' '}'
              # Consume '}'
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()


        self.output_stream.write("</ifStatement>\n")

    


    def compile_subroutine_body(self) -> None:
        """Compile a subroutinebody
        subroutineBody: '{' varDec* statements '}'
        """
        self.output_stream.write("<subroutineBody>" + "\n")
          # Consume '{'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        # Compile varDec*
        while self.tokenizer.keyword() == "var":
            self.compile_var_dec()
            self.tokenizer.advance()
        # Compile statements
        self.compile_statements()  # Consume '}'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        self.output_stream.write("</subroutineBody>\n")

    def compile_type(self) -> None:
        """Compile a type 
        type: 'int' | 'char' | 'boolean' | 'void' | className
        if 'int' | 'char' | 'boolean' | 'void' : compile keywords 
        else compile identifer
        """
        if self.tokenizer.token_type() == "KEYWORD":
            self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")
            self.tokenizer.advance()
        else:
            self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
            self.tokenizer.advance()

    def compile_subroutine_call(self) -> None:
        """Compile subroutine call 
        subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
        """
        # Compile subroutineName or className/varName


        self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
        self.tokenizer.advance()
        
        # Check for method call on object (className or varName)
        if self.tokenizer.symbol() == ".":
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()  # Consume '.'
            # Compile subroutineName
            self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")
            self.tokenizer.advance()

        # Consume '('
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()
        # Compile expressionList
        self.compile_expression_list()
        # Consume ')'
        
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()

        
    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.output_stream.write("<expression>" + "\n")
        self.compile_term()  # Compile first term

        # Compile (op term)*
        while self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            if self.tokenizer.symbol() == "<":
                self.output_stream.write("<symbol> &lt; </symbol>" + "\n")
                
            elif self.tokenizer.symbol() == ">":
                self.output_stream.write("<symbol> &gt; </symbol>" + "\n")
                
            elif self.tokenizer.symbol() == "&":
                self.output_stream.write("<symbol> &amp; </symbol>" + "\n")
            else:
                self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()  # Consume op
            self.compile_term()  # Compile term after op


        self.output_stream.write("</expression>" + "\n")

    def compile_term(self) -> None:
        """Compiles a term. 
        term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.output_stream.write("<term>" + "\n")

        if self.tokenizer.token_type() == "INT_CONST":
            self.output_stream.write(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>" + "\n")
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == "STRING_CONST":
            self.output_stream.write(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>" + "\n")
            self.tokenizer.advance()
            
        elif self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword().lower() in ["true", "false", "null", "this"]:
            self.output_stream.write(f"<keyword> {self.tokenizer.keyword()} </keyword>" + "\n")
            self.tokenizer.advance()

        elif self.tokenizer.symbol() == '(':
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()
            self.compile_expression()
            # Consume ')'
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()

        elif self.tokenizer.symbol() in ["-", "~", "^" , "#"]:
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
            self.tokenizer.advance()
            self.compile_term()

        elif self.tokenizer.token_type() == "IDENTIFIER":
            current_token = self.tokenizer.current_token
            # Check for array entry
            self.tokenizer.advance()

            if self.tokenizer.symbol() == '[':
                self.output_stream.write(f"<identifier> {current_token} </identifier>" + "\n")
                self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")  # Consume '['
                self.tokenizer.advance()
                self.compile_expression()
                # Consume ']'
                self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
                self.tokenizer.advance()

            elif self.tokenizer.symbol() in ['.', '(']:
            # Subroutine call
                self.compile_subroutine_call2(current_token)
            else:
                # Simple variable name
                self.output_stream.write(f"<identifier> {current_token} </identifier>" + "\n")
            
            
        self.output_stream.write("</term>\n")

    def compile_subroutine_call2(self, identifier) -> None:
        """Compile subroutine call
        subroutineCall: subroutineName '(' expressionList ')' | (className | 
                    varName) '.' subroutineName '(' expressionList ')'
        """
        if self.tokenizer.symbol() == ".":
            # Case: (className | varName) '.' subroutineName '(' expressionList ')'
            self.output_stream.write(f"<identifier> {identifier} </identifier>" + "\n")
            self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")  # .
            self.tokenizer.advance()  # Consume '.'
            self.output_stream.write(f"<identifier> {self.tokenizer.identifier()} </identifier>" + "\n")  # subroutineName
            self.tokenizer.advance()  # Consume subroutineName
        else:
            # Case: subroutineName '(' expressionList ')'
            self.output_stream.write(f"<identifier> {identifier} </identifier>" + "\n")

        # Consume '('
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance()  # Consume '('
        self.compile_expression_list()
        # Consume ')'
        self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")
        self.tokenizer.advance() 

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.output_stream.write("<expressionList>" + "\n")
        # Check for non-empty expression list
        if self.tokenizer.symbol() != ")":
            self.compile_expression()
            # Compile (',' expression)*
            while self.tokenizer.symbol() == ',':
                self.output_stream.write(f"<symbol> {self.tokenizer.symbol()} </symbol>" + "\n")  # ,
                self.tokenizer.advance()  # Consume ','
                self.compile_expression()

        self.output_stream.write("</expressionList>" + "\n")


import typing

import re
class JackTokenizer:
    """Removes all comments from the input stream and breaks it
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

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self.input_lines = input_stream.read().splitlines()
        self.KEYWORDS = {'class', 'constructor', 'function', 'method', 'field', 'static',
                'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
                'this', 'let', 'do', 'if', 'else', 'while', 'return'}

        self.SYMBOLS = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", 
                        "/", "&", "|", "<", ">", "=", "~"}
        
        self.token_list = self._removes_comments_and_extract()

        self.current_token = None
        self.index = 0

    def _removes_comments_and_extract(self):
        comment_block = False
        raw_tokens = []

        for line in self.input_lines:

            if line.startswith("//"):
                continue

            # Échapper temporairement les '/' à l'intérieur des chaînes entre guillemets
            in_string = False
            processed_line = ""
            for char in line:
                if char == '"':
                    in_string = not in_string
                if in_string and char == '/':
                    processed_line += '\x00'  # Remplace '/' par un caractère temporaire
                else:
                    processed_line += char

            line = processed_line

            if '//' in line:
                line = line.split("//")[0].strip()

            while '/*' in line and '*/' in line:
                start = line.index('/*')
                end = line.index('*/') + 2
                line = line[:start] + line[end:]

            if '/*' in line:
                line = line[:line.index('/*')]
                comment_block = True

            if comment_block and '*/' in line:
                line = line[line.index('*/') + 2:]
                comment_block = False

            if comment_block:
                continue

            # Restaurer les '/' échappés dans les chaînes
            line = line.replace('\x00', '/')
            if line:
                raw_tokens.extend(self._extract_tokens(line))

        return raw_tokens

    def _extract_tokens(self, line: str) -> typing.List[str]:
        tokens = []
        current_token = []
        in_string = False

        for char in line:
            if char == '"':
                if in_string:
                    # Fin de chaîne, ajouter le token complet
                    tokens.append('"' + ''.join(current_token) + '"')
                    current_token = []
                    in_string = False
                else:
                    # Début de chaîne
                    in_string = True
            elif in_string:
                # Ajouter les caractères dans la chaîne
                current_token.append(char)
            elif char.isspace():
                # Séparateur de token, ajouter le token courant s'il existe
                if current_token:
                    tokens.append(''.join(current_token))
                    current_token = []
            elif char in self.SYMBOLS:
                # Si un token est en cours, le terminer
                if current_token:
                    tokens.append(''.join(current_token))
                    current_token = []
                # Ajouter le symbole comme token
                tokens.append(char)
            else:
                # Ajouter le caractère au token en cours
                current_token.append(char)

        # Ajouter le dernier token s'il existe
        if current_token:
            tokens.append(''.join(current_token))

        return tokens

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.index < len(self.token_list)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        if self.has_more_tokens():
            self.current_token = self.token_list[self.index]
            self.index += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.current_token in self.KEYWORDS:
            return "KEYWORD"
        elif self.current_token in self.SYMBOLS:
            return "SYMBOL"
        elif self.current_token.isdigit():
            return "INT_CONST"
        elif self.current_token[0] == '"' and self.current_token[-1] == '"':
            return "STRING_CONST"
        else:
            return "IDENTIFIER"
        

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.current_token

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self.current_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self.current_token

    def int_val(self) -> int:
        """
        Returns:
            int: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return int(self.current_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                    double quote or newline '"'
        """
        return self.current_token[1:-1]

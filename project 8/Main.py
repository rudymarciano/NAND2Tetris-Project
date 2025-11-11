"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = 'C_PUSH'
C_POP = 'C_POP'
C_LABAL = 'C_LABAL'
C_GOTO = 'C_GOTO'
C_IF = 'C_IF'
C_FUNCTION = 'C_FUNCTION'
C_RETURN = 'C_RETURN'
C_CALL = 'C_CALL'
C_Label ='C_LABEL'

def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO,
        bootstrap: bool) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        bootstrap (bool): if this is True, the current file is the
            first file we are translating.
    """
    # Your code goes here!

    code_wr = CodeWriter(output_file)
    parser = Parser(input_file)
    input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    code_wr.set_file_name(input_filename)


    if bootstrap:
       code_wr.initializebootstrap()

    while parser.hasMoreLines():

        parser.advance()
        cur = parser.commandType()
        print(parser.lines)
        if cur in {C_PUSH, C_POP}:
            code_wr.write_push_pop(cur, parser.arg1(), parser.arg2())
        elif cur == C_CALL:
            code_wr.write_call( parser.arg1(), parser.arg2())
        elif cur == C_FUNCTION:
            code_wr.write_function(parser.arg1(), parser.arg2())
        elif cur == C_ARITHMETIC:
            code_wr.write_arithmetic(parser.arg1())
        elif cur == C_IF:
            code_wr.write_if(parser.arg1())
        elif cur == C_LABAL:
            code_wr.write_label(parser.arg1())

        elif cur == C_GOTO:
            code_wr.write_goto(parser.arg1())


        elif cur == C_RETURN:
            code_wr.write_return()
        elif cur == C_Label:
            code_wr.write_label(parser.arg1())


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False

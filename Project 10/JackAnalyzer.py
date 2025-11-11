import os
import sys
import typing
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer


def analyze_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Analyzes a single file.

    Args:
        input_file (typing.TextIO): the file to analyze.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # It might be good to start by creating a new JackTokenizer and CompilationEngine:
    # tokenizer = JackTokenizer(input_file)
    # engine = CompilationEngine(tokenizer, output_file)
    tokenizer = JackTokenizer(input_file)  # Create a JackTokenizer instance
    engine = CompilationEngine(tokenizer, output_file)  # Create a CompilationEngine instance

    if tokenizer.has_more_tokens(): #faire un while 
            engine.compile_class()

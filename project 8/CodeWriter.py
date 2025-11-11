"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

class CodeWriter:
    remember = [0]
    index_2 = 0

    def __init__(self, output_stream: typing.TextIO) -> None:

        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.file_name = None
        self.cur_func = "OS"
        self.lab = 0
        self.arithmetic_commands = {
            "add": "M=D+M\n",
            "sub": "M=M-D\n",
            "and": "M=D&M\n",
            "or": "M=D|M\n",
        }

        self.not_commands = {
            'not': "@SP\nA=M-1\nM=!M\n",
            'neg': "@SP\nA=M-1\nM=-M\n"}

        self.index_gt_lq = 0

        self.segment_map = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }

    def set_file_name(self, filename: str) -> None:
        self.file_name = filename



    def write_gt_lt_eq(self, command: str) -> None:
        self.output_stream.write(f'@SP\nAM=M-1\nD=M\n')
        self.output_stream.write(f'@R14\nM=D\n')
        self.output_stream.write(f'@R13\nM=D\n')
        self.output_stream.write(f'@R13\nD=M\n')
        self.output_stream.write(f'@CASE1_{self.index_gt_lq}\nD;JLT\n')
        self.output_stream.write(f'@SP\nD=M\n')

        self.output_stream.write(f'@SP\nAM=M-1\nD=M\n')
        self.output_stream.write(f'@R13\nM=D\n')

        self.output_stream.write(f'@CASE2_{self.index_gt_lq}\nD;JLT\n')

        self.output_stream.write(f'@R14\nD=D-M\n')
        self.output_stream.write(f'@R13\nM=D\n')
        self.output_stream.write(f'@SP\nD=M\n')
        self.output_stream.write(f'@FINISH_LEVEL1_{self.index_gt_lq}\n0;JMP\n')

        self.output_stream.write(f'(CASE1_{self.index_gt_lq})\n')
        self.output_stream.write(f'@SP\nD=M\n')
        self.output_stream.write(f'@SP\nAM=M-1\nD=M\n')
        self.output_stream.write(f'@CASE3_{self.index_gt_lq}\nD;JGT\n')
        self.output_stream.write(f'@R14\nD=D-M\n')
        self.output_stream.write(f'@R13\nM=D\n')
        self.output_stream.write(f'@SP\nD=M\n')
        self.output_stream.write(f'@FINISH_LEVEL1_{self.index_gt_lq}\n0;JMP\n')

        self.output_stream.write(f'(CASE2_{self.index_gt_lq})\n')
        self.output_stream.write(f'@SP\nD=M\n')
        self.output_stream.write(f'@R13\nM=-1\n')
        self.output_stream.write(f'@FINISH_LEVEL1_{self.index_gt_lq}\n0;JMP\n')

        self.output_stream.write(f'(CASE3_{self.index_gt_lq})\n')
        self.output_stream.write(f'@SP\nD=M\n')
        self.output_stream.write(f'@R13\nM=1\n')
        self.output_stream.write(f'@FINISH_LEVEL1_{self.index_gt_lq}\n0;JMP\n')

        cur = ''
        cur_at = ''
        if command == "eq":
            cur = 'EQ'
            cur_at = f'EQUAL{self.index_gt_lq}'
        elif command == "gt":
            cur = 'GT'
            cur_at = f'X_BIGGER_Y{self.index_gt_lq}'
        elif command == "lt":
            cur = 'LT'
            cur_at = f'Y_BIGGER_X{self.index_gt_lq}'

        self.output_stream.write(f'(FINISH_LEVEL1_{self.index_gt_lq})\n')
        self.output_stream.write(f'@R13\nD=M\n')
        self.output_stream.write(f'@{cur_at}\nD;J{cur}\n')
        self.output_stream.write(f'@SP\nA=M\nM=0\n')
        self.output_stream.write(f'@END{self.index_gt_lq}\n0;JMP\n')
        self.output_stream.write(f'({cur_at})\n')
        self.output_stream.write(f'@SP\nA=M\nM=-1\n')
        self.output_stream.write(f'(END{self.index_gt_lq})\n@SP\nM=M+1\n')
        self.output_stream.write(f'@R14\nM=0\n')
        self.output_stream.write(f'@R13\nM=0\n')
        self.index_gt_lq += 1
        self.remember[0] += 1

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if command in self.arithmetic_commands:
            self.output_stream.write("@SP\n")
            self.output_stream.write("AM=M-1\n")
            self.output_stream.write("D=M\n")
            self.output_stream.write("A=A-1\n")
            self.output_stream.write(self.arithmetic_commands[command])

        elif command == "eq":
            self.output_stream.write("@SP\n")
            self.output_stream.write("AM=M-1\n")
            self.output_stream.write("D=M\n")
            self.output_stream.write("A=A-1\n")
            self.output_stream.write(f"D=M-D\nM=-1\n@END{self.index_gt_lq}\n")
            self.output_stream.write("D;JEQ\n")
            self.output_stream.write(f"@SP\nA=M-1\nM=0\n(END{self.index_gt_lq})\n")
            self.index_gt_lq += 1

        elif command == "lt" or command == "gt":
            self.write_gt_lt_eq(command)


        elif command in self.not_commands:
            self.output_stream.write(self.not_commands[command])


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_PUSH":
            if segment in self.segment_map:
                self.output_stream.write(f"@{self.segment_map[segment]}\n")
                self.output_stream.write("D=M\n")
                self.output_stream.write(f"@{index}\nA=D+A\nD=M\n")
            elif segment == "constant":
                self.output_stream.write(f"@{index}\nD=A\n")

            elif segment == "temp":
                self.output_stream.write(f"@{index}\nD=A\n")
                self.output_stream.write("@R5\nA=D+A\nD=M\n")

            elif segment == "static":
                self.output_stream.write(f"@{self.file_name}.{index}\nD=M\n")


            elif segment == "pointer":
                if index == 0:
                    self.output_stream.write("@THIS\n")  # verifier si c est this
                elif index == 1:
                    self.output_stream.write("@THAT\n")  # verifier si c est that
                self.output_stream.write("D=M\n")

            self.output_stream.write("@SP\n")
            self.output_stream.write("A=M\n")
            self.output_stream.write("M=D\n")
            self.output_stream.write("@SP\n")
            self.output_stream.write("M=M+1\n")

        elif command == "C_POP":
            if segment in self.segment_map:
                self.output_stream.write(f"@{self.segment_map[segment]}\n")
                self.output_stream.write("D=M\n")
                self.output_stream.write(f"@{index}\nD=D+A\n")
                self.output_stream.write("@SP\nAM=M-1\nD=D+M\nA=D-M\nM=D-A\n")
            if segment == "temp":
                self.output_stream.write("@5\n")
                self.output_stream.write("D=A\n")
                self.output_stream.write(f"@{index}\nD=D+A\n")
                self.output_stream.write("@SP\nAM=M-1\nD=D+M\nA=D-M\nM=D-A\n")
            elif segment == "static":
                self.output_stream.write("@SP\nAM=M-1\nD=M\n")
                self.output_stream.write(f"@{self.file_name}.{index}\nM=D\n")
            elif segment == "pointer":
                self.output_stream.write("@SP\nAM=M-1\nD=M\n")
                if index == 0:
                    self.output_stream.write("@THIS\n")
                elif index == 1:
                    self.output_stream.write("@THAT\n")
                self.output_stream.write("M=D\n")

    def write_label(self, label: str) -> None:
        self.output_stream.write(f"//label command {self.cur_func}${label}\n")
        self.output_stream.write(f"({self.cur_func}${label})\n")

    def initializebootstrap(self):
        self.output_stream.write("@256\nD=A\n@SP\nM=D\n")
        self.write_call('Sys.init', 0)

    def write_goto(self, label: str) -> None:
        self.output_stream.write(f"//goto the {self.cur_func}${label}\n"
                                 f"@{self.cur_func}${label}\n"
                                 "0;JMP\n")

    def write_if(self, label: str) -> None:
        self.output_stream.write(f"//if command {self.cur_func}${label}\n")
        self.output_stream.write("@SP\nAM=M-1\nD=M\n"
                                 f"@{self.cur_func}${label}\n"
                                 "D;JNE\n")

    def write_function(self, function_name: str, n_vars: int) -> None:
        self.cur_func = function_name
        self.lab = 0
        self.output_stream.write(f"//func command {self.cur_func}\n")
        self.output_stream.write(f"({self.cur_func})\n")
        for _ in range(int(n_vars)):
            self.output_stream.write("@SP\nA=M\nM=0\n"
                                     "@R13\nM=D\n"
                                     "@SP\nM=M+1\n")
        self.output_stream.write("@R13\nM=0\n")



    def write_call(self, function_name: str, n_args: int) -> None:
        label = f"ret.{self.lab}"
        self.output_stream.write(f"//call command {self.cur_func}${label}\n")
        self.output_stream.write(f"@{self.cur_func}${label}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n")
        for i in ['LCL', 'ARG', 'THIS', 'THAT']:
            self.output_stream.write(f"@{i}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n")
        cur = int(n_args) + 5
        self.output_stream.write(f"@{cur}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n")
        self.output_stream.write("@SP\nD=M\n@LCL\nM=D\n")
        self.output_stream.write(f"@{function_name}\n0;JMP\n")
        self.write_label(label)
        self.lab += 1

    def help(self, num: int, where: str):
        self.output_stream.write(f"@{num}\nD=A\n@R15\nD=M-D\nA=D\nD=M\n@{where}\nM=D\n")

    def write_return(self) -> None:
        self.output_stream.write("//return command \n")
        self.output_stream.write("@LCL\nD=M\n@R15\nM=D\n")
        self.help(5, 'R14')
        self.output_stream.write("@SP\nD=A\n@ARG\nD=M+D\n@R13\nM=D\n"
                                 "@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n@R13\nM=0\n")
        self.output_stream.write("@ARG\nD=M\nD=D+1\n@SP\nM=D\n")
        self.help(1, 'THAT')
        self.help(2, 'THIS')
        self.help(3, 'ARG')
        self.help(4, 'LCL')
        self.output_stream.write(f"@R14\nA=M\n0;JMP\n")

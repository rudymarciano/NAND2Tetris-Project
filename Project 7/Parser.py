class Parser:
    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            self.lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('//')]
        self.current_command = None
        self.index = -1

    def has_more_commands(self):
        return self.index < len(self.lines) - 1


    # This method is used to advance the index and set the current command
    def advance(self):
        self.index += 1
        self.current_command = self.lines[self.index]

    # This method is used to determine the type of the current command
    def command_type(self):
        if self.current_command.startswith("push"):
            return "C_PUSH"
        elif self.current_command.startswith("pop"):
            return "C_POP"
        elif self.current_command in {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}:
            return "C_ARITHMETIC"
        else:
            raise ValueError(f"Unknown Command : {self.current_command}")

   # These methods are used to get the arguments of the current command
    def arg1(self):
        if self.command_type() == "C_ARITHMETIC": # If the command is an arithmetic command, return the command itself
            return self.current_command
        return self.current_command.split()[1] # Otherwise, return the first argument

    def arg2(self):
        if self.command_type() in {"C_PUSH", "C_POP"}: # If the command is a push or pop command, return the index
            return int(self.current_command.split()[2])
        return None # Otherwise, return None

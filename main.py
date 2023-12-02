import sys
from typing import Any

class CleanBug:
    def __init__(self, args: list[str]):
        self.args = args
        self.input = self.get_input_from_file()
        self.is_debug_mode = self.get_is_debug_mode()
        self.output_file_name = self.get_output_file_name()
        self.output = ''

        self.flag = False
        self.debug_flag = False
        self.build_flag = False

    def __call__(self):
        self.clean()
        self.write_output()
        
    def get_is_debug_mode(self):
        is_debug_mode = '--debug' in self.args
        
        try:
            self.args.remove('--build')
        except ValueError:
            pass

        try:
            self.args.remove('--debug')
        except ValueError:
            pass
    
        return is_debug_mode
    
    def get_output_file_name(self):
        output_file_name = self.args[2] if len(self.args) > 2 else self.args[1]
        return output_file_name
    
    def check_flags(self, stripped_line: str):
        if stripped_line.startswith('!DEBUG>') and not self.build_flag:
            self.debug_flag = True
            return True
        if stripped_line.startswith('!DEBUG<') and not self.build_flag:
            self.debug_flag = False
            return True
        if stripped_line.startswith('!BUILD>') and not self.debug_flag:
            self.build_flag = True
            return True
        if stripped_line.startswith('!BUILD<') and not self.debug_flag:
            self.build_flag = False
            return True
        return False
    
    def should_debug(self, stripped_prev_line: str):
        return stripped_prev_line.startswith('!DEBUG') and not stripped_prev_line.startswith('!DEBUG<') or self.debug_flag
    
    def should_build(self, stripped_prev_line: str):
        return stripped_prev_line.startswith('!BUILD') and not stripped_prev_line.startswith('!BUILD<') or self.build_flag

    def clean(self):
        prev_line = ''
        for line in self.input.split('\n'):
            if self.flag:
                self.output += '\n'
            else:
                self.flag = True

            stripped_line = self.strip_line(line)
            if self.check_flags(stripped_line):
                self.output += line
                continue

            stripped_prev_line = self.strip_line(prev_line)
            if self.should_debug(stripped_prev_line):
                if self.is_debug_mode:
                    self.output += self.uncomment(line)
                elif line.lstrip()[0] != '#':
                    self.output += self.comment(line)
                else:
                    self.output += line
            elif self.should_build(stripped_prev_line):
                if not self.is_debug_mode:
                    self.output += self.uncomment(line)
                elif line.lstrip()[0] != '#':
                    self.output += self.comment(line)
                else:
                    self.output += line
            else:
                self.output += line
            prev_line = line
    
    def write_output(self):
        output_file = open(self.output_file_name, 'w')
        output_file.write(self.output)
        output_file.close()

    @staticmethod
    def strip_line(line: str):
        return line.strip('#').strip()
    
    def get_input_from_file(self):
        try:
            input_file = open(self.args[1], 'r')
        except FileNotFoundError:
            print("File not found: " + self.args[1])
            exit(1)
        
        input = input_file.read()
        input_file.close()
        
        return input
    
    @staticmethod
    def comment(line: str):
        i = 0
        try:
            while line[i].isspace():
                i += 1
        except IndexError:
            return line
        
        return line[:i] + '# ' + line[i:]

    @staticmethod
    def uncomment(line: str):
        try:
            return line[:line.index('#')] + line[line.index('#')+1:].lstrip()
        except ValueError:
            return line

if __name__ == '__main__':
    args = sys.argv

    if '--build' in args and '--debug' in args:
        print("Usage: cleanbug <file> [output_file] [--build|--debug]")
        print("  --build: Clean the file and comment out all debug statements. Uncomment all the build statements")
        print("  --debug: Comment all the build statements. Uncomment all the debug statements")
        exit(1)

    if '-h' in args or '--help' in args:
        print("Usage: cleanbug <file> [output_file] [--build|--debug]")
        print("\t--build: Clean the file and comment out all debug statements. Uncomment all the build statements")
        print("\t--debug: Comment all the build statements. Uncomment all the debug statements")
        print("\t-h, --help: Display this help message")
        print("\tif output_file is not specified, the file will be overwritten")
        exit(0)

    if len(args) < 2:
        print("Usage: cleanbug <file> [output_file] [--build|--debug]")
        print("  --build: Clean the file and comment out all debug statements. Uncomment all the build statements")
        print("  --debug: Comment all the build statements. Uncomment all the debug statements")
        exit(1)

    clean_bug = CleanBug(args)
    clean_bug()
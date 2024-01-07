class CleanBug:
    def __init__(self, curr_flag_mode, all_flags, inline_comment = None, multi_comment_start = None, multi_comment_end = None):
        self.curr_flag_mode = curr_flag_mode
        self.all_flags = all_flags
        self.inline_comment = inline_comment
        self.multi_comment_start = multi_comment_start
        self.multi_comment_end = multi_comment_end
    
    def clean(self, text: str) -> str:
        output = ""
        lines = text.split('\n')
        index = 0
        while index < len(lines):
            output += f'{lines[index]}\n'
            if not self.is_flag_line(lines[index]):
                index += 1
                continue

            flags = self.get_flags_from_flag_line(lines[index])
            index += 1

            if index == len(lines):
                break
            
            if self.curr_flag_mode in flags:
                output += f'{self.uncomment(lines[index])}\n'
                index += 1
                if flags[0] != '>':
                    continue
                while index < len(lines):
                    if self.is_flag_line(lines[index]):
                        curr_flags = self.get_flags_from_flag_line(lines[index])
                        if self.curr_flag_mode in curr_flags and curr_flags[0] == '<':
                            output += f'{lines[index]}\n'
                            index += 1
                            break
                        output += f'{lines[index]}\n'
                        continue
                    output += f'{self.uncomment(lines[index])}\n'
                    index += 1
            else:
                output += f'{self.comment(lines[index])}\n'
                index += 1
                if flags[0] != '>':
                    continue
                while index < len(lines):
                    if self.is_flag_line(lines[index]):
                        curr_flags = self.get_flags_from_flag_line(lines[index])
                        if curr_flags[0] == '<':
                            output += f'{lines[index]}\n'
                            index += 1
                            break
                        output += f'{lines[index]}\n'
                        continue
                    output += f'{self.comment(lines[index])}\n'
                    index += 1

        return output[:-1] # Remove last newline

    def is_comment_line(self, text: str) -> bool:
        return (self.inline_comment and text.strip().startswith(self.inline_comment)) or (self.multi_comment_start and text.strip().startswith(self.multi_comment_start))

    def is_flag_line(self, text: str) -> bool:
        if not self.is_comment_line(text):
            return False
        try:
            self.get_flags_from_flag_line(text)
            return True
        except AssertionError:
            return False

    def get_flags_from_flag_line(self, text: str) -> list[str]:
        text = self.strip_clean(text)
        flags = [flag for flag in text.split('.') if len(flag.strip()) > 0]

        for flag in flags:
            assert flag == '<' or flag == '>' or flag in self.all_flags, f'Non-existent flag {flag} found in flag line'
        
        return flags
    
    def strip_clean(self, text: str) -> str:
        text = text.strip()
        if self.inline_comment is not None:
            while text.startswith(self.inline_comment):
                text = text[len(self.inline_comment):]
                text = text.strip()

        if self.multi_comment_start is not None:
            while text.startswith(self.multi_comment_start):
                text = text[len(self.multi_comment_start):]
                text = text.strip()
        
        if self.multi_comment_end is not None:
            while text.endswith(self.multi_comment_end):
                text = text[:text.index(self.multi_comment_end)]
                text = text.strip()
        return text

    def uncomment(self, text: str) -> str:
        IGNORE_COMMENT_LINE = '!!'
        
        def get_stripped_text(text: str, comment: str) -> str:
            return text[text.index(comment) + len(comment):].strip()
        
        if self.strip_clean(text).startswith(IGNORE_COMMENT_LINE):
            return text
        
        if self.inline_comment is not None and text.strip().startswith(self.inline_comment):
            stripped = get_stripped_text(text, self.inline_comment)
            # if stripped.startswith(IGNORE_COMMENT_LINE):
            #     return text
            white_space = text[:text.index(self.inline_comment)]
            return white_space + stripped
        
        if self.multi_comment_start is not None and text.strip().startswith(self.multi_comment_start):
            stripped = get_stripped_text(text, self.multi_comment_start)
            # if stripped.startswith(IGNORE_COMMENT_LINE):
            #     return text
            white_space = text[:text.index(self.multi_comment_start)]
            text = white_space + stripped
            
        if self.multi_comment_end is not None and text.strip().endswith(self.multi_comment_end):
            if self.multi_comment_start is not None and self.multi_comment_start in text:   # ignore multi-line comment that is part of single line
                return text
            text = text[:text.rindex(self.multi_comment_end)]
        
        return text
    
    def comment(self, text: str) -> str:
        if self.is_comment_line(text):
            return text
        
        white_space = ''    # Preserving indentation
        for c in text:
            if c.isspace():
                white_space += c
            else:
                break

        if self.inline_comment is not None:
            return f'{white_space}{self.inline_comment} {text.strip()}'
        
        if self.multi_comment_start is not None and self.multi_comment_end is not None:
            return f'{white_space}{self.multi_comment_start} {text.strip()} {self.multi_comment_end}'
        
        return text
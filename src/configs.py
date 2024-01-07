def get_flags(config_file: str) -> list[str]:
    flags = []
    with open(config_file) as f:
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith('FLAGS'):
                flags.extend(line.strip().split('=')[1].strip().split(' '))
    return list(set(flags))

def get_comments(config_file: str) -> tuple[str | None, str |  None, str | None]:
    inline = None
    multi_comment_start = None
    multi_comment_end = None

    with open(config_file) as f:
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith('INLINE_COMMENT'):
                inline = line.strip().split('=')[1].strip()
            elif line.strip().startswith('MULTI_COMMENT_START'):
                multi_comment_start = line.strip().split('=')[1].strip()
            elif line.strip().startswith('MULTI_COMMENT_END'):
                multi_comment_end = line.strip().split('=')[1].strip()
            elif line.strip().startswith('MULTI_COMMENT'):
                try:
                    multi_comment_start, multi_comment_end = line.strip().split('=')[1].strip().split()
                except ValueError:
                    raise ValueError("MULTI_COMMENT must have two arguments, the start and end of the multi-line comment")

    if inline is not None and len(inline) == 0:
        inline = None
    if multi_comment_start is not None and len(multi_comment_start) == 0:
        multi_comment_start = None
    if multi_comment_end  is not None and len(multi_comment_end) == 0:
        multi_comment_end = None

    return inline, multi_comment_start, multi_comment_end

if __name__ == "__main__":
    try:
        print(get_comments('cleanbug.config'))
    except ValueError as e:
        print(e)
        exit(1)
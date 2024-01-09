import sys
from src.cleanbug import CleanBug
from src.configs import get_comments, get_flags

def parse_args(args: list[str]):
    if '--help' in args or '-h' in args:
        print("Usage: cleanbug <file_name> [<output_file_name>] --mode <flag> --config <config_file>")
        print("Default Flags: DEV, BUILD")
        print("Default Flag Mode: DEV (or first of the user-defined flags)")
        print("Default Comments: '#'")
        exit(0)

    try:
        inline, multi_comment_start, multi_comment_end = get_comments(args[args.index('--config') + 1])
    except (ValueError, IndexError):
        inline, multi_comment_start, multi_comment_end = '#', None, None
    
    try:
        flags = get_flags(args[args.index('--config') + 1])
        assert len(flags) > 0
    except (ValueError, IndexError, AssertionError):
        flags = ['DEV', 'BUILD']
    
    try:
        config_index = args.index('--config')
        args.pop(config_index)
        args.pop(config_index)
    except (ValueError, IndexError):
        pass

    try:
        mode = args[args.index('--mode')+1]
        assert mode in flags
    except AssertionError:
        raise ValueError(f"Invalid mode {mode}, must be one of {flags}")
    except (ValueError, IndexError):
        mode = flags[0]

    try:
        mode_index = args.index('--mode')
        args.pop(mode_index)
        args.pop(mode_index)
    except (ValueError, IndexError):
        pass
    
    cleanbug = CleanBug(mode, flags, inline_comment=inline, multi_comment_start=multi_comment_start, multi_comment_end=multi_comment_end)

    assert len(args) > 1, "Must provide a file name to clean."

    return cleanbug, args[1]

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 n_main.py <file_name> [<output_file_name>] --mode <flag> --config <config_file>")
        exit(1)

    cleanbug, file_name = parse_args(sys.argv)

    with open(file_name) as f:
        text = f.read()
        cleaned = cleanbug.clean(text)
        if len(sys.argv) > 2 and not sys.argv[2].startswith('--'):
            output_file_name = sys.argv[2]
        else:
            output_file_name = sys.argv[1]
        with open(output_file_name, 'w') as f:
            try:
                f.write(cleaned)
            except Exception as e:
                print(f'Error:{e}')
                f.write(text)
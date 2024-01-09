# cleanbug

CLI tool for managing and easily converting the code into comments and vice versa. Define multiple modes and execute the command to swap between them. Comments all flags that are not the current mode and uncomment the flag that is the current mode.

## Prerequisites

- Python 3.6 or higher

## Installation

```bash
pip install cleanbug
```

## Usage

```bash
cleanbug <file_name> [<output_file_name>] --mode <flag> --config <config_file>
```

## Config File

Can contain the parameters FLAGS, INLINE_COMMENT, MULTILINE_COMMENT. The starting and ending symbols of MULTILINE_COMMENT should be separated by spaces.
Eg: 
```bash
FLAGS = DEBUG DEV PROD
INLINE_COMMENT = //
MULTI_COMMENT = /* */
```

```bash
FLAGS = DEBUG DEV PROD BUILD
INLINE_COMMENT = #
```

MULTILINE_COMMENT can also be broken into MULTILINE_COMMENT_START and MULTILINE_COMMENT_END.

## Input File

The flags should be written in the following format:
```bash
.<flag_name_1>[.<flag_name_2>...<flag_name_n>]
```
with each flag separated by a dot. The flags must be written in a single line, preceded and succeeded only by the comment symbol and whitespace.

### Multiple Lines

To mark multiple lines under a single flag line, use a `>` sybmol as the first flag in the line. The end of the lines marked under those flags is marked by another flag line using the `<` symbol. The flag lines between the `>` and `<` symbols are marked under the same flag.

### Example

**Original Code:**
```bash
void main() {
    // .DEV
    printf("Hello World!\n");
    // >.PROD
    printf("Hello There, World!\n");
    printf("Nice to meet you! \n");
    // <.PROD
    // .PROD.DEV
    printf("I'm Good!\n");
    printf("Nice to meet you! \n");
}
```
**FLAG: DEV**
>cleanbug example/test.c --config example/cleanbug.config --mode DEV
```bash
void main() {
    // .DEV
    printf("Hello World!\n");
    // >.PROD
    /* printf("Hello There, World!\n");
    printf("Nice to meet you! \n"); */
    // <.PROD
    // .PROD.DEV
    printf("I'm Good!\n");
    printf("Nice to meet you! \n");
}
```
**FLAG: PROD**
>cleanbug example/test.c --config example/cleanbug.config --mode PROD
```bash
void main() {
    // .DEV
    // printf("Hello World!\n");
    // >.PROD
    printf("Hello There, World!\n");
    printf("Nice to meet you! \n");
    // <.PROD
    // .PROD.DEV
    printf("I'm Good!\n");
    printf("Nice to meet you! \n");
}
```
**FLAG: DEBUG**
>cleanbug example/test.c --config example/cleanbug.config --mode DEBUG
```bash
void main() {
    // .DEV
    // printf("Hello World!\n");
    // >.PROD
    /* printf("Hello There, World!\n");
    printf("Nice to meet you! \n"); */
    // <.PROD
    // .PROD.DEV
    // printf("I'm Good!\n");
    printf("Nice to meet you! \n");
}
```

### Prevent Conversion from Comments to Code

The conversion from comment to code can be prevented by inserting a `!!` symbol after the comment symbol (separated only by whitespaces).
Eg:
```bash
# !! NOTE: This is a note.
```
This allows for comment lines within the code to be ignored by the tool.

## Output File

If the output file is not specified, the input file is overwritten with the converted code. If the output file is specified, the converted code is written to the output file.
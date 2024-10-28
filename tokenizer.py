import subprocess
import os
import tempfile

# Define TokenType to be used in GUI and for token classification
class TokenType:
    KEYWORD = "KEYWORD"
    COMMAND = "COMMAND"
    OPERATOR = "OPERATOR"
    DELIMITER = "DELIMITER"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    STRING_LITERAL = "STRING_LITERAL"
    OPTION = "OPTION"
    ARGUMENT = "ARGUMENT"
    ERROR = "ERROR"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    COMMENT = "COMMENT"
    AND = "AND"
    OR = "OR"
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    LESS_OR_EQUAL = "LESS_OR_EQUAL"
    GREATER_OR_EQUAL = "GREATER_OR_EQUAL"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASSIGN = "ASSIGN"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    NOT = "NOT"
    COLON = "COLON"
    SEPARATOR = "SEPARATOR"
    PIPE = "PIPE"
    APPEND_REDIRECT = "APPEND_REDIRECT"
    VARIABLE = "VARIABLE"

# Token class to store token information
class Token:
    def __init__(self, token_type, value, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"| {self.line:<4} | {self.column:<4} | {self.token_type:<20} | {self.value:<20} |"

# Function to run the LEX tokenizer and capture its output
def run_lex_tokenizer(input_file, verbose=False):
    try:
        # Compile the LEX file if not already compiled
        if not os.path.exists('./a.out'):
            if verbose:
                print("Compiling LEX file...")
            subprocess.run(['flex', 'tokenizer.lex'])
            subprocess.run(['gcc', 'lex.yy.c', '-o', 'a.out'])
            if verbose:
                print("Compilation complete.")

        if verbose:
            print(f"Processing input file: {input_file}")
            
        process = subprocess.Popen(['./a.out', input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr:
            print('Error:', stderr.decode())
        if verbose:
            print("Tokenization complete.")
        return stdout.decode().splitlines()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to parse the LEX output into Token objects
import re

def parse_tokens(lex_output, verbose=False):
    tokens = []
    if verbose:
        print("\nParsing tokens...")
        print("-" * 60)
        print(f"{'Line':<4} | {'Col':<4} | {'Token Type':<20} | {'Value':<20} |")
        print("-" * 60)
    
    for line in lex_output:
        line = line.strip()
        if not line or line.startswith("Starting") or line.startswith("----------------") or line.startswith("Parsing Complete"):
            continue
        match = re.match(r"\[Line (\d+), Column (\d+)\] (\w+): (.+)", line)
        if match:
            line_num = int(match.group(1))
            column_num = int(match.group(2))
            token_type = match.group(3)
            value = match.group(4)
            token = Token(token_type.upper(), value, line_num, column_num)
            tokens.append(token)
            if verbose:
                print(token)
        else:
            print(f"Unrecognized line format: {line}")
    
    if verbose:
        print("-" * 60)
    return tokens

# Main function to process the input and generate the detailed token breakdown
def tokenize(input_file, verbose=False):
    if verbose:
        print("\nStarting tokenization process...")
        print(f"Input file: {input_file}")
        
    lex_output = run_lex_tokenizer(input_file, verbose)
    tokens = parse_tokens(lex_output, verbose)

    total_tokens = len(tokens)
    token_count = {}
    error_count = 0

    for token in tokens:
        token_type = token.token_type
        token_count[token_type] = token_count.get(token_type, 0) + 1
        if token_type == TokenType.ERROR:
            error_count += 1

    error_percentage = (error_count / total_tokens) * 100 if total_tokens > 0 else 0
    whitespace_count = token_count.get(TokenType.WHITESPACE, 0)
    comment_count = token_count.get(TokenType.COMMENT, 0)

    if verbose:
        print("\nTokenization Statistics:")
        print(f"Total tokens: {total_tokens}")
        print(f"Error percentage: {error_percentage:.2f}%")
        print("\nToken type distribution:")
        for token_type, count in token_count.items():
            print(f"{token_type:<20}: {count:>5} ({(count/total_tokens*100):.1f}%)")

    return tokens, total_tokens, token_count, error_percentage, whitespace_count, comment_count

# Example usage
if __name__ == "__main__":
    input_file = 'INPUT.txt'
    tokens, total_tokens, token_count, error_percentage, whitespace_count, comment_count = tokenize(input_file, verbose=True)

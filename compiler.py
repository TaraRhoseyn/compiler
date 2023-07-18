import re


# TOKEN TYPES
# keywords:
TOKEN_IF = "IF"
TOKEN_ELSE = "ELSE"
TOKEN_ELIF = "ELIF"
TOKEN_WHILE = "WHILE"
TOKEN_PRINT = "PRINT"
TOKEN_INT_INIT = "INT"
# data types:
TOKEN_NUMBER = "NUMBER"
TOKEN_LETTERS = "LETTERS"
TOKEN_VARIABLE_NAME = "VARIABLE_NAME"
# comments:
TOKEN_COMMENT = "COMMENT"
TOKEN_MULTI_COMMENT = "MULTI_COMMENT"
# handling invalid inputs:
TOKEN_INVALID = "INVALID"
TOKEN_QUOTATION = "QUOTE"
# arhithmetic operators:
TOKEN_ADDITION = "ADD"
TOKEN_SUBTRACT = "SUBTRACT"
TOKEN_DIVIDE = "DIVIDE"
TOKEN_MULTIPLY = "MULTIPLY"
# punctuation:
TOKEN_LEFT_PARENT = "LEFT_PARENTHESIS"
TOKEN_RIGHT_PARENT = "RIGHT_PARENTHESIS"
TOKEN_LEFT_BRACKET = "LEFT_BRACKET"
TOKEN_RIGHT_BRACKET = "RIGHT_BRACKET"
TOKEN_SEMI_COLON = "SEMI_COLON"
TOKEN_MORE_THAN = "MORE_THAN"
TOKEN_LESS_THAN = "LESS_THAN"
TOKEN_MORE_THAN_OR_EQUALS = "MORE_THAN_OR_EQUALS"
TOKEN_LESS_THAN_OR_EQUALS = "LESS_THAN_OR_EQUALS"
TOKEN_NOT_EQUALS = "NOT_EQUALS"
TOKEN_EQUALS = "EQUALS"
TOKEN_ASSIGN = "ASSIGN"
TOKEN_INCREMENT = "INCREMENT"
TOKEN_COMMA = "COMMA"

# token patterns

TOKEN_PATTERNS = [
    # comments:
    (r"//.*", TOKEN_COMMENT),  # single line comment, will be skipped in tokenize_string()
    (r"/\*.*?\*/", TOKEN_MULTI_COMMENT),  # multi-line comment, will be skipped in tokenize_string()
    # whitesapce:
    (r"\s+", None),  # used for skipping whitespace in tokenize_string()
    # keywords:
    (r"if", TOKEN_IF),
    (r"else", TOKEN_ELSE),
    (r"printf\('.*?'\)", TOKEN_PRINT),
    (r"elif", TOKEN_ELIF),
    (r"while", TOKEN_WHILE),
    (r"int", TOKEN_INT_INIT),
    # data types:
    (r"[a-zA-Z]+", TOKEN_LETTERS), 
    (r"[a-zA-Z_][a-zA-Z_0-9]*", TOKEN_VARIABLE_NAME), 
    (r"\d+", TOKEN_NUMBER),
    # increment for while loop:
    (r"\+\+", TOKEN_INCREMENT),
    # arthimetic operators:
    (r"\+", TOKEN_ADDITION),
    (r"\-", TOKEN_SUBTRACT),
    (r"\/", TOKEN_DIVIDE),
    (r"\*", TOKEN_MULTIPLY),
    # punctuation:
    (r"{", TOKEN_LEFT_PARENT),
    (r"}", TOKEN_RIGHT_PARENT),
    (r"\(", TOKEN_LEFT_BRACKET),
    (r"\)", TOKEN_RIGHT_BRACKET),
    (r";", TOKEN_SEMI_COLON),
    (r"'", TOKEN_QUOTATION),
    (r",", TOKEN_COMMA),
    # relative operators:
    (r">=", TOKEN_MORE_THAN_OR_EQUALS),
    (r"<=", TOKEN_LESS_THAN_OR_EQUALS),
    (r">", TOKEN_MORE_THAN),
    (r"<", TOKEN_LESS_THAN),
    (r"==", TOKEN_EQUALS),
    (r"!=", TOKEN_NOT_EQUALS),
    (r"=", TOKEN_ASSIGN),
    # handling invalid inputs (everything that isn't defined):
    (r"\S+", TOKEN_INVALID),
]


def tokenize_string(input_string):
    """
    Creates a tuple of tokens and lexemes based on an input string.

    Args:
      input_string (str): A string variable that represents a user's
      source code input to be compiled.

    Returns:
      tokens (tuple): Contains tokens and lexemes.

    Raises:
      ValueError: if the input string contains invalid tokens.
    """
    position = 0
    tokens = []
    previous_token = None
    # loops through input string chars:
    while position < len(input_string):
        match_output = None
        match_len = 0
        for pattern, token_type in TOKEN_PATTERNS:
            regex = re.compile(pattern)
            match_output = regex.match(input_string, position)
            if match_output and token_type:  # skips whitespaces
                match_len = match_output.end() - match_output.start()
                if token_type in [TOKEN_INVALID]:
                    # raises error if any tokens are invalid
                    invalid_token = input_string[position : position + match_len]
                    raise ValueError(
                        f"ERROR - The input contains the following invalid tokens: '{invalid_token}'"
                    )
                token_value = match_output.group()
                # assigning strings as variable name if preceeded by an variable initialisation (INT token):
                if previous_token == TOKEN_INT_INIT:
                    token_type = TOKEN_VARIABLE_NAME
                # only captures tokens that are NOT comments:
                if token_type not in [TOKEN_COMMENT, TOKEN_MULTI_COMMENT]:
                    tokens.append((token_type, token_value))
                # captures previous increment for the purpose of checking for variable names
                previous_token = token_type
                break
        if match_len != 0:
            position += match_len
        else:
            position += 1
    return tokens


def print_tokens(tokens):
    """
    Helper function that prints each token in the passed tuple.

    Args:
      tokens (tuple): A tuple containing tokens and lexemes.
    """
    for token in tokens:
        print(token)


def parse_tokens(tokens):
    '''
    Checks that the sequence of tokens follows the defined LL(1) grammar. 

    Creates a parser table out of non-terminals and terminals,
    loops through tokens and if the top of the stack is a non-terminal
    the function will go to the parsing table to find it's production rule. 
    If the production rule is matched with the input - stack will be extended.
    If the top is a terminal the token is consumed and the function moves to the next.
    
    Returns:
        parser_passed (bool): Signifies whether the tokenized input has passed the parser successfully. 
    Raises:
        SyntaxError: raises if there's a mismatch between the top of the stack and the current token
        SyntaxError: raises if there's a mismatched production rule
    '''
    token_index = 0
    stack = ["<program>"] # starting point of stack
    # The rows of the parser table:
    non_terminals = [
        "<program>",
        "<if_statement>",
        "<condition>",
        "<letters>",
        "<variable_name>",
        "<rel_op>",
        "<exe_block>",
        "<end_if>",
        "<print_statement>",
        "<int_variable>",
        "<number>",
        "<arithemtic_exp>",
        "<arithmetic_op>",
        "<while_loop>",
    ]
    # The cols of the parser table:
    terminals = [
        "IF",
        "LEFT_BRACKET",
        "RIGHT_BRACKET",
        "LEFT_PARENTHESIS",
        "RIGHT_PARENTHESIS",
        "SEMI_COLON",
        "LETTERS",
        "VARIABLE_NAME",
        "MORE_THAN",
        "LESS_THAN",
        "ELSE",
        "ELIF",
        "PRINT",
        "ASSIGN",
        "INT",
        "WHILE",
        "NUMBER",
        "ADD",
        "SUBTRACT",
        "MULTIPLY",
        "DIVIDE",
        "INCREMENT",
        "LESS_THAN_OR_EQUALS",
        "MORE_THAN_OR_EQUALS",
        "NOT_EQUALS",
        "EQUALS"
    ]
    column_indices = {terminal: i for i, terminal in enumerate(terminals)}
    row_indices = {non_terminal: i for i, non_terminal in enumerate(non_terminals)}
    # Parsing table with production rules
    parsing_table = [
        [6, None, None, None, None, None, None, None, None, None, None, None, 17, None, 18, 26, 21, None, None, None, None, None, None, None, None, None],
        [6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 19, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, 8, None, None, None, None, None, None, None, None, None, 7, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, 9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, 10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, 11, 12, None, None, None, None, None, None, None, None, None, None, None, None, 28, 29, 30, 31],
        [6, None, None, None, None, None, None, None, None, None, None, None, 17, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, 27, None, None, None, None, 15, 16, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, 17, None, None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, 18, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 19, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 21, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 22, 23, 24, 25, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 26, None, None, None, None, None, None, None, None, None, None],
    ]
    while stack:
        top = stack[-1]
        current_token = tokens[token_index][0]
        # cross-referencing with production rules:
        if top in non_terminals:
            row_index = row_indices[top]
            column_index = column_indices[current_token]
            production_rule = parsing_table[row_index][column_index]
            if production_rule is None:
                raise SyntaxError('Parsing error: Unexpected token {}'.format(current_token))
            stack.pop() 
            if production_rule == 6:
                stack.extend( # if statement - allows you to end with a ; or continue with else/elif clauses
                    [
                        "<end_if>",
                        "RIGHT_PARENTHESIS",
                        "<exe_block>",
                        "LEFT_PARENTHESIS",
                        "RIGHT_BRACKET",
                        "<condition>",
                        "LEFT_BRACKET",
                        "IF",
                    ]
                )
            elif production_rule == 7: # <condition> rule (numbers)
                stack.extend(["NUMBER", "<rel_op>", "NUMBER"])
            elif production_rule == 8: # <condition> rule (letters)
                stack.extend(["LETTERS", "<rel_op>", "LETTERS"])
            elif production_rule == 9:
                stack.extend(["LETTERS"])
            elif production_rule == 10:
                stack.extend(["VARIABLE_NAME"])
            elif production_rule == 11:
                stack.extend(["MORE_THAN"])
            elif production_rule == 12:
                stack.extend(["LESS_THAN"])
            elif production_rule == 15:  # <end_if> (else)
                stack.extend(
                    [
                        "SEMI_COLON",
                        "RIGHT_PARENTHESIS",
                        "<exe_block>",
                        "LEFT_PARENTHESIS",
                        "ELSE",
                    ]
                )
            elif production_rule == 16:  # end_if (elif)
                stack.extend(
                    [
                        "<end_if>",
                        "RIGHT_PARENTHESIS",
                        "<exe_block>",
                        "LEFT_PARENTHESIS",
                        "RIGHT_BRACKET",
                        "<condition>",
                        "LEFT_BRACKET",
                        "ELIF",
                    ]
                )
                
            elif production_rule == 17:
                """
                Print statement
                Originally I had this rule seperating out all of the elements of the print statement, but it was tricky
                allowing more than one word at a time within the ('') of the statement. Therefore, I created a seperate
                token that captures the whole print statement so that regex would allow the statement to contain
                all characters and any number of words.
                """
                stack.extend(["SEMI_COLON", "PRINT"])  # print statement
            elif production_rule == 18:
                stack.extend( # int variable declaration
                    ["SEMI_COLON", "<number>", "ASSIGN", "<variable_name>", "INT"]
                )
            elif production_rule == 19:
                stack.extend(["NUMBER"])
            elif production_rule == 21:  # arithmetic expressions
                stack.extend(["SEMI_COLON", "NUMBER", "<arithmetic_op>", "NUMBER"])
            elif production_rule == 22:
                stack.extend(["ADD"])
            elif production_rule == 23:
                stack.extend(["SUBTRACT"])
            elif production_rule == 24:
                stack.extend(["MULTIPLY"])
            elif production_rule == 25:
                stack.extend(["DIVIDE"])
            elif production_rule == 26:  # while loop
                stack.extend(
                    [
                        "SEMI_COLON",
                        "RIGHT_PARENTHESIS",
                        "INCREMENT",
                        "LETTERS",
                        "<exe_block>",
                        "LEFT_PARENTHESIS",
                        "RIGHT_BRACKET",
                        "NUMBER",
                        "<rel_op>",
                        "LETTERS",
                        "LEFT_BRACKET",
                        "WHILE",
                    ]
                )
            elif production_rule == 27:
                stack.extend( # end_if (ends)
                    ["SEMI_COLON"]
                )
            elif production_rule == 28:
                stack.extend(["LESS_THAN_OR_EQUALS"])
            elif production_rule == 29:
                stack.extend(["MORE_THAN_OR_EQUALS"])
            elif production_rule == 30:
                stack.extend(["NOT_EQUALS"])
            elif production_rule == 31:
                stack.extend(["EQUALS"])
            else:
                raise SyntaxError(
                    "PARSER ERROR - Unexpected production rule {}".format(
                        production_rule
                    )
                )
        elif top == current_token:
            # Terminal symbol matches the current token, consume it and move to the next token
            stack.pop()
            token_index += 1
            if token_index >= len(tokens):
                break
        else:
            raise SyntaxError(
                "PARSER ERROR - Unexpected token {}".format(current_token)
            )
    if token_index >= len(tokens) and not stack:
        print("\nParser: Successful\n")
        parser_passed = True
        return parser_passed
    else:
        parser_passed = False
        return parser_passed


def semantic_analyzer(tokens):
    '''
    Checks whether the lexeme of the VARIABLE_NAME token contains any integers. 

    Returns:
        semantic_passed (bool): Signifies the input has passed the analyser.
    '''
    for token in tokens:
        if token[0] == "VARIABLE_NAME":
            if any(char.isdigit() for char in str(token[1])):
                semantic_passed = False
                raise Exception("ERROR - Variable name cannot contain any numbers.")
        else:
            semantic_passed = True
    return semantic_passed


def generate_code(tokens):
    '''
    Loops through the tokens tuple and consumes the token values (lexemes) when matches are found.
    It then prints these lexemes to the console. 

    I chose to use a for loop for this function over the while loop we went over in class as it removes the need to manually
    move the index and only captures the specific tokens it's looking for, rathering than 'skipping'
    over those it doesn't need.

    Args:
        tokens (tuple): A tuple containing tokens and lexemes.
    Raises:
        Exception: raises if any part of the generator code fails. 
    '''


    def check_if_statement(str, pattern):
        '''
        Helper function to check whether there's a nested if
        statement within another if statement
        '''
        if str.count(pattern) >= 3:
            return True
        else:
            return False

    try:
        pseudo_code = []
        for t in tokens:
            # Appends most tokens to be printed:
            token = t[0]
            lexeme = t[1]
            if token == 'PRINT':
                print_value = lexeme.replace("printf('", "")
                print_value = print_value.replace("')", "")
                pseudo_code.append(f"\nPRINT {print_value} ")
            elif token == 'VARIABLE_NAME':
                pseudo_code.append(f"INT {lexeme} ")
            elif token == 'NUMBER':
                pseudo_code.append(f"{lexeme}")
            elif token == 'IF':
                pseudo_code.append("\nIF ")
            elif token == 'MORE_THAN':
                pseudo_code.append(f" IS MORE THAN ")
            elif token == 'LESS_THAN_OR_EQUALS':
                pseudo_code.append(f" IS LESS THAN OR EQUAL TO ")
            elif token == 'MORE_THAN_OR_EQUALS':
                pseudo_code.append(f" IS MORE THAN OR EQUAL TO ")
            elif token == 'EQUALS':
                pseudo_code.append(f" IS EQUAL TO ")
            elif token == 'NOT_EQUALS':
                pseudo_code.append(f" IS NOT EQUAL TO ")
            elif token == 'LESS_THAN':
                pseudo_code.append(f" IS LESS THAN ")
            elif token == 'LETTERS':
                pseudo_code.append(f"{lexeme}")
            elif token == 'ELIF':
                pseudo_code.append(f"\nELSE IF ")
            elif token == 'INCREMENT':
                pseudo_code.append(f"++ ")
            elif token == 'ELSE':
                pseudo_code.append(f"\nELSE")
            elif token == 'ADD':
                pseudo_code.append(f" ADDED TO ")
            elif token == 'SUBTRACT':
                pseudo_code.append(f" SUBTRACT ")
            elif token == 'DIVIDE':
                pseudo_code.append(f" DIVIDED BY ")
            elif token == 'MULTIPLY':
                pseudo_code.append(f" MULTIPLIED BY ")
            elif token == 'WHILE':
                pseudo_code.append(f"\nWHILE ")
        pseudo_code = [str(i) for i in pseudo_code]
        pseudo_code_str = ''.join(pseudo_code)
        '''
        The following code makes sure the pseudo code is properly
        indented depending on what type of expression is being passed
        '''
        if_str = "IF"
        while_str = "WHILE"
        end_if_str = "END IF"
        end_while_str = "END WHILE"
        nested_if_statements = False
        # Printing if statement:
        if if_str in pseudo_code_str:
            pseudo_code_str = pseudo_code_str.replace("PRINT", "   PRINT")
            pseudo_code_str = pseudo_code_str + "\n" + end_if_str
            nested_if_statements = check_if_statement(pseudo_code_str, if_str)
        '''
        Following code checks whether there is a nested if statement within an if statement and indented 
        the second if statement accordingly
        '''    
        if nested_if_statements:
            matches = re.finditer(if_str, pseudo_code_str)
            match_positions = [match.start() for match in matches]
            if len(match_positions) >= 2:
                second_index = match_positions[1]
            pseudo_code_str = pseudo_code_str[:second_index] + "   " + pseudo_code_str[second_index:]
            pseudo_code_str = pseudo_code_str.replace("PRINT", "   PRINT")
            pseudo_code_str = pseudo_code_str.replace("ELSE    IF", "ELSE IF")
        # Printing while loop:
        if while_str in pseudo_code_str:
            # Indenting:
            pseudo_code_str = pseudo_code_str.replace("IF", "   IF")
            pseudo_code_str = pseudo_code_str.replace("ELSE", "   ELSE")
            pseudo_code_str = pseudo_code_str.replace("PRINT", "  PRINT")
            pseudo_code_str = pseudo_code_str.replace("END    IF", "   END IF")
            pseudo_code_str = pseudo_code_str + "\n" + end_while_str
            # Making sure increment is on the same line within while loop:
            increment_pattern = r'(.)(?=\+\+)'
            match = re.search(increment_pattern, pseudo_code_str)
            if match:
                '''
                The increment pattern (eg 'x++') in a while loop was challenging to indent
                while not disrupting the indented pattern of an 'if' statement if
                present in the while loop. This logic executes when the increment 
                pattern is found and ensures the indents are in the correct location for that instance:
                '''
                pseudo_code_str = pseudo_code_str.replace("   END IF","")
                i = match.start(1)
                if if_str in pseudo_code_str:
                    pseudo_code_str = pseudo_code_str[:i] + "\n   END IF"+"\n  " + pseudo_code_str[i:] 
                else:
                    pseudo_code_str = pseudo_code_str[:i] + "\n  " + pseudo_code_str[i:] 
        print(pseudo_code_str + "\n")
    except Exception as e:
        raise Exception(
            "ERROR - Code generator has failed."
        )


def compile_input(input_string):
    '''
    Passes an input string to the tokenizer, parser, semantic analyser, and code generator.

    The function checks whether the previous stage (eg parser) 
    has been successfully completed before moving on to the next stage (eg semantic).
    It does this by checking for the True value of returned boolean variables from
    the various functions (with the exception of tokenize_string() as that's returning a tuple
    needed for the other functions)

    Raises:
        Exception: if input is empty.
        ValueError: if input contains only comments.
    '''
    # Calling tokeniser function:
    try:
        tokens = tokenize_string(input_string)
    except Exception as e:
        raise Exception(
            "ERROR - Tokenization has failed. Review any ValueErrors and ensure the input string is not empty."
        )
    if tokens:
        print("\nTokeniser: Successful. See tokens:\n")
        print_tokens(tokens)
        # Calling parser function:
        parser_passed = parse_tokens(tokens)
    else:
        raise ValueError(
            "ERROR - The input string contains only comments, please review."
        )
    if parser_passed:
        # Calling semantic analyser:
        semantic_passed = semantic_analyzer(tokens)
        if semantic_passed:
            print("\nSemantic analyser: Successful\n")
            print("\nGenerator: Successful. See code generated:\n")
            # Calling generator:
            generate_code(tokens)
    else:
        raise Exception("ERROR - Parser has failed.")


def main():
    """
    Entry point of the program.
    Contains all test inputs (both valid and invalid) 
    to be passed to main compiler functionality.

    You can view a table with all inputs and results in evidence_of_expected_outputs.docx
    """
    
    test_if_statement_1 = "if (a > b) { printf('a is more than b'); };"
    test_if_statement_2 = "if (x > i) { printf('x is more than i'); } elif (i == x) { printf('i is equal to x'); };" 
    test_if_statement_3 = (
        "if (100 > 90) { printf('100 is greater than 90'); } elif (100 > 70) { printf('100 is greater than 70'); } else { printf('100'); };")
    test_if_statement_4 = "if (100 > 90) { printf('100 is greater than 90'); } elif (100 > 70) { printf('100 is greater than 70'); } elif (100 > 50) { printf('100 is greater than 50'); } else { printf('100'); };"
    test_if_statement_5 = "if (a != b) { printf('a is not equal to b'); };"
    test_if_statement_6 = "if (a <= b) { printf('a is either less than or equal to b'); };"
    test_if_statement_7 = "if (x > i) { printf('x'); } else { printf('i'); };"
    test_if_statement_8 = "if (a > b) { if (a != c) { printf('a is more b but not equal to c'); }; };"
    test_print_statement_1 = "printf('oneword');"
    test_print_statement_2 = "printf('this is a statement with lots of characters like AND 12984 $3(^&*&)');"
    test_while_loop_1 = "while (x < 34) { printf('x is less than 34'); x++ }; // example comment to show it doesn't tokenise"
    test_while_loop_2 = "while (x < 10) { if (x > i) { printf('x'); } else { printf('i'); }; x++ };"
    test_while_loop_3 = "while (x == 13) { printf('x is equal to 13'); x++ };"
    test_int_variable_1 = "int x = 876;"
    # Should pass tokenizer & parser but fail semantic due to variable name containing a number:
    invalid_test_int_variable = "int 4 = 76;" 
    test_arith_1 = "7 + 8;"
    test_arith_2 = "342 - 6;"
    test_arith_3 = "5 * 4;"
    test_arith_4 = "100 / 4;"
    # Trying to tokenize comments by themselves will cause Exceptions to be raised:
    invalid_test_comment = "// this is a comment"
    invalid_test_multi_line_comment = "/* this is also a comment */"
    test_comment_plus_text = "int x = 10; // comment" # Tokenisation will remove comment

    # PASS TEST CASE VAR TO FUNC TO START COMPILER OR INPUT OWN STRING:
    compile_input(test_if_statement_1)


if __name__ == "__main__":
    main()
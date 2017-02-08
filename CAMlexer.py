import re

RESERVED = 'RESERVED'
INT = 'INT'
STRING = 'STRING'
ID = 'ID'

tokenExpressions = [
    (r'[ \n\t]+', None),
    (r'#[^\n]*', None),
    (r'==', RESERVED),
    (r'\(', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'!=', RESERVED),
    (r'=', RESERVED),
    (r'"[A-Za-z][A-Za-z0-9_-]*"', STRING),
    (r'and', RESERVED),
    (r'or', RESERVED),
    (r'not', RESERVED),
    (r'if', RESERVED),
    (r'then', RESERVED),
    (r'else', RESERVED),
    (r'while', RESERVED),
    (r'do', RESERVED),
    (r'for', RESERVED),
    (r'to', RESERVED),
    (r'func', RESERVED),
    (r'call', RESERVED),
    (r'end', RESERVED),
    (r'print', RESERVED),
    (r'input', RESERVED),
    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID)]


def lex(characters):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for tokenExpression in tokenExpressions:
            pattern, tag = tokenExpression
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            print('Illegal character: {}\n'.format(characters[pos]))
            return
        else:
            pos = match.end(0)
    return tokens

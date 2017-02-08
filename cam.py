import CAMparser, lexer


def main(filePath):
    filename = filePath
    text = open(filename).read()
    tokens = lexer.lex(text)
    if not tokens:
        return

    parse_result = CAMparser.parse(tokens)
    if not parse_result:
        print("Parse error!")
        return

    ast = parse_result.value
    env = {"printing": []}
    ast.eval(env)

    if __name__ != "__main__":
        return env


if __name__ == "__main__":
    main(input())

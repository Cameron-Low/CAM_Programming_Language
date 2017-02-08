import CAMparser, CAMlexer


def main(filePath):
    filename = filePath
    text = open(filename).read()
    tokens = CAMlexer.lex(text)
    if not tokens:
        return

    parse_result = CAMparser.parse(tokens)
    if not parse_result:
        print("Parse error!")
        return

    ast = parse_result.value
    env = {"printing": []}
    ast.eval(env)
    print(ast)

    if __name__ != "__main__":
        return env


if __name__ == "__main__":
    main(input())

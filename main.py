import argparse, json

OPERATIONS = {
    '+': lambda x, y: x + y,
    'concat': lambda *args: args.join(' '),
    'min': lambda x, y: x % y
}


def evaluate_postfix(expression, constants):
    stack = []
    for token in expression:
        if token in constants:
            stack.append(constants[token])
        elif token in OPERATIONS:
            if token in ['min', 'concat']:
                args = [stack.pop() for _ in range(len(stack))]
                stack.append(OPERATIONS[token](*args))
            else:
                y, x = stack.pop(), stack.pop()
                stack.append(OPERATIONS[token](x, y))
        else:
            stack.append(float(token))
    return stack[0]


def load_json_from_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as error:
        print(f"Error parsing JSON: {error}")
        raise
    except FileNotFoundError as error:
        print(f"File not found: {error}")
        raise


def load_json_from_str(json_str: str) -> dict:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as error:
        print(f"Error parsing JSON: {error}")
        raise


def generate_config(data: dict) -> str:
    def format_value(value, indent_level):
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (int, float, bool)):
            return str(value).lower() if isinstance(value, bool) else str(value)
        elif isinstance(value, list):
            return "[" + ", ".join(format_value(item, indent_level) for item in value) + "]"
        elif isinstance(value, dict):
            return generate_dict(value, indent_level + 1)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    def generate_dict(data: dict, indent_level=0) -> str:
        lines = []
        indent = "    " * indent_level
        next_indent = "    " * (indent_level + 1)

        for key, value in data.items():
            if key == "comment":
                comment = value
                if "\n" in comment:
                    buffer = comment.replace("\n", f"\n{next_indent}")
                    lines.append(f"{next_indent}/*\n{next_indent}{buffer}\n{indent}*/")
                else:
                    lines.append(f"{next_indent}/* {comment} */")
            elif key.startswith("const-"):
                const_name = key[6:]
                lines.append(f"{next_indent}var {const_name} = {format_value(value, indent_level)}")
            else:
                formatted_value = format_value(value, indent_level)
                if isinstance(value, dict):
                    lines.append(f"{next_indent}{key} -> {formatted_value}")
                else:
                    lines.append(f"{next_indent}{key} -> {formatted_value},")

        return "{\n" + "\n".join(lines).rstrip(",") + f"\n{indent}}}"

    return generate_dict(data, indent_level=0)


def main():
    parser = argparse.ArgumentParser(description="Transform Json to custom configuration language.")
    parser.add_argument('--input', required=False, help="Input file path.")
    parser.add_argument('--output', required=True, help="Output file path.")
    args = parser.parse_args()

    if not args.input:
        print("Enter the input json: ", end="")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        data = load_json_from_str("\n".join(lines))
    else:
        data = load_json_from_file(args.input)

    print(data)

    config = generate_config(data)
    with open(args.output, "w") as file:
        file.write(config)


if __name__ == '__main__':
    main()

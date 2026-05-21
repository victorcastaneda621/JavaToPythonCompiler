import os
import re
import sys
import argparse
from java_lexer import JavaLexer
from java_parser import JavaParser
from translator import Translator
from scope import Scope

DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(DIR, "code")

parser_arg = argparse.ArgumentParser(description="Java to Python translator")
parser_arg.add_argument("--file", nargs="?", default=None, help="Path to a .java file to translate (optional)")
args = parser_arg.parse_args()

lexer = JavaLexer()
parser = JavaParser()
translator = Translator()
scope = Scope()

if args.file:
    filepath = os.path.abspath(args.file)
    with open(filepath, "r", encoding="utf-8") as f:
        java_file = f.read()

    tokens = lexer.tokenize(java_file)
    parser.errors = []
    ast = parser.parse(tokens)

    out_dir = os.path.join(DIR, "out")
    os.makedirs(out_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    out_path = os.path.join(out_dir, base_name + ".py")

    if parser.errors:
        result = '\n'.join(parser.errors)
        print(f"PARSER ERROR in file {args.file}")
        with open(out_path, 'w', encoding="utf-8") as output:
            output.write(result)
    else:
        translated_output = translator.translate_initial(ast, scope)
        out_str = '\n'.join(line for line in str(translated_output).split('\n') if line)
        with open(out_path, 'w', encoding="utf-8") as output:
            output.write(out_str)
        print(f"Translated: {out_path}")

else:
    JAVA_FILES = [file for file in os.listdir(TEST_DIR)
                  if os.path.isfile(os.path.join(TEST_DIR, file)) and
                  re.search(r"^[a-zA-Z0-9_].*\.(java)$", file)]

    for filename in JAVA_FILES:
        with open(os.path.join(TEST_DIR, filename), "r", encoding="utf-8") as f:
            java_file = f.read()
        with open(os.path.join(TEST_DIR, filename).replace(".java", ".expected"), "r", encoding="utf-8") as f:
            expected_file = f.read()

        if os.path.isfile(os.path.join(TEST_DIR, filename).replace(".java", ".out")):
            os.remove(os.path.join(TEST_DIR, filename).replace(".java", ".out"))

        tokens = lexer.tokenize(java_file)
        parser.errors = []
        ast = parser.parse(tokens)

        if parser.errors:
            result = '\n'.join(parser.errors)
            print(f"PARSER ERROR in file {filename}")
            with open(os.path.join(TEST_DIR, filename).strip(".java") + '.py', 'w', encoding="utf-8") as output:
                output.write(result)
        else:
            translated_output = translator.translate_initial(ast, scope)
            out_file_lines = [line for line in str(translated_output).split('\n') if line]
            expected_file_lines = [line for line in expected_file.split('\n') if line]

            out_str = '\n'.join(out_file_lines)
            expected_str = '\n'.join(expected_file_lines)

            if expected_str.strip().split() != out_str.strip().split():
                print(f"ERROR in file {filename}")
            else:
                print(f" - file {filename} (CORRECT)")

            with open(os.path.join(TEST_DIR, filename).strip(".java") + '.py', 'w', encoding="utf-8") as output:
                output.write(out_str)
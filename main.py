import os
import re
import sys
from java_lexer import JavaLexer
from java_parser import JavaParser
from translator import Translator
from scope import Scope

PHASE = "03"

DIR = r"C:\Users\Usuario\Desktop\compiler"
sys.path.append(DIR)

TEST_DIR = os.path.join(DIR, PHASE)
JAVA_FILES = [file for file in os.listdir(TEST_DIR)
              if os.path.isfile(os.path.join(TEST_DIR, file)) and
              re.search(r"^[a-zA-Z0-9_].*\.(java)$",file)]

lexer = JavaLexer()
parser = JavaParser()
translator = Translator()
scope = Scope()

tests = {}
expected_results = {}
for filename in JAVA_FILES:
    with open(os.path.join(TEST_DIR, filename), "r", encoding="utf-8") as f:
        java_file = f.read()
    with open(os.path.join(TEST_DIR, filename).replace(".java", ".expected"), "r", encoding="utf-8") as f:
        expected_file = f.read()

    if os.path.isfile(os.path.join(TEST_DIR, filename).replace(".java", ".out")):
        os.remove(os.path.join(TEST_DIR, filename).replace(".java", ".out"))

    if PHASE == "01": # Lexer
        tokens = f'#name "{filename}"\n' + '\n'.join(lexer.output(java_file))
        out_file = [linea.strip() for linea in tokens.split('\n') if linea.strip()]
        expected_file = [linea.strip() for linea in expected_file.split('\n') if linea.strip()]
        out_file = '\n'.join(out_file)
        expected_file = '\n'.join(expected_file)

        if expected_file.strip().split() != out_file.strip().split():
            print(f"ERROR in file {filename}")
            with open(os.path.join(TEST_DIR, filename)+'.out', 'w', encoding="utf-8") as output:
                output.write(out_file.strip())
        else:
            print(f" - file {filename} (CORRECT)")

    elif PHASE == '02': # Parser
        tokens = lexer.tokenize(java_file)
        parser.errors = []
        ast = parser.parse(tokens)
    
        if parser.errors:
            result = '\n'.join(parser.errors)
            print(f"ERROR in file {filename}")
            with open(os.path.join(TEST_DIR, filename)+'.out', 'w', encoding="utf-8") as output:
                output.write(result)
        else:
            result = ast.str(0)
            out_file = [line for line in result.split('\n') if line]
            expected_file_lines = [line for line in expected_file.split('\n') if line]
            out_file_str = '\n'.join(out_file)
            expected_str = '\n'.join(expected_file_lines)
            
            if expected_str.strip().split() != out_file_str.strip().split():
                print(f"ERROR in file {filename}")
                with open(os.path.join(TEST_DIR, filename)+'.out', 'w', encoding="utf-8") as output:
                    output.write(out_file_str)
            else:
                print(f" - file {filename} (CORRECT)")
    elif PHASE == "03": # Translator/Evaluator
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

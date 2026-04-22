import os
import re
import sys
from java_lexer import JavaLexer
from java_parser import JavaParser
#from Clases import *

FASE = "01"

DIR = r"C:\Users\Usuario\Desktop\compiler"
sys.path.append(DIR)

TEST_DIR = os.path.join(DIR, FASE)
JAVA_FILES = [file for file in os.listdir(TEST_DIR)
              if os.path.isfile(os.path.join(TEST_DIR, file)) and
              re.search(r"^[a-zA-Z0-9_].*\.(java)$",file)]

lexer = JavaLexer()
parser = JavaParser()

tests = {}
expected_results = {}
for filename in JAVA_FILES:
    with open(os.path.join(TEST_DIR, filename), "r", encoding="utf-8") as f:
        java_file = f.read()
    with open(os.path.join(TEST_DIR, filename).replace(".java", ".expected"), "r", encoding="utf-8") as f:
        expected_file = f.read()

    if os.path.isfile(os.path.join(TEST_DIR, filename).replace(".java", ".out")):
        os.remove(os.path.join(TEST_DIR, filename).replace(".java", ".out"))

    if FASE == "01": # Lexer
        tokens = f'#name "{filename}"\n' + '\n'.join(lexer.tokenize(java_file))
        out_file = [linea.strip() for linea in tokens.split('\n') if linea.strip()]
        expected_file = [linea.strip() for linea in expected_file.split('\n') if linea.strip()]
        out_file = '\n'.join(out_file)
        expected_file = '\n'.join(expected_file)

        if expected_file.strip().split() != out_file.strip().split():
            print(f"Revisa el fichero {filename}")
            with open(os.path.join(TEST_DIR, filename)+'.out', 'w', encoding="utf-8") as output:
                output.write(out_file.strip())

    elif FASE == "02": # Parser
        pass


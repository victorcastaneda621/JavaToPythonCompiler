# JavaToPythonCompiler
Sly compiler that receives Java code as input and outputs the equivalent Python code, as well as the result of the execution. Only a subset of Java instructions is supported. If run as `python main.py` (no arguments), the test `.java` files provided in the `code` folder will be translated into '.py' files in that same folder, and it will be checked that they are corrected against some `.expected` text files.

For actual usage, you can pass the path of a file as an argument, like in this example with Windows paths:
`python main.py --file .\path\to\java\file.java`

This will create (if it didn't exist already) an `out` folder and the translated `.py` will be saved inside it.

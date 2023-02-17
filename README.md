Creating a simple C-like programming language for fun, with a strange name Ayeyarwady.

First steps are taken from [here](https://medium.com/@marcelogdeandrade/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df)

Requirements:

Anaconda
```bash
$ conda install --channel=numba llvmlite
$ conda install -c conda-forge rply
```
LLC

GCC

Run:
1. `python3 main.py`
2. `llc -filetype=obj build/output.ll`
3. `gcc build/output.o -o build/output`
4. `./build/output`

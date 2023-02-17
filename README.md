### Description
Creating a simple C-like programming language for fun, with a strange name Ayeyarwady.

First steps are taken from [here](https://medium.com/@marcelogdeandrade/writing-your-own-programming-language-and-compiler-with-python-a468970ae6df).

### Requirements:

- Anaconda
- LLC
- GCC
```bash
$ conda install --channel=numba llvmlite
$ conda install -c conda-forge rply
```

To run:
```bash
    python3 main.py
    llc -filetype=obj build/output.ll
    gcc build/output.o -o build/output
    ./build/output
```

Or simply: 
```bash
./run.sh
```

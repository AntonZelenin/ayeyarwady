#!/bin/bash

python3 aye/main.py
llc -filetype=obj build/output.ll
gcc build/output.o -o build/output
./build/output

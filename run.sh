#!/bin/bash

python3 ayeyarwady/main.py
llc -filetype=obj build/output.ll
gcc build/output.o -o build/output
./build/output

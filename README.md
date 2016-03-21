# SAT Solver LvR

Main file for running the SAT solver is satsolver.py. The tests included for submission are in /tests folder.

The tests are run via command:

```
python satsolver.py [input file] [output file] 
```
The input file is in dimacs input format and the output is in the dimacs result format.

Note that the input file must not contain lines with starting with anything other than "c", "p" or clause lines (as some dimacs files do).

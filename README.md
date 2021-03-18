# Statistical hypothesis tests for exploring relational data

## Overview

This repository contains two Jupyter notebooks and two standalone Python command line tools to examine the structure of a binary relation that is formatted as a boolean `numpy` array.

## Installation

Install Python 3.x along with `numpy`.

The command line tools `bernoulli_test.py` and `redundancy_sort.py` are self-contained and require no further installation.

## Operation

### Command line tool: `bernoulli_test`

The command line tool is intended to help identify a set of rows from a binary matrix that are likely misclassified.  The command line tool takes as input a threshold (decimal between 0 and 1) and two files that describe two binary relations.  Briefly, given a calling sequence like

```
 $ bernoulli_test <threshold> <file1.txt> <file2.txt>
```

the program will output the 0-based indices of rows in file1 that that probably should have been in file2.  Both files need to have the same number of entries in each row.

The input files are space-delimited streams of "0" or "1" entries, split into equal-length rows.  Each row corresponds to an observation, each entry corresponds to a Boolean response variable.

### Command line tool: `redundancy_sort`

This command line tool Sorts columns in a binary matrix from least to most redundant, grouped based upon column labels.  It is used by

```
 $ redundancy_sort  <matrix_file.txt> <column_headers.txt>
```

The program will dump a sorted list of column headers from <column_headers.txt> to stdout.

## Acknowledgment

This material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) SafeDocs program under contract HR001119C0072.  Any opinions, findings and conclusions or recommendations expressed in this material are those of the author and do not necessarily reflect the views of DARPA.

## License

Copyright © 2020 Michael Robinson

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

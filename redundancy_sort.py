# Sort columns in a binary matrix from least to most redundant, grouped based upon column labels
#
# Usage:
#  redundancy_sort  <matrix_file.txt> <column_headers.txt>
#
# The program will dump a sorted list of column headers from <column_headers.txt> to stdout

# Copyright (c) 2020 Michael Robinson
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
#
# This material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) SafeDocs program under contract HR001119C0072.
# Any opinions, findings and conclusions or recommendations expressed in this material are those of the author and do not necessarily reflect the views of DARPA.

import numpy as np
import argparse

def run_redundancy_sort(relation_mat,rows_list):
    '''
    Sort the unique entries of rows_list according to their redundancy of rows in the relation_mat matrix 
    '''
    # Unique row tags
    rows=list(set(rows_list))

    # How many occurences of 1 in each row
    msg_count=np.sum(relation_mat,axis=1)

    # Correlation matrix
    cor_mat=np.abs(np.corrcoef(1-relation_mat))

    # Perform grouping using median
    grouped_cor=np.zeros((len(rows),len(rows)))
    for i1,p1 in enumerate(rows):
        for i2,p2 in enumerate(rows):
            idx1=[ix for ix,p in enumerate(rows_list) if p==p1 and msg_count[ix]>0]
            idx2=[ix for ix,p in enumerate(rows_list) if p==p2 and msg_count[ix]>0]
            if idx1 and idx2:
                grouped_cor[i1,i2]=np.nanmedian(cor_mat[np.ix_(idx1,idx2)].flatten())

    # Output sorted list
    idx=np.argsort(np.nanmedian(grouped_cor,axis=0))
    return([rows[i] for i in idx])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort columns in a binary matrix from least to most redundant, grouped based upon column labels')
    parser.add_argument('matrix_file',help='Test file, consists of whitespace-separated rows of "0" or "1"')
    parser.add_argument('column_headers_file',help='List of column headers for "matrix_file", one per line')

    args = parser.parse_args()
    
    # Ingest the input files
    relation_mat=np.transpose(np.loadtxt(args.matrix_file))
    with open(args.column_headers_file) as fp:
        column_headers = fp.readlines()

    # Run the test
    sorted_column_headers=run_redundancy_sort(relation_mat,column_headers)

    # Dump to stdout
    for i in sorted_column_headers:
        print(i)

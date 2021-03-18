# Identify a set of rows from a binary matrix that are likely misclassified
#
# Usage:
#  bernoulli_test <threshold> <file1.txt> <file2.txt>
#
# The program will dump a list of 0-based row indices from <file1.txt> to stdout

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

def run_bernoulli_test(threshold,set1_relation_mat,set2_relation_mat):
    '''
    Run the Bernoulli test statistic on two matrices to identify columns of one matrix that ought to be columns in a second matrix because they fit its statistics better.

    Input: 
      threshold         : Percentage of columns to accept as being "within bounds", and therefore not misclassification
      set1_relation_mat : matrix of rows (variables) and columns (observations)
      set2_relation_mat : matrix of rows (variables) and columns (observations)
    Output:
       np.array of integer indices of columns of set1_relation_mat (observations) that better match the statistics of set2_relation_mat

    Note: Lower thresholds result in more columns being returned.
    '''

    # Compute row-wise probabilities for each column
    set1_row_prob=np.mean(set1_relation_mat,axis=1)
    set2_row_prob=np.mean(set2_relation_mat,axis=1)

    s1p=np.expand_dims(set1_row_prob,1)
    s2p=np.expand_dims(set2_row_prob,1)

    # Bernoulli likelihood functions for each file and under both correct and misclassified hypotheses
    set1_bern_likely_correct=np.prod(s1p*set1_relation_mat+(1-s1p)*(1-set1_relation_mat),axis=0)
    set1_bern_likely_incorrect=np.prod(s2p*set1_relation_mat+(1-s2p)*(1-set1_relation_mat),axis=0)

    # Compute likelihood ratio
    bern_lr=set1_bern_likely_incorrect/set1_bern_likely_correct

    # Clean up any faulty entries
    bern_lr[np.logical_not(np.isfinite(bern_lr))]=np.inf

    # Normalize the threshold based on percentage
    thres=np.sort(bern_lr)[int(threshold*len(bern_lr))]
    
    # Postprocessing/thresholding
    idx=np.where(np.logical_and(np.isfinite(bern_lr),bern_lr>thres))[0]
    return idx

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Identify rows in file1 that that probably should have been in file2.  Both files need to have the same number of entries in each row.')
    parser.add_argument('threshold',type=float,help='Percentile threshold for decision')
    parser.add_argument('file1',help='Test file, consists of whitespace-separated rows of "0" or "1"')
    parser.add_argument('file2',help='Training file, consists of whitespace-separated rows of "0" or "1"')

    args = parser.parse_args()
    
    # Ingest the input files
    set1_relation_mat=np.transpose(np.loadtxt(args.file1))
    set2_relation_mat=np.transpose(np.loadtxt(args.file2))

    # Run the test
    idx=run_bernoulli_test(args.threshold,set1_relation_mat,set2_relation_mat)

    # Dump to stdout
    for i in idx:
        print(i)

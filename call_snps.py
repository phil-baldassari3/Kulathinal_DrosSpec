#3rd iteration of the python based SNP calling tool.  Goal is to make an alignment dataframe and filter out the monomorphic sites.

#importing modules
import os
import pandas as pd
import numpy as np
import sys
import itertools

#setting directory
directory = "/Users/philipbaldassari/desktop/seq_diff_test/"

#opening fasta and converting to dictionary
with open("aln_test.fa") as file_one:
    fasta = {line.strip(">\n"):next(file_one).rstrip() for line in file_one}

#converting values in dictionary to list
    for k, v in fasta.items():
            fasta[k] = list(v)
    
#making dataframe from dictionary
aln = pd.DataFrame.from_dict(fasta)

#Replace N with NaN
aln = aln.replace('N', np.nan)



#Add Locus column
aln.insert(0, "Locus", aln.index + 1)

#new dataframe for bp counts
counts = pd.DataFrame(columns = ["Acount", "Tcount", "Ccount", "Gcount"])

#iterating through aln dataframe and counting bps for counts dataframe by tuples
for row in aln.itertuples():
                
        Acount = row.count("A")
        Tcount = row.count("T")
        Ccount = row.count("C")
        Gcount = row.count("G")
        
        counts = counts.append({'Acount' : Acount, 'Tcount' : Tcount, 'Ccount' : Ccount, 'Gcount' : Gcount}, 
                ignore_index = True)

#merging counts to aln dataframe by index
aln = pd.merge(aln, counts, left_index=True, right_index=True)

#summing for total bp count
aln["bpcount"] = aln['Acount'] + aln['Tcount'] + aln['Ccount'] + aln['Gcount']

#getting rid of rows with zero bps
aln = aln[aln.bpcount !=0]

#allele frqeuncies per nucleotide
aln['Aprop'] = aln['Acount']/aln['bpcount']
aln['Tprop'] = aln['Tcount']/aln['bpcount']
aln['Cprop'] = aln['Ccount']/aln['bpcount']
aln['Gprop'] = aln['Gcount']/aln['bpcount']

#Major allele Frequency
aln['MajorAF'] = aln[["Aprop","Tprop","Cprop","Gprop"]].max(axis=1)

#getting rid of monomorphic sites
aln = aln[aln.MajorAF !=1]

#saving as csv
aln.to_csv('SNPs_called_test.csv', index=False)

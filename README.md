# Kulathinal Lab DrosSpec Scripts

Here is Phil's repository for scripts for the DrosSpec Project

This repo contains:

Miscellaneous:

search+replace.py --->
Simple script to search and replace characters in txt files.

check-looper.py --->
Script that loops through the seq directories and does various checks like checking the length of each sequence and printing chunks of aligned sequences.

get-pop-ids.py & sample-ids.py --->
Scripts for printing pop ids and sample ids to txt files.

VCF processing:

zim-cos_vcf_maker.sh --->
Bash script to create vcfs from the seq files using seq2fas.py, hap2dip.py, vcf_fixer_N_common.py and vcf_fixer_N_uncommon.py. This script makes sure to fix the missing alleles and the corresponding counts by splitting the vcfs into N_common and N_uncommon and fixing each file separately before concatenating them.

-------> seq2fas.py ---> Script that loops though the seq directory and converts each to a fast file in a new directory.

-------> hap2dip.py ---> Script that makes the haploid vcfs from sap-sites package diploid (crudely) by replacing 1 with 1/1, 0 with 0/0, etc.

-------> vcf_fixer_N_common.py & vcf_fixer_N_uncommon.py ---> Scripts that fix the separated vcfs containing sites with N_common or N-uncommon.

vcf_sample-sites_2csv.py --->
Script using the unfiltered vcfs from zim-cos_vcf_maker.sh and performs counts on major allele, minor allele, and missing allele to create csv files.

vcf_sample-sites_filtering.py --->
Script takes the csv files from vcf_sample-sites_2csv.py and outputs a sites filtration txt file with all sites excluding singletons. These text files can be used with vcftools --positions to filter the actual vcfs and bcftools should be used to remove triallelic SNPs

zim-cos_pca-plots.R & pca-plots.R --->
Using the snprelate and ggplot2 packages, this script performs a PCA analysis on the vcfs

vcf_allele-counts_downsample_2csv.py --->
Script that loops through VCFs and randomly downsamples according set sample sizes per population. Outputs a csv with Chromosomes, position, major allele frequencies and counts per population and minor allele frequencies and counts per population.

Seq processing:

seq2SNPcsv_preprocess.sh --->
Bash script that uses fas_chuncks.py, concat_fas.sh, and call_snps.py to scan through seq files and create csv files that print the sites, allele counts and allele proportions.

-------> fas_chuncks_Chr2L.py ---> Example script of fas_chuncks.py that can be modified for other chromosomes. This script is the same as seq2fas.py except it breaks the genome into 200,000 bp chunks which need to be concatenated. Script also outputs txt list files that are used to concatenate.

-------> concat_fas_chr2L.sh ---> Example script of concat_fas.sh that can be modified for other chromosomes. Bash script uses the txt list files output from fas_chuncks.py to concatenate corresponding individual fats files into fasta alignment files by chunk.

-------> call_snps_chr2L.py ---> Example script of call_snps.py that can be modified for other chromosomes. Scans through the fasta alignment files and outputs a csv of all SNPs with corresponding allele counts and proportions. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This needs to be done before seq2SNPcsv_preprocess.sh is done!

SNPcsv_filtering.sh --->
Bash script to filter out and overwrite SNP csvs without singletons and triallelic sites. This script uses filter_SNP_csvs.py.

-------> filter_SNP_csvs.py ---> Script filter out singletons and triallelic sites by replacing singletons with "N" and recounting and removing sites with more than 2 variants. This script needs to be placed in each directory where filtering is needed. csv files are overwritten with the filtered data. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This needs to be done before SNPcsv_filtering.sh is done!

SNPcsv_downsampling.sh --->
Bash script to randomly downsample the SNP csvs into csvs that print the chromosomes, positions, minor allele frequencies, and downsampled sample sizes by population. Script uses downsample_SNP_csvs.py.

-------> downsample_SNP_csvs.py ---> Script randomly downsamples the SNP csvs into csvs that print the chromosomes, positions, minor allele frequencies, and downsampled sample sizes by population. Random downsampling is performed 10 times per population and the frequencies are averages across each iteration. This script needs to be placed in each directory where downsampling is needed. The downsampled sample sizes can be set at the beginning of the script. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This needs to be done before SNPcsv_downsampling.sh is run!

Fst Analysis:

pairwise_fst_from_seq.R --->
Script to estimate pairwise Fst between populations. Only sites with exactly the number of samples as the set sample size are kept. Fst is estimated using the Hudson 1992 estimator from Bhatia 2013. csvs are output.

fst_gene_find.R --->
Script to take the top 1% of sites with the highest average Fst between multiple pairwise comparisons.  Outputs a smaller version of the Fst csvs with only the top 1% of sites.

r5_to_r6_coordinate_converter.sh --->
Script to take flybase coordinates from the fst_gene_find.R csvs and convert them from r5 to r6 using the perl script provided by flybase (dmel_r5_to_r6_converter.pl).  It used the python scripts coordinate_scraper_r5.py and coordinate_scraper_r6.py which must be prepared for multiprocessing pool. The bash script pauses to allow for this.

-------> coordinate_scraper_r5.py ---> Script to scrape r5 coordinates from the csvs and save them as text files that can be ran through dmel_r5_to_r6_converter.pl to be converted to r6 coordinates. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This can be done when prompted by r5_to_r6_coordinate_converter.sh

-------> coordinate_scraper_r6.py ---> Script to scrape r6 coordinates from the conversion files from dmel_r5_to_r6_converter.pl and save them to text files. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This can be done when prompted by r5_to_r6_coordinate_converter.sh

SNP_gene_mapper.py --->
Script that takes in flybase Dmel point coordinates and maps those sites to gene maps provided by flybase. These coordinates should be in flybase format in in text files separated by line breaks. csvs with gene lists in FBgn and gene symbols are output. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This needs to be done before SNP_gene_mapper.py is run!

null_genes_df_consolidator.py --->
This script merges the null sites dataframes with the gene hits dataframes. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This needs to be done before null_genes_df_consolidator.py is done.

null_GO_annotator.py --->
This script uses GO annotation lists of specific GO terms and annotates the genes from the null dataframes. This script is specifically marking neurogenesis, mating behavior, male mating behavior, and female mating behavior genes. This script uses the Pool from the python module, multiprocessing. Thus, a list of input files needs to be mapped to the function. Use the commented out block at the beginning of the script to print a list of input files which can be copied into the mapping list. This needs to be done before null_GO_annotator.py is done.

sliding_window_fst.py & sliding_window_fst_by_filtering --->
Two versions of the same script that takes the per site Fst data and averages by sliding window and outputs new csv files.  Uses multiprocessing.  These scripts take unusually long which will have to be fixed in the future.  Also, sliding_window_fst.py has been modified to fix the type error (float type nan cannot be averaged) that is thrown when the list contains nan values.

pairwise_fst_from_vcf.R --->
Script to estimate pairwise Fst between populations. Only sites with exactly the number of samples as the set sample size are kept. Fst is estimated using the Hudson 1992 estimator from Bhatia 2013. csvs are output.























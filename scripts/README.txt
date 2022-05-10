Scripts to query PlutoF for SH membership for sequences/sequence names from a FASTA file, and to query PlutoF for taxonomy for given SHs. To generate the files needed by the nf-core/ampliseq Nextflow workflow for the optional argument --addsh, the following procedure is suggested:

* Run create_sequence-SH_matching.py to find sequence to SH matchings
* From the list, extract the names of all SHs
* Run find_SH_taxonomy.py to find complete taxonomies for the SHs

For short usage information, run
create_sequence-SH_matching.py -h
and/or
find_SH_taxonomy.py -h

Example code for UNITE release 8.3:
./create_sequence-SH_matching.py -f sh_general_release_10.05.2021/sh_general_release_dynamic_10.05.2021.fasta -c 1.5 -v 8 -o sh_general_release_dynamic_10.05.2021.seq2sh.tsv > sh_10.05.2021.log 2>&1 &
cut -f 2 sh_general_release_dynamic_10.05.2021.seq2sh.tsv | sort -u > sh_general_release_dynamic_10.05.2021.SHs.txt
./find_SH_taxonomy.py -i sh_general_release_dynamic_10.05.2021.SHs.txt -o sh_general_release_dynamic_10.05.2021.SHs.tax -s all_taxons_10.05.2021.tsv > sh_10.05.2021.SHtax.log 2>&1 &
bzip2 sh_general_release_dynamic_10.05.2021.seq2sh.tsv sh_general_release_dynamic_10.05.2021.SHs.tax

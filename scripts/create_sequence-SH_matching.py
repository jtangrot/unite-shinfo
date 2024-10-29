#!/usr/bin/python3
#@author Jeanette Tångrot

# Script to query PlutoF for SHs at a given identity level, in order to create a
# file with sequence-SH matchings for sequences in a given fasta file.
# Names in fasta file are assumed to be in the same format as in the UNITE general
# FASTA release (sh_general_release-files), e.g.:
# >Symbiotaphrina_buchneri|DQ248313|SH1641879.08FU|reps|k__Fungi;p__Ascomycota;c__Xylonomycetes;o__Symbiotaphrinales;f__Symbiotaphrinaceae;g__Symbiotaphrina;s__Symbiotaphrina_buchneri
# ... i.e. sequence name is the entry after the first "|".
#
# Input: Fasta file, e.g. UNITE general FASTA release
# Output: Tab separated text file with one sequence name and the corresponding SH on each line
# 
# Usage: create_sequence-SH_matching.py -f <UNITE.fa> -o <seq2SH.txt> [-c <id> -v <version>]
#        -f <UNITE.fa>: Fasta file
#        -o <seq2SH.txt>: Name of resulting sequence to SH matching file
# Options:
#        -c <id>: SH identity level. Default: 1.5
#        -v <version>: SH version. Default: 8
#

#--- Import libraries, do initializations  ---#
import sys
import getopt
import os.path 
import requests
import json

def main():
    usage = """create_sequence-SH_matching.py -f <UNITE.fa> -o <seq2SH.txt> [-c <id> -v <version>]
                 -f <UNITE.fa>: Fasta file
                 -o <seq2SH.txt>: Name of resulting sequence to SH matching file. Default: seq2SH.tsv
               Options:
                 -c <id>: SH identity level. Default: 1.5
                 -v <version>: SH version. Default: 8
    """

    fasta_in = ""
    file_out = "seq2SH.tsv"
    sh_id = 1.5
    ver = 8

    #--- Read and store command line arguments ---#
    try:
        opts, args = getopt.getopt(sys.argv[1:],"c:hf:o:v:")
    except getopt.GetoptError:
        print( usage )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( usage )
            sys.exit()
        elif opt == "-c":
            sh_id = arg
        elif opt == "-f":
            fasta_in = arg
        elif opt == "-o":
            file_out = arg
        elif opt == "-v":
            ver = arg

    if os.path.isfile( file_out ):
        sys.exit('Output file ' + file_out + ' already exists. Please remove or use another name (option -o).')

    if fasta_in == "":
        sys.exit( 'You need to supply a fasta file with sequences to extract SH for.\nUsage: ' + usage )

    #---  Read each entry in fasta, find sequence name and query PlutoF, write to file ---#
    fh = open( fasta_in, mode = 'r' )
    fh_out = open( file_out, mode = 'w', buffering = 1 )
    for row in fh:
        if row.startswith('>'):
            try:
                name = row.split('|')[1]
            except ValueError:
                sys.exit( 'Names in fasta file seem to be incorrectly formatted. The sequence name is expected to be found after the first "|" in the identifier.' )
            [SH, taxon] = query_PlutoF(name, str(sh_id), str(ver))
            fh_out.write( name + "\t" + SH  + "\t" + taxon +  "\n" )
    fh.close()
    fh_out.close()
    
#--- Define functions ---#
def query_PlutoF(name, sh_id = "1.5", version = "8"):
    # The following lines were needed in previous versions of the PlutoF API
    #thresholds = {"3": "1", "2": "2", "1": "3", "2.5": "4", "1.5": "5", "0.5": "6"}
    #thresh = thresholds[ sh_id ]
    #query = "q=" + name + "&th=" + thresh + "&v=" + version
    # Seems not to matter what version I ask for - always get all versions
    # Need to loop through to find correct version

    # New query line
    query = "sequence_accession_nr=" + name + "&threshold=" + sh_id + "&version=" + version
    try:
        response = requests.get( "https://api.plutof.ut.ee/v1/public/dshclusters/search/?" + query ) 
    except ValueError:
        sys.exit('Error when querying PlutoF for ' + name)
    # There can be several SHs for the same sequence;
    # loop through all and select the one with no conflict and a value on "designators".
    # Error if many SHs with the same properties (conflict status, designator status)
    # Also, store taxon if available.
    SH = ""
    taxon = ""
    numSH = 0
    for data in response.json()['data']:
        if data['attributes']['version'] == "Version " + str(version):
            if SH == "":
                SH = data['attributes']['name']
                conflict = data['attributes']['has_conflict']
                designator = data['attributes']['designators']
                try:
                    if data['relationships']['taxon_node']['data']['type'] == "Taxon":
                        taxon = data['relationships']['taxon_node']['data']['id']
                except KeyError:
                    taxon = ""
                numSH = 1
            elif not data['attributes']['has_conflict']:
                if conflict:
                    SH = data['attributes']['name']
                    conflict = data['attributes']['has_conflict']
                    designator = data['attributes']['designators']
                    try:
                        if data['relationships']['taxon_node']['data']['type'] == "Taxon":
                            taxon = data['relationships']['taxon_node']['data']['id']
                    except KeyError:
                        taxon = ""
                    numSH = 1
                elif not designator:
                    if data['attributes']['designators']:
                        SH = data['attributes']['name']
                        conflict = data['attributes']['has_conflict']
                        designator = data['attributes']['designators']
                        try:
                            if data['relationships']['taxon_node']['data']['type'] == "Taxon":
                                taxon = data['relationships']['taxon_node']['data']['id']
                        except KeyError:
                            taxon = ""
                        numSH = 1
                    else:
                        newSH = data['attributes']['name']
                        numSH += 1
                elif data['attributes']['designators']:
                    numSH += 1
            elif conflict:
                numSH +=1
    if numSH == 0:
        print( "WARNING: SH not found for " + name, file=sys.stderr, flush = True )
    elif numSH > 1:
        print( "ERROR: Several \"best\" SHs found for " + name, file=sys.stderr, flush = True )
        SH = ""
        taxon = ""
    return [SH, taxon]

#--- Run it all ---#
if __name__ == '__main__':
    main()

#!/usr/bin/python3
#@author Jeanette Tångrot

# Script to query PlutoF for all taxonomic ranks for the given SHs.
#
# Input: A file with a list of SHs, one SH per row
# Output: Tab separated text file with SH name followed by taxonomy; kingdom,phylum,class,order,family,genus,species

# Usage: find_SH_taxonomy.py -i <SHs.list> -o <SHtax.tsv>
#        -i <SHs.list>: Text file with list of SHs to examine
#        -o <SHtax.tsv>: Name of file with results
# Options:
#        -s <taxons.tsv>: Give a file name if you want to save taxonomy list
#

#--- Import libraries, do initializations  ---#
import sys
import getopt
import os.path 
import requests
import json

def main():
    usage = """find_SH_taxonomy.py -i <SHs.list> -o <SHtax.tsv> [-s <taxons.tsv>]
                -i <SHs.list>: Text file with list of SHs to examine
                -o <SHtax.tsv>: Name of results file
               Optional:
                -s <taxons.tsv>: Give a file name if you want to save taxonomy list
    """

    file_in = ""
    file_out = "SHtax.tsv"
    taxfile = ""
    taxontable = {}

    #--- Read and store command line arguments ---#
    try:
        opts, args = getopt.getopt(sys.argv[1:],"c:hi:o:s:")
    except getopt.GetoptError:
        print( "Usage: " + usage )
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print( "Usage: " + usage )
            sys.exit()
        elif opt == "-i":
            file_in = arg
        elif opt == "-o":
            file_out = arg
        elif opt == "-s":
            taxfile = arg

    if os.path.isfile( file_out ):
        sys.exit('Output file ' + file_out + ' already exists. Please remove or use another name (option -o).')

    if file_in == "":
        sys.exit( '\nYou need to supply a list of SHs to find taxonomy for (option -i).\n\nUsage: ' + usage )

    if taxfile != "" and os.path.isfile( taxfile ):
        sys.exit('Taxonomy report file ' + taxfile + ' already exists. Please remove or use another name (option -s).')
        
    #---  Read each SH, query PlutoF, fill in taxonomy, write results ---#
    ranks = ['kingdom','phylum','class','order','family','genus','species']
    fh = open( file_in, mode = 'r' )
    fh_out = open( file_out, mode = 'w' )
    for row in fh:
        SH_tax = {}
        SH = row.strip()
        if SH == "": continue
        print( SH, flush=True )
        #--- Find taxon for SH ---#
        [taxon, name, rank, lineage] = query_PlutoF_taxonForSH( SH )
        if taxon in taxontable:
            if taxontable[ taxon ]['name'] != name or taxontable[ taxon ]['rank'] != rank:
                sys.exit('taxon ' + taxon + ' have ambigious name and/or rank')
        else:   
            taxontable[ taxon ] = { 'name': name, 'rank': rank }
        if rank in ranks:
            SH_tax[ rank ] = name
        elif rank != "":
            print( "WARNING: Rank " + rank + " is not listed." )
        SH_tax[ 'taxon' ] = taxon
        #--- Find ranks and names for taxons in lineage for higher ranks ---#
        for tax in lineage:
            if tax in taxontable:     
                if taxontable[ tax ]['rank'] in ranks:
                    SH_tax[ taxontable[ tax ]['rank'] ] = taxontable[ tax ]['name']
            else:
                [rank, name] = query_PlutoF_taxon( tax )
                if rank in ranks:
                    SH_tax[ rank ] = name
                taxontable[ tax ] = { 'name': name, 'rank': rank }
        #--- Write results for SH to file ---#
        fh_out.write( SH + "\t" + SH_tax[ 'taxon' ] )
        for rank in ranks:
            if rank in SH_tax:
                fh_out.write( "\t" + SH_tax[ rank ] )
            else:
                fh_out.write( "\t" + "" )
        fh_out.write( "\n" )
            
    fh.close()
    fh_out.close()

    #--- Write taxontable to file ---#
    if taxfile != "":
        fh_out = open( taxfile, mode = 'w' )
        for tax in taxontable:
            fh_out.write( tax + "\t" + taxontable[ tax ][ 'rank' ] + "\t" + taxontable[ tax ][ 'name' ] + "\n" )
        fh_out.close()
        
    
#--- Define functions ---#
def query_PlutoF_taxon( taxon ):
    # Query PlutoF for rank and name for a given taxon id
    try:
        response = requests.get( "https://api.plutof.ut.ee/v1/public/taxa/" + taxon ) 
    except ValueError:
        sys.exit('Error when querying PlutoF for ' + taxon)

    rank = response.json()['data']['attributes']['rank']
    name = response.json()['data']['attributes']['name']

    return [rank.lower(), name] 


def query_PlutoF_taxonForSH( sh ):
    # Query PlutoF for taxon id, rank, name and lineage for a given SH

    #--- First find taxon id... ---#
    query = "name=" + sh
    try:
        response = requests.get( "https://api.plutof.ut.ee/v1/public/dshclusters/search/?" + query ) 
    except ValueError:
        sys.exit('Error when querying PlutoF for ' + query)
    for data in response.json()['data']:
        if data['attributes']['name'] == sh :
            try:
                taxon = data['relationships']['taxon_node']['data']['id']
            except KeyError:
                print( "WARNING: SH "+ sh + " lacks taxonomy", file=sys.stderr, flush=True )
                taxon = ""

        else:
            print( "SH name " + data['attributes']['name'] + " is not the same as " + sh , flush=True )
    
    #--- ...then find name, rank and lineage for that taxon ---#
    if taxon != "":
        try:
            response = requests.get( "https://api.plutof.ut.ee/v1/public/taxa/" + taxon ) 
        except ValueError:
            sys.exit('Error when querying PlutoF for ' + taxon)

        rank = response.json()['data']['attributes']['rank']
        name = response.json()['data']['attributes']['name']

        lineage = []
        for reldata in response.json()['data']['relationships']['lineage']['data']:
            if reldata['type'] == "Taxon":
                lineage.append(reldata['id'])
    else:
        rank = ""
        name = ""
        lineage = []

    return [taxon, name, rank.lower(), lineage]

#--- Run it all ---#
if __name__ == '__main__':
    main()


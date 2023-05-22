# SH information from UNITE databases

## General information

Author: SBDI molecular data team  
Contact e-mail: jeanette.tangrot@nbis.se  
DOI: 10.17044/scilifelab.19411403  
License: CC BY-SA 4.0  
Categories: Microbiology not elsewhere classified, Microbial ecology, Microbial genetics,
Plant and fungus systematics and taxonomy  
Item type: Dataset  
Keywords: ITS, UNITE, PlutoF, SBDI, Ampliseq, Species Hypothesis, SH  
Funding: Swedish Research Council (VR), grant number 2019-00242.  

This README file was last updated: 2023-05-22

Please cite as: Swedish Biodiversity Data Infrastructure (SBDI; 2023). SH information for UNITE databases. https://doi.org/10.17044/scilifelab.19411403

## Dataset description

The data in this repository is the result of querying the PlutoF API (https://plutof.docs.apiary.io, Abarenkov et al 2010) with all sequence names in the UNITE general FASTA release (https://doi.org/10.15156/BIO/2483911; Abarenkov et al. 2022), in order to find the sequence hypothesis (SH) at level 1.5, version 9, for each sequence, resulting in a sequence-to-SH matching file (*.seq2SH.tsv). For each SH, the complete taxonomy is extracted from PlutoF by querying the PlutoF API, and stored in the *.SH.tax files.

Files are available for UNITE version 9.0; sh_general_release_dynamic_29.11.2022.seq2sh.tsv.bz2 containing sequence to SH matchings, and sh_general_release_dynamic_29.11.2022.SHs.tax.bz2 containing SH taxonomies. Corresponding files are also available for the all eukaryotes version of the UNITE database (https://doi.org/10.15156/BIO/2483913; Abarenkov et al 2022b). All files are tab separated text files compressed with bzip2.

Assignment of species hypothesis to ITS amplicons using this data and the UNITE general FASTA release is available as an optional argument to the nf-core/ampliseq Nextflow workflow from version 2.3.2: `--addsh` together with `--dada_ref_taxonomy unite-fungi` or `--dada_ref_taxonomy unite-alleuk` (https://nf-co.re/ampliseq; Straub et al. 2020).

### Generation of files

After download and file extraction of the UNITE general FASTA release, each sequence name in the fasta file was used as query to PlutoF to find which SH at level 1.5 in release 9 the sequence belongs to, in order to generate the *.seq2sh.tsv files with sequence to SH matchings. Each SH was subsequently used as query to PlutoF to extract the complete taxonomy for the SH, stored in the *.SHs.tax files.
Two python scripts for automatic querying and generation of the files can be found in the `scripts` folder in the GitHub repo: https://github.com/biodiversitydata-se/unite-shinfo. See the accompanying README file for usage information.

## References

Abarenkov, Kessy; Tedersoo, Leho; Nilsson, R. Henrik; Vellak, Kai; Saar, Irja; Veldre, Vilmar; Parmasto, Erast; Prous, Marko; Aan, Anne; Ots, Margus; Kurina, Olavi; Ostonen, Ivika; Jõgeva, Janno; Halapuu, Siim; Põldmaa, Kadri; Toots, Märt; Truu, Jaak; Larsson, Karl-Henrik; Kõljalg, Urmas (2010). PlutoF - a Web Based Workbench for Ecological and Taxonomic Research, with an Online Implementation for Fungal ITS Sequences. Evolutionary Bioinformatics 6, 189-196. https://doi.org/10.4137/EBO.S6271

Abarenkov, Kessy; Zirk, Allan; Piirmann, Timo; Pöhönen, Raivo; Ivanov, Filipp; Nilsson, R. Henrik; Kõljalg, Urmas (2022): UNITE general FASTA release for Fungi. Version 16.10.2022. UNITE Community. https://doi.org/10.15156/BIO/2483911

Abarenkov, Kessy; Zirk, Allan; Piirmann, Timo; Pöhönen, Raivo; Ivanov, Filipp; Nilsson, R. Henrik; Kõljalg, Urmas (2022b): UNITE general FASTA release for eukaryotes. Version 16.10.2022. UNITE Community. https://doi.org/10.15156/BIO/2483913

Straub, Daniel, Nia Blackwell, Adrian Langarica-Fuentes, Alexander Peltzer, Sven Nahnsen, and Sara Kleindienst. 2020. “Interpretations of Environmental Microbial Community Studies Are Biased by the Selected 16S RRNA (Gene) Amplicon Sequencing Pipeline.” Frontiers in Microbiology 11. https://doi.org/10.3389/fmicb.2020.550420.

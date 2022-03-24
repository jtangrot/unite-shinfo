# SH information from UNITE databases

## General information

Author: SBDI molecular data team  
Contact e-mail: jeanette.tangrot@nbis.se  
DOI:  
License: CC BY-SA 4.0  
Version:  
Categories: Microbial ecology (310703), Microbial genetics (310704), Medical microbiology not elsewhere classified (320799)  
Item type: Dataset  
Keywords: ITS, UNITE, PlutoF, SBDI, Ampliseq  
Funding:  

This README file was last updated: 2022-03-24

Please cite as: Swedish Biodiversity Infrastructure (SBDI; 2022). SH information for UNITE databases. https://doi.org/...

## Dataset description

The data in this repository is the result of querying the PlutoF API (https://api.plutof.ut.ee/public) with all sequence names in the UNITE general FASTA release (https://doi.org/10.15156/BIO/786368; Abarenkov et al. 2020, https://doi.org/10.15156/BIO/1280049; Abarenkov et al. 2021), in order to find the sequence hypothesis (SH) at level 1.5, version 8, for each sequence, resulting in a sequence-to-SH matching file (*.seq2SH.tsv). For each SH, the complete taxonomy is extracted from PlutoF by querying the PlutoF API, and stored in the *.SH.tax files.

Files are available for UNITE version 8.2; sh_general_release_dynamic_04.02.2020.seq2sh.tsv.bz2 containing sequence to SH matchings, and sh_general_release_dynamic_04.02.2020.SHs.tax.bz2 containing SH taxonomies, and for UNITE version 8.3; sh_general_release_dynamic_10.05.2021.seq2sh.tsv.bz2 and sh_general_release_dynamic_10.05.2021.SHs.tax.bz2. All files are tab separated text files compressed with bzip2.

Assignment of species hypothesis to ITS amplicons using this data and the UNITE general FASTA release is available as an optional argument to the nf-core/ampliseq Nextflow workflow from version 2.3: `--addsh` together with `--dada_ref_taxonomy unite-fungi` (https://nf-co.re/ampliseq; Straub et al. 2020).

### Generation of files

After download and file extraction of the UNITE general FASTA release, each sequence name in the fasta file was used as query to PlutoF to find which SH at level 1.5 in release 8 the sequence belongs to, in order to generate the *.seq2sh.tsv files with sequence to SH matchings. Each SH was subsequently used as query to PlutoF to extract the complete taxonomy for the SH, stored in the *.SHs.tax files.
Two python scripts for automatic querying and generation of the files can be found in the `scripts` folder in the GitHub repo: `https://github.com/biodiversitydata-se/unite-shinfo`. See the accompanying README file for usage information.


## References

Abarenkov, Kessy; Zirk, Allan; Piirmann, Timo; Pöhönen, Raivo; Ivanov, Filipp; Nilsson, R. Henrik; Kõljalg, Urmas (2020): UNITE general FASTA release for Fungi. Version 04.02.2020. UNITE Community. https://doi.org/10.15156/BIO/786368

Abarenkov, Kessy; Zirk, Allan; Piirmann, Timo; Pöhönen, Raivo; Ivanov, Filipp; Nilsson, R. Henrik; Kõljalg, Urmas (2021): UNITE general FASTA release for Fungi. Version 10.05.2021. UNITE Community. https://doi.org/10.15156/BIO/1280049

Straub, Daniel, Nia Blackwell, Adrian Langarica-Fuentes, Alexander Peltzer, Sven Nahnsen, and Sara Kleindienst. 2020. “Interpretations of Environmental Microbial Community Studies Are Biased by the Selected 16S RRNA (Gene) Amplicon Sequencing Pipeline.” Frontiers in Microbiology 11. https://doi.org/10.3389/fmicb.2020.550420.

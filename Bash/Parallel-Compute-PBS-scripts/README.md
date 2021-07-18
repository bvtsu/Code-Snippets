# Usage

This identifies HSE motifs in either UCSC or CGP genome browser genomes using a regular expression search for the degenerate HSE motif, NGAANNTTCNNGAAN

```./submit_parallel_motif_search.sh```

To run this example test, you must have downloaded the associated genome files listed in the Example-input/CGP_planfile_full.txt.

To side-step this, implement a wget line within the .sh file to correspond to each input genome name, pointed to either the UCSC genome browser FTP server or the CGP genome browser download server.

# Caenorhabditis-HSE-Helitrons project
The full development of HSE-Helitron overlap analyses by bvtsu for Garrigues et al., 2019 is under construction in the affiliated Daugherty Lab organization repo.
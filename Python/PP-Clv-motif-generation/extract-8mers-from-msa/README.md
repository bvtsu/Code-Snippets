# Usage

Identifies the 8mer polyprotein cleavage site window for every seq in a polyprotein MSA .aln by referencing the original fasta to fill in gaps  -- currently hardcoded, but can be altered.

```python extract-8mers.py Example-input/combined.fasta.aln Example-input/combined.fasta```

## Example stdout

### If this is working correctly, picks up the reference 8mer cleavage sites from NP_047200 at the end of each shown sliding window (excluding gaps)
Found LQRQGNSV at 309 : 369
-----------AGALTQLLN-F-----PSTPPLT----LP--T-------TNLQRQGNSV 

Found LAPQHWKT at 814 : 874
PWTFYLQVLSPLNPPPSLPTSLSCSIYVTPVDSSFHGLRYLA--------PQ---HW-KT 

Found LTSQTLTE at 1049 : 1109
NPDALLSTTGYVSIWVQNPLVGPHTAPASALVQAFISAGESFNVRLMQNPALTSQTL-TE 

Found IRRQGLLT at 1628 : 1688
GESLPNTGFSL--------ALG--IGALTAIAASAAVAVKALPG--------IRRQGLLT 

Found LEPQGLKD at 1890 : 1950
CADLAPHAREFFTASGNVLSSLYYWIASKLGLSVTPQE-CE----RATLEPQ----GLKD 

Found IRRQGNRV at 2293 : 2353
VSNSLASLIRR-------------QG-------------------------------NRV 

Found QEPQAAYS at 2426 : 2486
----------KYRKPIFTCTTFLAVLGFLCSV---IPLARSLWKSK--QDTPQEPQAAYS 

Found IQRQGISP at 2463 : 2523
LARSLWKSK--QDTPQEPQAAYSAISHQK-------PKP-KSQKPVPTRHIQRQG--ISP 

Found TTQQSLIV at 2664 : 2724
AATFEGLCGSPLVTDDPSGVKILGLHVAGVAGTSGFSAPIH-PILGQITQFATTQQSLIV 

### AA positions for each polyprotein cleavage site in the ref sequence NP_047200 
Positions of cleavage sites in the reference sequence
{'LQRQGNSV': [361, 362, 363, 364, 365, 366, 367, 368], 'LAPQHWKT': [854, 855, 864, 865, 869, 870, 872, 873], 'LTSQTLTE': [1100, 1101, 1102, 1103, 1104, 1105, 1107, 1108], 'IRRQGLLT': [1680, 1681, 1682, 1683, 1684, 1685, 1686, 1687], 'LEPQGLKD': [1938, 1939, 1940, 1941, 1946, 1947, 1948, 1949], 'IRRQGNRV': [2301, 2302, 2303, 2317, 2318, 2350, 2351, 2352], 'QEPQAAYS': [2478, 2479, 2480, 2481, 2482, 2483, 2484, 2485], 'IQRQGISP': [2513, 2514, 2515, 2516, 2517, 2520, 2521, 2522], 'TTQQSLIV': [2716, 2717, 2718, 2719, 2720, 2721, 2722, 2723]} 

### Cleanup report -- removing dupe sets, sets with missing 8mers, and sets with seq ambiguities
199 IDs before cleanup
162 IDs after removing missing cleavage sites
160 IDs after removing cleavage sites with uncertainty (X residues)
90 IDs after removing duplicate cleavage site sets

### Example dictionary output before writing to file
('SNQ28043', ['IVRQGNST', 'VQTQHWKI', 'FQLQAADD', 'IIRQGLLS', 'VEHQGVRD', 'VKRQGLTI', 'DKTQGAYS', 'VVRQSLSP', 'IDQQSIII'])

### Current output style
>sp|O91464
['LQRQGNSV', 'LAPQHWKT', 'LTSQTLTE', 'IRRQGLLT', 'LEPQGLKD', 'IRRQGNRV', 'QEPQAAYS', 'IQRQGISP', 'TTQQSLIV']
# Usage

To convert .txt output from Cytation5 version 3.10.06 platereader to matplotlib and seaborn plots.

```python check-linearity.py Example-input/20210321-WT-R40Wvsall3CL.txt Example-input/20210321-WT-R40W-test_batch.txt```

# Example batch inputs necessary for run - add number of condition tags to reflect number of conditions tested
#Filetag=filename prefix ("20210321-WT-R40W")
#Forced-Rsquared=value between 0 and 120, select time point rather than using the max (set "0" for default)
#Group-Separator=separator used to separate grouped conditions ("vs")
#Standard-Cols=columns containing the HEK-blue standards ("10,11")
#Condition=name of condition containing Group,separator, and condition ("WTvsEV")

# Example stdout
#Time point based off of -Rsquared.png plot for maximum linearity
Best timepoint: 20 min

#Slope and y-intercept based on selected timepoint std-linearity.png
Best Slope: 0.0032413669064748165 
Best Y-Intersect: 0.08972482014388491
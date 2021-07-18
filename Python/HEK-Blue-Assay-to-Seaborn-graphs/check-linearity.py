#!/usr/bin/env python
import sys
import pandas as pd
import re
import numpy as np
from numpy import genfromtxt,corrcoef,polyfit
import operator
import matplotlib.pyplot as plt
import seaborn as sns
import os

try:
    os.mkdir("outputs/")
except OSError:
    print("Creation of the directory %s failed, already exists")
else:
    print("Successfully created the output directory.")

#%matplotlib inline
#Interactive Mode: sys.argv[2] set as "interactive"
if sys.argv[2]=="interactive":
    print("Enter your title tag (e.g. today's date):")
    specified_date=input().replace(" ","-")#"20210304"
    print("Enter your conditions, comma-separated (e.g. Blank,WTvsEV,WTvsS2,WTvsS2*):")
    hek_blue_x_labels=input().replace(" ","").split(",")#["Blank","WTvsEV","WTvsS2","WTvsS2*","S39PvsEV","S39PvsS2","S39PvsS2*","R40WvsEV","R40WvsS2","R40WvsS2*"] #Manual for now, will automate later
    print(hek_blue_x_labels)
    abs_df_columnlocs=[]#[["C8","E8","G8"],["B2","D2","F2"],["B3","D3","F3"],["B4","D4","F4"],["C2","E2","G2"],["C3","E3","G3"],["C4","E4","G4"],["B5","D5","F5"],["B6","D6","F6"],["B7","D7","F7"]]
    for condition in hek_blue_x_labels:
        print("Enter the wells (e.g. C8, E8, G8) for {}:".format(condition))
        abs_df_columnlocs.append(input().replace(" ","").split(","))
    print(abs_df_columnlocs)
    print("Set cols to search for standards data, assuming plate row A and plate row H are empty (e.g. 10, 11):")
    subs=input().replace(" ","").split(",") #['10','11']
    print("What is your group separator?")
    group_sep=input()
else: #obtain from an external batch file
    hek_blue_x_labels=[]
    abs_df_columnlocs=[]
    specified_date=''
    with open(sys.argv[2],"r") as f:
        for lines in f.readlines():
            if lines.startswith("FileTag:"):
                specified_date=lines.strip().split(":")[1]
            elif lines.startswith("Standard-Cols:"):
                subs=lines.strip().split(":")[1].split(",")
            elif lines.startswith("Forced-Rsquared:"):
                forced_rsquared=int(lines.strip().split(":")[1])
            elif lines.startswith("Group-Separator:"):
                group_sep=lines.strip().split(":")[1]
            elif lines.startswith("Condition:"):
                hek_blue_x_labels.append(lines.strip().split(":")[1])
            else:
                abs_df_columnlocs.append(lines.strip().split(","))
print("FileTag:",specified_date)
print("Conditions:",hek_blue_x_labels)
print("Wells:",abs_df_columnlocs)
print("Standard Columns:",subs)


def generate_abs_table(file,headerskip_val,footerskip_val)->pd.DataFrame:
    with open(file,encoding='cp1252') as f:
        header_line = re.split('\t|\n',f.readlines()[headerskip_val-1])[0:-1]
    data = np.genfromtxt(file, encoding='cp1252', skip_header=headerskip_val, skip_footer=footerskip_val)
    pd_data=pd.DataFrame(data)
    pd_data.columns=header_line
    pd_data['Time']=[i*5 for i in range(0,pd_data.shape[0])]
    return(pd_data)

def Filter(string, substr): 
    return([substring for substring in string if any(sub in substring for sub in substr)])

def standard_r_squared(header_subset,pd_df,timepoint_val,X_values,plot_desired,which_color)->float:
    abs_y=[]
    for x in standard_header_positions:
        abs_y.append(pd_df[pd_df['Time']==timepoint_val][x].values[0])
    correlation_matrix = np.corrcoef(X_values, abs_y)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2
    if plot_desired=='yes':
        m, b = np.polyfit(X_values, abs_y, 1)
        plt.plot(X_values,abs_y,'o', label='{0}, Rsquared={1}'.format(timepoint_val,round(r_squared,4)), color=which_color)
        plt.plot(X_values, m*np.array(X_values) + b,color=which_color)
        return(m,b)
    elif plot_desired=='no':
        return(r_squared)
        
def sns_DataFrame(raw_abs_df,conditions,condition_locs,timepoint)->pd.DataFrame():
    plt_dict={}
    for x in range(0,len(conditions)):
        for i in range(0,len(condition_locs[0])):
            if len(plt_dict)>0:
                plt_dict["Group"].append(conditions[x].split(group_sep)[0])
                plt_dict["Conditions"].append(conditions[x])
                plt_dict["Absorbance"].append(raw_abs_df[raw_abs_df['Time']==timepoint][condition_locs[x][i]].values[0])
            else:
                plt_dict["Group"]=[conditions[x].split("vs")[0]]
                plt_dict["Conditions"]=[conditions[x]]
                plt_dict["Absorbance"]=[raw_abs_df[raw_abs_df['Time']==timepoint][condition_locs[x][i]].values[0]]
    return(pd.DataFrame(plt_dict))

#Make table of absorbance values at 96 wells across diff time points
abs_df = generate_abs_table(sys.argv[1],34,34) #sys.argv[1]

#Prepare set standard cols to search for standards data, again assuming plate row A and plate row H are empty
standard_header_positions=Filter(abs_df.columns,subs)[4:-2]
standards_X=[200,200,50,50,20,20,5,5,0,0]

#Store and plot all r-squared vals for each timepoint set of standards
r_squared_compilation={}
for timepoint in abs_df['Time']:
    r_squared_compilation[timepoint]=standard_r_squared(standard_header_positions,abs_df,timepoint,standards_X,'no',"None")
x_times, y_rsquared = zip(*r_squared_compilation.items()) # unpack a list of pairs into two tuples
plt.plot(x_times, y_rsquared)
plt.xlabel('Timepoint')
plt.ylabel('R-squared')
plt.savefig('outputs/{0}-Rsquared.png'.format(specified_date))
plt.close()

#Find timepoint with highest r-squared val
max_rsquared_time=max(r_squared_compilation.items(), key=operator.itemgetter(1))[0]
#print(max_rsquared_time)
if forced_rsquared!=0:
    max_rsquared_time=forced_rsquared
    print("Forcing best R-squared")
print(max_rsquared_time)
#Export matplotlib plot of the best fit line scatter
color = ['r', 'b', 'm']
if max_rsquared_time!=0:
    slope1,y_intersect1=standard_r_squared(standard_header_positions,abs_df,max_rsquared_time-5,standards_X,'yes',color[1])
slopebest,y_intersectbest=standard_r_squared(standard_header_positions,abs_df,max_rsquared_time,standards_X,'yes',color[0])
if max_rsquared_time!=120:
    slope2,y_intersect2=standard_r_squared(standard_header_positions,abs_df,max_rsquared_time+5,standards_X,'yes',color[2])
plt.legend(title="Time (min)",loc="upper left")
plt.xlabel('Standard (pg/ml)')
plt.ylabel('Absorbance (655)')
plt.savefig('outputs/{0}-std-linearity-timepoint-{1}min.png'.format(specified_date,max_rsquared_time))
plt.close()
print("Best timepoint:",max_rsquared_time,"min\nBest Slope:",slopebest,"\nBest Y-Intersect:",y_intersectbest)

#Set colors, hardcoded
colorblind=["#CC79A7", "#0072B2", "#009E73", "#F0E442", "#56B4E9","#D55E00"]

#Plot Seaborn barplot with sd error bars along with an swarm plot overplay
plt_df=sns_DataFrame(abs_df,hek_blue_x_labels,abs_df_columnlocs,max_rsquared_time)
plt_df["Abs_to_pg/ml"]=(plt_df["Absorbance"]-y_intersectbest)/slopebest
plt_df["Supernatant IL-1B (ng/ml)"]=plt_df["Abs_to_pg/ml"]*20/1000
sns.set_style("ticks")
ax=sns.barplot(x="Conditions",y="Supernatant IL-1B (ng/ml)",data=plt_df,capsize=.1,errwidth=1,ci="sd",hue="Group",palette=colorblind,dodge=False)
ax.set_xticklabels(ax.get_xticklabels(),rotation=30,ha="right")
sns.swarmplot(x="Conditions",y="Supernatant IL-1B (ng/ml)",data=plt_df,alpha=0.5,color='black')
ax.yaxis.grid(True)
plt.tight_layout()
plt.savefig('outputs/{0}supernatant-IL-1B-timepoint-{1}min.png'.format(specified_date,max_rsquared_time),dpi=600)
plt.close()
plt_df.to_csv('outputs/{0}supernatant-IL-1B-timepoint-{1}min.csv'.format(specified_date,max_rsquared_time), index=False)
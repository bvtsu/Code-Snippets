# library & dataset
import seaborn as sns
import sys
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(sys.argv[1])
GOterm=str(sys.argv[3])

df_subset = df[df["GOBiologicalProcess"].str.contains(GOterm)]
df_subset['Label']=GOterm

# plot
sns_plot=sns.violinplot(x=df_subset[sys.argv[2]], y=df_subset['Label'])
plt.title('{} {}'.format(GOterm,sys.argv[2]))
sns_plot.figure.savefig('outputs/{}_{}.png'.format(GOterm,sys.argv[2]))
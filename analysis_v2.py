import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math
import os

#cleaned up Yougov UK data from pdf using the Tabula GUI app.  
#if a larger number of source files were involved I would automate this (or beg YouGov UK for csv files to begin with

df=pd.read_csv('tabula-NFUResults_Veganism_UK_170410_Extra_W.csv')
df_i=df.set_index('Category')

column_groups = {
        'brexit' : ['Remain', 'Leave'],
        '2015' : ['Con', 'Lab', 'Lib Dem', 'UKIP'],
        'gender' : ['Male', 'Female'],
        'age' : ['18-24', '25-49', '50-64', '65+'],
        'social' : ['ABC1', 'C2DE'],
        'geography' : ['London','Rest of South', 'Midlands/Wales', 'North', 'Scotland', 'Northern Ireland']
}

row_groups = {
        'habits' : slice(3,7),
        'vegan ad' : slice(8,10),
        'vegan likely' : [13, 16, 17],
#       'vegan likely' : [11, 12, 14, 15, 17], #this is the higher-resolution data, excluded for small sample size issues
        'vegan ad likely' : [21, 24, 25],
#       'vegan ad likely' : [19, 20, 22, 23, 25], #this is the higher-resolution data, excluded for small sample size issues
        'less meat' : slice(27, 31),
        'less milk' : slice(32, 36),
        'less other dairy' : slice(37, 41),
        'less future' : [44, 45, 48, 49]
#       'less future' : [42, 43, 45, 46, 47, 49] #this is the higher-resolution data, excluded for small sample size issues
}

subtables = {}

for cg_name, cg_columns in column_groups.items():
        cols = df_i[cg_columns]
        for rg_name, rg_slice in row_groups.items():
                subtables[(cg_name, rg_name)] = cols.iloc[rg_slice]


ind_i=0
ind_j=0

os.mkdir('plots/')

for i in row_groups:
        fig, axes=plt.subplots(2,3,  figsize=(2,2))

        for j in column_groups:
                st=subtables[j, i]
                st_t=st.transpose()


                if  j=='gender':
                        st_t.plot.bar(stacked="True", rot=0, title=j, ax=axes[math.floor(ind_i/3), ind_j%3], colormap='Blues').legend(loc='center left',bbox_to_anchor=(1.0, 0.5), fontsize=8)
                elif j=='geography':
                        st_t.plot.bar(stacked="True", rot=45, title=j, ax=axes[math.floor(ind_i/3), ind_j%3], colormap='Blues', legend=None, fontsize=8)
                else:
                        st_t.plot.bar(stacked="True", rot=0, title=j, ax=axes[math.floor(ind_i/3), ind_j%3], colormap='Blues', legend=None)

                ind_i=ind_i+1
                ind_j=ind_j+1

                fig.suptitle(i)
                fig.legend(loc='center left',bbox_to_anchor=(1.0, 0.5))

                fig.subplots_adjust(right=0.8)

        fig = plt.gcf()
        fig.set_size_inches((11, 8.5), forward=False)
        fig.savefig('plots/' + i +'.pdf', format='pdf', dpi=500)

        ind_i=0
        ind_j=0
plt.show()


#!/users/bin/env/Python

"""@Author: Samson Jacob
    #Purpose: brief code to answer the questions in the assignment & generate PMF
    """


import pandas as pd
import matplotlib.pyplot as plt

#read in file
cl_DF = pd.read_csv('cota_ds_analyst_dataset_Jacob_Samson.csv')

#1.	How many patients have a therapy type of ‘metastatic’ and stage IV (includes IVa,b,c etc..)?
grp = cl_DF.groupby(['stage', 'therapy_type'])['therapy_type'].agg({"Frequencey": "count"})


#2.	How many patients have colon cancer, with stage III (include IIIa,b,c.. etc) and therapy type of ‘adjuvant’?
grp2=cl_DF.groupby(['rectal_or_colon_ca','stage', 'therapy_type'])['therapy_type'].agg({"Frequencey": "count"})

#3	What proportion of patients have rectal cancer?

rect=cl_DF.loc[cl_DF['rectal_or_colon_ca']=='rectal']
rect.shape

# What is the probability mass function of lymph_nodes_removed?
lymph=cl_DF.lymph_nodes_removed.value_counts().sort_index()/1000 #shape of original doc
ax=lymph.plot(kind='bar',title='Lymph_Nodes_Removed_PMF')
ax.set_xlabel("bin")
ax.set_ylabel("Freq")
plt.tight_layout()
plt.savefig('lymph.png')
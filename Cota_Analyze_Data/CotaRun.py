#!/users/bin/env/Python

"""@Author: Samson Jacob
    #Purpose: Clean Cota_ds_analyst.csv generate cleaned file using
    deus (aux_dataset.xlsx)

    """

#load back-end scripts

from Cota_Parse import *
from Cota_Deus import *

if __name__ == '__main__':


    # hardwired filepaths
    dataset = './cota_ds_analyst_dataset.csv'
    deuspth = './aux_dataset.xlsx'

    #create merged deus dataframe
    concat_Deus = concat_excel_samples(deuspth)

    #read in the csv
    DF = pd.read_csv(dataset)

    # convert to date time
    DF = convert_col_todatetime(DF,'date_of_birth')

    #convert to int
    DF= convert_col_to_int(DF,'lymph_nodes_removed')

    # apply the corrections for the columns from the deus
    ColumnsToClean = read_sheets_tolis(deuspth)

    for col in ColumnsToClean:
            if col == 'rectal_or_colon_ca':
                DF[col]=DF[col].replace({'Rectal':'rectal'})
                DF=apply_deus_to_col(DF,concat_Deus,col,np.nan)
            if col == 'braf_mutation':
                DF = apply_deus_to_col(DF,concat_Deus,col,np.nan)

    #filter braf
    DF['braf_mutation'] = DF['braf_mutation'].map({'True': True, 'FALSE': False, False: False}).fillna(np.nan)

    # find the rows that explicitly says adjuvant, neoadjuvant and metastatic not sure about 'ad' as adjuvant
    DF['therapy_type'] = DF.therapy_type.str.extract('({})'.format('|'.join(['metastatic', 'adjuvant', 'neoadjuvant'])),expand=False)

    #fix resection column
    DF['resection']=DF.resection.apply(find_val).apply(lambda x: "%s"%','.join(x)).replace('',np.nan)

    #fix Patient preferance column
    DF=fix_spaces_in_col(DF,'patient_preference','(')
    DF['patient_preference'] = DF['patient_preference'].map({'yes': True, 'no': False}).fillna(np.nan)

    #fix histological grade (likely 1 = g1 etc)
    DF['histological_grade']=DF['histological_grade'].replace({"4":'g4', "3": "g3", "2": "g2", "1": "g1"})

    #clean stage column
    DF['stage']=DF.loc[(DF.stage.str.contains('i')) & (~DF.stage.str.contains('pathologic')) & (~DF.stage.str.contains('no'))].stage.str.replace('stage','')
    DF['stage']=DF['stage'].str.split()

    #final
    final = parse_final_df(DF)
    DF.to_csv('cota_ds_analyst_dataset_Jacob_Samson.csv',na_rep=np.nan)
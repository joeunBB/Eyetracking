# -*- coding: utf-8 -*-
"""
Created on Fri May 16 14:42:49 2025

@author: maeva
"""

from os import listdir
from os.path import isfile, join
import pandas as pd
import re



def colonnes_entierement_vides(df: pd.DataFrame) -> list:
    """
    Retourne la liste des noms de colonnes dont toutes les valeurs sont NaN.
    """
    return df.columns[df.isna().all()].tolist()


def get_value_per_AOI(df_test) :
    """ retourne les valeurs depuis un dataframe"""
    y = []
    for col in df_test.columns:
        x = [i for i in list(set(df_test["{}".format(col)].tolist())) if str(i)!='nan']
        y.append(x)
            
    return y

def get_item_from_col(col_name):
    """ prend le numero d'item à partir du nom de la colonne"""
    pattern = "(\d_\d{1,2}\w\w)"
    x = re.search(pattern, col_name) #check if pattern in col
    if x:
        return x.group(1)
    else:
        return "non"

def get_type_fixation(col_name):
    """ prend le type de fixation à partir du nom de la colonne"""
    pattern = "(.*)\d_\d{1,2}\w\w"
    x = re.search(pattern, col_name) #check if pattern in col
    if x:
        return x.group(1)
    else:
        return "non"

def get_AOI(col_name):
    """ prend le nom de l'AOI à partir du nom de la colonne"""

    pattern = "\d_\d{1,2}\w\w_(.*)"
    x = re.search(pattern, col_name) #check if pattern in col
    if x:
        return x.group(1)
    else:
        return "non"

def get_order_in_timeline(item, file):
    """ prend le num de l'item dans la timeline (lordre de présentation) 
    à partir du numéro d'item et du fichier .csv"""

    pattern = "\d_(\d{1,2}\w\w)"
    id_ = re.search(pattern, item)
    if id_ : 
        id_ = id_.group(1) #check if pattern in col
    else:
        return item
    df_file = pd.read_csv("{}".format(file), sep=",")
    index = df_file.index[df_file['id'] == "{}".format(id_.lower())].tolist()
    return index

def create_df_from_data(data):
    def extract_item(x):
        pattern = "\d_(\d{1,2})(\w\w)"
        match = re.match(pattern, x)
        return match.group(1)
    def extract_cond(x):
        pattern = "\d_(\d{1,2})(\w\w)"
        match = re.match(pattern, x)
        return match.group(2)
    df = pd.DataFrame(data)
    df = df.iloc[8:] #supprimer les rangs inutiles
    
        # Step 1: Flatten list columns
    df['value'] = df['value'].apply(lambda x: x[0] if isinstance(x, list) else x)
    df['timeline_order'] = df['timeline_order'].apply(lambda x: x[0] if isinstance(x, list) else x)
    
    # Step 2: Pivot table
    df_pivot = df.pivot_table(
        index=['item', 'AOI', 'timeline_order'],
        columns='type_fixation',
        values='value'
    ).reset_index()
    
    df_pivot = df_pivot.rename_axis(None, axis=1)
    
    # Reorder manually if needed
    desired_order = ['item', 'Total_duration_of_whole_fixations.',
                     'Average_duration_of_whole_fixations.',
                     'Number_of_whole_fixations.', 'AOI', 'timeline_order']
    
    df_pivot = df_pivot[desired_order]

   # df_pivot['condition'] = df_pivot['item'].apply(lambda x: re.match('\w\w', x))
    df_pivot['numero_item'] = df_pivot['item'].apply(lambda x: extract_item(x))
    df_pivot['condition'] = df_pivot['item'].apply(lambda x: extract_cond(x))
    return df_pivot





#prendre le dossier avec les fichiers .tsv de résultats
mypath = "C:\Users\iuiui\Downloads\eyetracking\"

#tous les extraire dans des dataframes
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
all_dfs = [pd.read_csv('{}{}'.format(mypath, x), sep="\t") for x in onlyfiles]


#essai avec un dataframe
df_test = all_dfs[0]

#enlever les colonnes vides (car dans d'autres timelines, non concerné)
df_test = df_test.drop(columns=colonnes_entierement_vides(df_test)) 

#enlever les colonnes vides (car dans d'autres timelines, non concerné)
y = get_value_per_AOI(df_test) 

#récupérer toutes les valeurs, et vérifier que ça marche
#parler de l'avantage d'avoir nommé les AOI de cette façon pour l'exploitation des données, comme dans ce programme, 
# qui a récupéré toutes les informations à partir du nom de l'AOI
for val, col in zip(y, df_test.columns):
    print(val, col)
    print(f'{val} -> {col}', "-> {}".format(get_item_from_col(col)) , "-> {}".format(get_type_fixation(col)), "-> {}".format(get_AOI(col)),
          "-> {}".format(get_order_in_timeline(col, "C:\Users\iuiui\Downloads\eyetracking\STIMULI_expe40.csv_2.csv")),)



#créer un dictionnaire pour reprendre toutes les informations
data = []

y = get_value_per_AOI(df_test)
for val, col in zip(y, df_test.columns):
    row = {
        'value': val,
        'column': col,
        'item': get_item_from_col(col),
        'type_fixation': get_type_fixation(col),
        'AOI': get_AOI(col),
        'timeline_order': get_order_in_timeline(col, "C:\Users\iuiui\Downloads\eyetracking\STIMULI_expe40.csv_2.csv")
    }
    data.append(row)

# convertir le dictionnaire dans un dataframe
df_result = create_df_from_data(data)

#enregistrer le dataframe final
df_result.to_csv("C:\Users\iuiui\Downloads\eyetracking\result_{}.csv".format(str(onlyfiles[0]).replace('.tsv', '')), index=False)




for x in df_test.columns:
    if "1_18" in x : 
        print(x)

from collections import Counter
print(Counter(df_test['Total_duration_of_whole_fixations.0_11PT_C'].tolist()))
print(Counter(df_test['Number_of_whole_fixations.0_11PT_POSTC'].tolist()))
print(Counter(df_test['Number_of_whole_fixations.1_18PT_C'].tolist()))

































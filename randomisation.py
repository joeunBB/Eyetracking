# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 12:28:26 2025

@author: Joeun
"""

import argparse
from pathlib import Path
import pandas as pd
import random

def process_file(input_path: Path):
    """
    Traite le fichier d'entrée et écrit le résultat dans le fichier de sortie.
    """
    
    fichier_in = pd.read_csv('{}'.format(input_path), sep=',')  #ouverture fichier
    
    list_rows = []
    
    nb_expe = int(len(fichier_in[fichier_in[' type'] == 'expérimental'][' type'].tolist())/2)
    
    for x in range(1,nb_expe+1):
      famille_rows = fichier_in[fichier_in["Famille"] == str(x)]
    
      pt_row = famille_rows[famille_rows["Condition"] == "pt"]
      qm_row = famille_rows[famille_rows["Condition"] == "qm"]
    
      list_rows.append(random.choice([pt_row, qm_row]))
      all_rows_df = pd.concat(list_rows)
    
      PT_row = all_rows_df[all_rows_df["Condition"] == "pt"]
      QM_row = all_rows_df[all_rows_df["Condition"] == "qm"]
    
      if len(PT_row) != len(QM_row) and len(PT_row) < len(QM_row):
          list_rows.pop()
          list_rows.append(pt_row)
    
      if len(PT_row) > len(QM_row) and len(PT_row) != len(QM_row):
          list_rows.pop()
          list_rows.append(qm_row)
    
    new = pd.concat(list_rows)
    new = new.reset_index(drop=True)

    new_shuffled_index = list(new.index)
    random.shuffle(new_shuffled_index)
    new = new.iloc[new_shuffled_index]
        
    filler_rows = fichier_in[fichier_in[' type'] == 'FILLER'].sample(frac=1).reset_index(drop=True)
    
    final_rows = []
    insert_index = 2
    exp_count = 0
    filler_index = 0
    
    for index, row in new.iterrows():
        final_rows.append(row)
        exp_count += 1
    
        if exp_count % insert_index == 0 and filler_index < len(filler_rows):
            final_rows.append(filler_rows.iloc[filler_index])
            filler_index += 1
    
    # Continuer à insérer les fillers s’il en reste
    while filler_index < len(filler_rows):
        final_rows.append(filler_rows.iloc[filler_index])
        filler_index += 1
    
    fichier_mod = pd.DataFrame(final_rows)

    
    script = fichier_mod[[col for col in fichier_mod.columns if col in ("ContextePrompt", "Cible","Continuation", "Question", "Famille", " type", "Condition")]]

    all_ = [True if x in [11, 21, 31, 41, 51, 61, 71, 81, 91] else False for x in range(len(script))]
    script['test'] = all_
    
    def return_question(value_, question):
      if value_ == True:
        return question
    
    script['Question'] = script.apply(lambda x :return_question(x['test'], x['Question']), axis=1)
    
    return script


def main():
    parser = argparse.ArgumentParser(description="Traitement du fichier .csv pour la randomisation des stimuli.")
    parser.add_argument("input_file", type=Path, help="Chemin du fichier d'entrée")

    args = parser.parse_args()
    input_path = args.input_file
    
    for i in range(40):
       df =  process_file(input_path)
       output_path = str(input_path).replace(".csv", "")
       df[["ContextePrompt", "Cible","Continuation", "Question", "Famille", " type", "Condition"]].to_csv('{}_{}.csv'.format(input_path, i), sep=',', index=False)

if __name__ == "__main__":
    main()

#pour utiliser le code : python randomisation.py mon_fichier.csv (enregistre les 40 timelines)

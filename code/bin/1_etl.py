# LIBRARIES
import os
import sys
import json
from glob import glob
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# CUSTOM IMPORTS
# IMPORT ALL DATA TREATMENT CLASSES
script_directory = os.path.dirname( __file__ )
module_directory = os.path.join(script_dir, '..', 'lib')
sys.path.append(module_directory)
from 1_etl import DataTreatment, FeatureEngineering


# DEFINE THE METADATA COLUMNS
# The metadata column for every system
metadata_columns = ['id']

# For system 1
metadata_items = ["tipo", "declaracionCompleta",
                  "actualizacionConflictoInteres", "actualizacion",
                  "institucion"]
declaracion_items = ["nombre", "primerApellido", "segundoApellido",
                     "correoElectronico_institucional"]

metadata_columns += ['metadata_'+item for item in metadata_items]
metadata_columns += ['declaracion_situacionPatrimonial_datosGenerales_'+item for item in declaracion_items]

# For system 2
metadata_columns += declaracion_items

# For system 3s
servidor_items = ["nombres", "primerApellido", "segundoApellido",
                  "genero_clave", "genero_valor"]

metadata_columns += ["fechaCaptura", "expediente", "fechaCaptura", "expediente"]
metadata_columns += ['servidorPublicoSancionado_'+item for item in servidor_items]

# The unique build for ids in each system (at least in this exercise, without CURP)

# For system 1, it will be the full name plus the delcaring institution plus estado_declarante 
declaracion_items = ["nombre", "primerApellido", "segundoApellido"]
s1_id = ['declaracion_situacionPatrimonial_datosGenerales_'+item for item in declaracion_items]
s1_id += ['estado_declarante', 'metadata_institucion']

# For system 2, it will be similar
s2_id = ["nombres", "primerApellido", "segundoApellido"]
s2_id += ['estado_declarante', 'institucionDependencia_siglas']

# For system 3, it is only the full name and estado_declarante because there's
# no info about the institution the server works for
servidor_items = ["nombres", "primerApellido", "segundoApellido"]

s3s_id = ['servidorPublicoSancionado_'+item for item in servidor_items]
s3s_id += ['estado_declarante']

# Put every list into a single dictionary
systems_id_dictionary = {'s1': s1_id, 's2': s2_id, 's3s': s3s_id}

# The column with the date to sort by in order to group data
grouping_date_dictionary = {'s1': 'metadata_actualizacion', 's2': 'fechaCaptura', 's3s': 'fechaCaptura', 's3p': 'fechaCaptura'}

def main():
  for system in ['s1', 's2', 's3s', 's3p']:
    if system=='s1':
      etl = FeatureEngineering(pdn_system=system, root_path='/content/drive/MyDrive/Dataton_2022/pruebas/',
                           metadata_columns=metadata_columns)

      # Initial extraction and normalization
      etl.extractData('ext_data')

      # Define the unique id of each servant
      etl.defineId(systems_id_dictionary[system], 'ext_data', 'ext_data')

      etl.normalizeData('ext_data', 'norm_data_inter_1')
      etl.normalizeData('norm_data_inter_1', 'norm_data_inter_2')
      etl.normalizeData('norm_data_inter_2', 'norm_data_1')

      # Treat all missing data
      etl.missingData(0, 'norm_data_1', 'miss_data_1')

      # Save this untokenized ungrouped data
      etl.last_data.to_csv('/content/drive/MyDrive/Dataton_2022/pruebas/'+system+'/ut_ug_m_data.csv', index=False)

      # Group the historic data
      etl.groupData('miss_data_1', 'group_data_1')

      # Save this untokenized grouped data
      etl.last_data.to_csv('/content/drive/MyDrive/Dataton_2022/pruebas/'+system+'/ut_g_um_data.csv', index=False)

      # Missing treatment for new NaNs (it has a different missing input because the origin is different)
      etl.missingData(-1, 'group_data_1', 'miss_data_2')

      # Save this untokenized grouped data
      etl.last_data.to_csv('/content/drive/MyDrive/Dataton_2022/pruebas/'+system+'/ut_g_m_data.csv', index=False)


      # Tokenize the text data and then normalize the newly created vectors
      etl.tokenizeData(True, 'miss_data_1', 'tok_data')
      etl.normalizeData('tok_data', 'norm_data_2')
      etl.missingData(0, 'norm_data_2', 'miss_data_3')

      # Save this tokenized ungrouped data
      etl.last_data.to_csv('/content/drive/MyDrive/Dataton_2022/pruebas/'+system+'/t_ug_m_data.csv', index=False)

    else:
      etl = FeatureEngineering(pdn_system=system, root_path='/content/drive/MyDrive/Dataton_2022/pruebas/',
                           metadata_columns=metadata_columns)

      # Initial extraction and normalization
      etl.extractData('ext_data')

      # Define the unique id of each servant
      etl.defineId(systems_id_dictionary[system], 'ext_data', 'ext_data')

      etl.normalizeData('ext_data', 'norm_data_inter_1')
      etl.normalizeData('norm_data_inter_1', 'norm_data_inter_2')
      etl.normalizeData('norm_data_inter_2', 'norm_data_1')

      # Treat all missing data
      etl.missingData(0, 'norm_data_1', 'miss_data_1')

      # Save this untokenized ungrouped data
      etl.last_data.to_csv('/content/drive/MyDrive/Dataton_2022/pruebas/'+system+'/ut_ug_m_data.csv', index=False)

      # Tokenize the text data and then normalize the newly created vectors
      etl.tokenizeData(True, 'miss_data_1', 'tok_data')
      etl.normalizeData('tok_data', 'norm_data_2')
      etl.missingData(0, 'norm_data_2', 'miss_data_3')

      # Save this tokenized ungrouped data
      etl.last_data.to_csv('/content/drive/MyDrive/Dataton_2022/pruebas/'+system+'/t_ug_m_data.csv', index=False)
    
    with open('/content/drive/MyDrive/Dataton_2022/pruebas/'+system+'/etl.pkl') as f:
      pickle.dump(etl, f)

if __name__=='__main__':
  main()

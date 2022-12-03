# LIBRARIES
import os
import json
from glob import glob
import pandas as pd

# CUSTOM IMPORTS
# IMPORT ALL DATAT TREATMENT CLASSES

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

def main():
  # For System 1
  etl = FeatureEngineering(pdn_system='s1', root_path='/content/drive/MyDrive/Dataton_2022/pruebas/',
                         metadata_columns=metadata_columns)

  # Initial extraction and normalization
  etl.extractData('ext_data')
  
  # Iterate over multiple normalization
  etl.normalizeData('ext_data', 'norm_data_inter_1')
  etl.normalizeData('norm_data_inter_1', 'norm_data_inter_2')
  etl.normalizeData('norm_data_inter_2', 'norm_data_1')
  
  # Tokenize the text data and then normalize the newly created vectors
  etl.tokenizeData('norm_data_1', 'tok_data')
  etl.normalizeData('tok_data', 'norm_data_2')
  
  # Treat all missing data
  etl.missingData('norm_data_2', 'miss_data')
  
  # Group the historic data
  etl.groupData('miss_data', 'group_data')

if '__name__'==main():
  main()

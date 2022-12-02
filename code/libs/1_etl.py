class DataTreatment:
  def __init__(self, pdn_system:str, root_path:str) -> None:
    '''
      This object recieves the root path where all systems data is located
      as well as the PDN system, the it is able to append multiple paths into
      a single dataset.

      Parameters:
        root_path (str): The main location where every system data library is
        pdn_system (str): The PDN system you wish to work with:
                            's1', 's2', 's3p' or 's3s'
    '''
    # TODO: ADD A FUNCTIONALITY TO ALSO READ URLS

    # Define the system
    if type(pdn_system)==str:
      if pdn_system in ['s1', 's2', 's3p', 's3s']:
        self.pdn_system = pdn_system
      else:
        raise TypeError('Error on __init__ method:   Only values allowed for pdn_system are "s1", "s2", "s3p" or "s3s"')
    else:
      raise TypeError('Error on __init__ method:   Only string type is allowed for pdn_system')
    
    # Define the root path
    if type(root_path)==str:
      self.root_path = root_path
    else:
      raise TypeError('Error on __init__ method:   Only string type is allowed for root_path')

    return None
  
  # PRIVATE METHODS
  def _getPaths(self, main_path:str) -> list:
    return glob(main_path, '*', recursive=False)

  def _readJson(self, path:str) -> dict:
    with open(path, 'r') as f:
      dictionary = json.load(f)
    return dictionary
  
  def _normalizeStateName(self, string:str) -> str:
    return string.replace('SESNA', '').replace('_','').replace(' ', '').lower()
  
  def _flattenDictionary(self, dictionary:dict, separator:str='_', prefix:str='') -> dict:
    # Source: https://www.geeksforgeeks.org/python-convert-nested-dictionary-into-flattened-dictionary/
    return { prefix + separator + k if prefix else k : v
            for kk, vv in dictionary.items()
            for k, v in self._flattenDictionary(vv, separator, kk).items()
          } if isinstance(dictionary, dict) else { prefix : dictionary }
  
  def _flattenStatesData(self, state_paths:list) -> pd.DataFrame:
    # TODO: REFACTOR AND MODULARIZE THIS CODE
    normalized_data = pd.DataFrame({})
    
    for state_path in state_paths:
      # Get the state name and normalize it
      state = self._normalizeStateName(state_path.split('/')[-1])

      # Get every data file on the state
      single_files = self._getPaths(state_path)
      state_list = []
      for single_file in single_files:
        # Read the json as a dictionary
        dictionary_file = self._readJson(single_file)

        # Flatten the dictionary
        flatten_dictionary = self._flattenDictionary(dictionary_file)

        # Add the flattened dictionary to the list of every file in the state
        state_list.append(flatten_dictionary)
      
      # Normalize the state data
      state_data = pd.DataFrame(state_list)
      state_data['estado'] = state
      normalized_data.append(state_data, ignore_index=True)

      return normalized_data
  
  def _tokenizeData(self):
    pass
  
  def _missingTreatment(self):
    pass

  # PUBLIC METHODS
  def extractData(self) -> None:
    # The main path of the PDN system
    system_root_path = os.path.join(self.root_path, self.pdn_system)

    # The list of every state on the PDN system
    state_paths = self._getPaths(system_root_path)

    # Flatten all the states' data and append it into a single dataframe
    self.flattened_data = self._flattenStatesData(state_paths)
    self.last_data = self.flattened_data

    return None
  
  def normalizeData(self) -> None:
    # This method extends every element  with a list within the dataframe 
    # into multiple columns in the same dataframe
    self.normalized_data = self._normalizeData()
    self.last_data = self.normalized_data

    return None

  def missingData(self) -> None:
    # This method turns all missing data into a value
    self.no_missing_data = self._missingTreatment()
    self.last_data = self.no_missing_data

    return None
 
class FeatureEngineering(DataTreatment):
  # PRIVATE METHODS
  
  # PUBLIC METHODS
  def tokenizeData(self) -> None:
    # This method tokenizes text data based on the bag of words of each column
    return None
  
  def groupData(self) -> None:
    # This method groups data into multiple features
    return None

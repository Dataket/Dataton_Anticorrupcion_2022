# TODO: WORK ON OTHER FEATURE SELECTION METHODS
class FeatureSelection:
  def __init__(self, root_path:str, dataset_name:str) -> None:
    pass
  
  def dropConstantFeatures(self) -> None:
    pass
  
class AnomalyDetection(FeatureSelection):
  
  # These ones define a model, an instance variable to which one can use method fit and predict
  def anomalyBenchmark(self, load_path:str=None) -> None:
    pass
  def anomalyChallenger(self, load_path:str=None) -> None:
    pass
  
class NetworkDetection(AnomalyDetection):
  # La network detection va a funconar a nivel institución en el caso del sistema 1+sistema 1
  #   va a funcionar a nivel estado en el caso del sistema 1+sistema 3 asímismo
  #   hay un boost al peso del nodo si id_sistema1 = id_sistema2 (a nivel dependencia+estado) o id_sistema2=id_sistema_3 (a nivel estado)

class DataQuality:
    def __init__ (self, csv_file):
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        self.df = pd.read_csv(f"./{csv_file}")
        
    def analise_numerica(self): # Analisando as colunas numericas
        return self.df.describe()
    
    def contagem_nulos(self): # Exibe a contagem dos valores nulos por coluna
        return self.df.isnull().sum()
    
    def valores_unicos(self): # Exibindo a contagem dos valores unicos por coluna
        return self.df.nunique()
    
    #def descricao(self, *args=df.columns):
        #df[[args]].describe()
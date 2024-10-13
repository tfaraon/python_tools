import pandas as pd
import Xbeach_reader as XBr

def read_SAMAT_data(chemin, start_date= '2005-11-24 00:00', end_date= '2005-11-26 23:00'): 
    #Chargement de la donnée SAMAT
    SAMAT_data_raw = pd.read_csv(chemin, 
                             decimal= ',', 
                             sep = '.', 
                             date_parser = True)
        
    #Mise en forme des dates
    SAMAT_data_raw['Date'] = pd.to_datetime(SAMAT_data_raw['Date'], dayfirst=True)
    mask = (SAMAT_data_raw['Date'] >= start_date) & (SAMAT_data_raw['Date'] <= end_date)
    
    #Extraction dans les dates
    SAMAT_data = SAMAT_data_raw.loc[mask]
    
    return SAMAT_data 

def extract_var_point(file, variable_to_get, point, start_date):
    data_set = XBr.XB_Loader(file)
    XB_variable = pd.DataFrame() #Mise en forme pratique des résultats de XB pour le plt
    XB_variable[f'{variable_to_get}'] = data_set.get_variable(variable_to_get)[:,0,point].astype(float) #Récupération de la colonne Hs
    XB_variable['time'] = data_set.time.data #Récupération du vecteur temps
    
    #Conversion du temps (s) en date avec un pas minute
    XB_variable['DateTime'] = XBr.secondes_vers_temps(XB_variable['time'], start_date,'%Y-%m-%d %H:%M')
    XB_variable.set_index('DateTime', inplace=True)
    XB_variable = XB_variable.resample('1T').mean().reset_index()
    XB_variable['DateTime']= pd.to_datetime(XB_variable['DateTime'], dayfirst=True)

    return XB_variable


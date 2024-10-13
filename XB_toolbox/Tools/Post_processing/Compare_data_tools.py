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

def extract_hs_point(file, point, start_date):
    dataset = XBr.XB_Loader(file)
    XB_Hs = pd.DataFrame() #Mise en forme pratique des résultats de XB pour le plt
    XB_Hs['Hs'] = dataset.H[:,0,point].astype(float) #Récupération de la colonne Hs
    XB_Hs['time'] = dataset.time.data #Récupération du vecteur temps
    
    #Conversion du temps (s) en date avec un pas minute
    XB_Hs['DateTime'] = XBr.secondes_vers_temps(XB_Hs['time'], start_date,'%Y-%m-%d %H:%M')
    XB_Hs.set_index('DateTime', inplace=True)
    XB_Hs = XB_Hs.resample('1T').mean().reset_index()
    XB_Hs['DateTime']= pd.to_datetime(XB_Hs['DateTime'], dayfirst=True)

    return XB_Hs


def extract_zb_point(dataset, point, start_date):
    XB_zb = pd.DataFrame() #Mise en forme pratique des résultats de XB pour le plt
    XB_zb['zb'] = dataset.H[:,0,point].astype(float) #Récupération de la colonne zb
    XB_zb['time'] = dataset.time.data #Récupération du vecteur temps
    
    #Conversion du temps (s) en date avec un pas minute
    XB_zb['DateTime'] = XBr.secondes_vers_temps(XB_zb['time'], start_date,'%Y-%m-%d %H:%M')
    XB_zb.set_index('DateTime', inplace=True)
    XB_zb = XB_zb.resample('1T').mean().reset_index()
    XB_zb['DateTime']= pd.to_datetime(XB_zb['DateTime'], dayfirst=True)

    return XB_zb


def extract_zs_point(dataset, point, start_date):
    XB_zs = pd.DataFrame() #Mise en forme pratique des résultats de XB pour le plt
    XB_zs['zs'] = dataset.H[:,0,point].astype(float) #Récupération de la colonne zs
    XB_zs['time'] = dataset.time.data #Récupération du vecteur temps
    
    #Conversion du temps (s) en date avec un pas minute
    XB_zs['DateTime'] = XBr.secondes_vers_temps(XB_zs['time'], start_date,'%Y-%m-%d %H:%M')
    XB_zs.set_index('DateTime', inplace=True)
    XB_zs = XB_zs.resample('1T').mean().reset_index()
    XB_zs['DateTime']= pd.to_datetime(XB_zs['DateTime'], dayfirst=True)

    return XB_zs
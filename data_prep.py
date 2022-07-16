import pandas_datareader as pdr
import pandas as pd
import numpy as np
from datetime import datetime as dt
start = dt(1992,1,1)
end = dt(2022,6,1)


# Getting EU Milk price from CLAI

# eu = pd.read_excel('https://www.clal.it/upload/eu-milk-historical-price-series_en06072022.xlsx', usecols='B:AC,AE', header=6, index_col=28, nrows=546)[['Germany', 'France', 'Netherlands', 'Italy', 'Poland', 'Irleand', 'Spain', 'Denmark', 'Belgium', 'Austria', 'EU\n\n(without UK)']]
eu = pd.read_excel('https://ec.europa.eu/info/sites/default/files/food-farming-fisheries/farming/documents/eu-milk-historical-price-series_en.xlsx', usecols='B:AC,AE', header=6, index_col=28, nrows=546)[['Germany', 'France', 'Netherlands', 'Italy', 'Poland', 'Irleand', 'Spain', 'Denmark', 'Belgium', 'Austria', 'EU\n\n(without UK)']]
eu.rename(columns = {'Irleand':'Ireland', 'EU\n\n(without UK)':'EU(without UK)'}, inplace = True)



# Getting US Milk price from quickstats


us_raw = pd.read_html('https://quickstats.nass.usda.gov/data/printable/ED3AE74E-9CE1-3094-BA0D-CD94A67BC399')[0][['Year','Period','State','Value']]
us_raw['Date'] = pd.to_datetime(us_raw.Period + '-' + us_raw.Year.astype(str))
us = us_raw.pivot(index='Date', columns='State').Value.rename(columns=str.title)[['California', 'Wisconsin', 'Idaho', 'Texas', 'New York', 'Michigan', 'Minnesota', 'Pennsylvania', 'New Mexico', 'Washington', 'Us Total']]
us.rename(columns = {'Us Total':'US Total'}, inplace = True)

# Getting China Milk price from CLAI

cn_raw = pd.read_html('https://www.clal.it/en/index.php?section=latte_cina')[9].iloc[2:14,0::2].iloc[:,:-2].to_numpy(dtype=float).T.flatten()
cn_raw = cn_raw[~np.isnan(cn_raw)]
cn = pd.Series(cn_raw, index = pd.date_range('2009-1-1', freq='MS', periods=len(cn_raw)), name='China')


# Getting other commodity prices from FRED

#fred = pdr.get_data_fred(['MCOILBRENTEU', 'MCOILWTICO', 'MHHNGSP', 'PBARLUSDM', 'PMAIZMTUSDM', 'PNGASEUUSDM', 'PSOYBUSDM', 'PWHEAMTUSDM', 'GDP', 'DGOERC1Q027SBEA', 'IPG32411S', 'A33DNO'], start, end)
fred = pdr.get_data_fred(['MCOILBRENTEU', 'MCOILWTICO', 'MHHNGSP', 'PBARLUSDM', 'PMAIZMTUSDM', 'PNGASEUUSDM', 'PSOYBUSDM', 'PWHEAMTUSDM', 'IPG32411S', 'A33DNO'], start, end)

eu.to_pickle('data/eu.pickle')
us.to_pickle('data/us.pickle')
cn.to_pickle('data/cn.pickle')
fred.to_pickle('data/fred.pickle')
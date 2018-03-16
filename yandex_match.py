import pandas as pd

ya=pd.read_excel('yandex_market.xlsx',dtype=str).replace({'nan':None})
ya=ya.loc[ya.Web.notnull()]
ya.Web=ya.Web.replace({'www.':''},regex=True)

top100=pd.read_excel('top100.xlsx',header=None,names=['Web'])
top100.Web=top100.Web.replace({'www.':''},regex=True)
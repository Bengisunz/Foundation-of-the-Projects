import warnings
import datetime
import numpy as np
import pandas as pd

from Core.CorePaths import GetMyRootFolder

warnings.filterwarnings("ignore")


def GettingTheYear(df, yearn):
    df['year'] = df['ds'].dt.year
    subset = df[df["year"] == yearn]
    subsetDataFrame = subset.drop(["year"], 1)
    return subsetDataFrame


class TimeSeriesCreatingFromFile(object):
    def __init__(self, csvname, yilaygun, columns=None):
        super().__init__()
        self.yilaygun = yilaygun
        self.columns = columns
        self.csvname = csvname

    def Read(self):
        RootPath = GetMyRootFolder()
        self.raw = pd.read_csv(RootPath + self.csvname)
        self.df = self.raw.copy()
        self.df.rename(str.lower, axis='columns', inplace=True)
        return self.df

    def Seperate(self, columnname):
        self.df[self.yilaygun] = self.df[self.yilaygun].apply(str)
        t = []
        for i in columnname:
            i = str(i)
            t.append(i[0:4] + "-" + i[4:6] + "-" + i[-2:])
        return t

    def ReadSeperateConvertime(self):
        dfc = self.Read()
        times = self.Seperate(dfc[self.yilaygun])
        time = []
        for i in range(0, len(times)):
            t = datetime.datetime.strptime(times[i], '%Y-%m-%d').date()
            time.append(t)

        dfc["date"] = np.array(time)

        return dfc

    def Extract(self):
        dfcw = self.ReadSeperateConvertime()
        dfcw = dfcw.drop(self.columns, 1)
        df1 = dfcw.groupby(["date"])["satis"].sum().reset_index()
        df1['ds'] = df1['date']
        df1['y'] = df1['satis']
        dfo = df1.drop(["satis", "date"], 1)
        dfo['ds'] = pd.to_datetime(dfo['ds'])
        return dfo

    def GetDf(self):
        dfts = self.Extract()
        return dfts


if __name__ == '__main__':
    cols = ['yilaygun', 'deporef', 'merchaltgrupref', 'yil', 'yildakiaylar',
            'yildakihaftalar', 'haftaningunu', 'aydakigunler', 'outletmi',
            'sehirref', 'stok']
    ut = TimeSeriesCreatingFromFile('MagazaGunBGM2017.csv', yilaygun='yilaygun', columns=cols)
    y = ut.ReadSeperateConvertime()

import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from Core.CorePaths import FileReader


class HolidayTableCreating(object):

    def __init__(self, dataframe, datecolumn, cref, ref):
        super().__init__()

        self.datec = datecolumn
        self.cref = cref
        self.dataframe = dataframe
        self.ref = ref

    def Preprocessing(self):
        self.dataframe[self.cref].fillna(0).astype(int)
        self.dataframe[self.datec] = pd.to_datetime(self.dataframe[self.datec])
        subsetDataFrame = self.dataframe[
            self.dataframe[self.cref] == self.ref]  # subsetDataFrame['day'] = subsetDataFrame.gun.dt.day
        return subsetDataFrame

    def Zerolistmaker(self, n):
        listofzeros = [0] * n
        return listofzeros

    #
    # def onelistmaker(self, n):
    #     listofones = [1] * n
    #     return listofones

    def Windows(self):
        subset_data_frame = self.Preprocessing()  # belki baska isim vermem gerekebilir
        lower_window = self.Zerolistmaker(len(subset_data_frame["name"]))
        upper_window = self.Zerolistmaker(len(subset_data_frame["name"]))
        subset_data_frame["lower_window"] = lower_window
        subset_data_frame["upper_window"] = upper_window
        newdf = subset_data_frame.filter(['name', 'gun', "lower_window", "upper_window"], axis=1)
        newdf.rename(columns={"name": "holiday", "gun": "ds"}, inplace=True)
        return newdf

    def GetDf(self) :
        holidaydf = self.Windows()
        return holidaydf




if __name__ == '__main__':
    t = FileReader()
    rawdf = t.ReadExcel("sdays_summary.xlsx")  # TODO: Local holidays should be added
    rawdf.rename(str.lower, axis='columns', inplace=True)
    myholiday = HolidayTableCreating(rawdf, "gun", "countryref", 57)
    d = myholiday.GetDf()

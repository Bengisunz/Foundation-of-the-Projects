from Core.CorePaths import FileReader

class TrainTestSplit(object):

    """
    :param df: Timeseries Dataframe, datecolumns:Column of Date, splitday: The day that train and test datasets split
    :return: train and test sets

    """
    def __init__(self,dataframe,datecolumn,splitday):
        super().__init__()

        self.dataframe = dataframe
        self.datecolumn = datecolumn
        self.splitday=splitday

    def MaxMinDays(self):
        print(self.dataframe[self.datecolumn].max())
        print(self.dataframe[self.datecolumn].min())

    def TrainTestSplit(self):
        train = self.dataframe.loc[self.dataframe[self.datecolumn] < self.splitday]
        test = self.dataframe.loc[self.dataframe[self.datecolumn] > self.splitday]
        return train, test

    def GetTrainTest(self):
        trainset, testset = self.TrainTestSplit()
        return trainset, testset



if __name__ == '__main__':

    reader = FileReader()
    raw_df = reader.ReadCsv("timesplitdeneme.csv")
    tt = TrainTestSplit(raw_df, "ds", "2019-01-01")
    tt.MaxMinDays()
    t, u = tt.GetTrainTest()

import pandas as pd


def GetMyRootFolder():
    return "C:/Users/bengisu.oniz/Documents/datasets/"


class FileReader(object):

    def __init__(self, rootPath = None):
        super().__init__()
        self.RootPath = rootPath
        if self.RootPath is None:
            self.RootPath = GetMyRootFolder()

    def ReadCsv(self, nameofthefile):
        raw = pd.read_csv(self.RootPath + nameofthefile)
        raw.rename(str.lower, axis='columns', inplace=True)
        return raw

    def ReadExcel(self, nameofthefile):
        raw = pd.read_excel(self.RootPath + nameofthefile)
        raw.rename(str.lower, axis='columns', inplace=True)
        return raw


def know_data(data):
    print('Head: {}'.format(data.ndim))
    print('Shape: {}'.format(data.shape))
    print('Length: {}'.format(data.size))
    print('Columns: {}'.format(data.columns))
    print("-----------------------------------")
    print('Types: {}'.format(data.dtypes))
    print("-----------------------------------")
    print("Nullity Check:\n", pd.isnull(data).any())


if __name__ == '__main__':
    myfile = FileReader().ReadCsv("mytest.csv")
    print(myfile.head())

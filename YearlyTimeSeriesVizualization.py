from Core.CorePaths import FileReader
from Foundation.ConvertingToTimeSeries import GettingTheYear, TimeSeriesCreatingFromFile
import matplotlib.pyplot as plt

# region Creatibg Df
from Foundation.TimeSeriesVizualization import TimeSeriesVizualization, CreatingHolidayTableforPlotting

reader = FileReader()

romania_rawdf = reader.ReadCsv("ro_ma.csv")
ro = romania_rawdf[romania_rawdf["ulkeref"] == 65]

cols = ['deporef', 'tl', 'gsddepostok',
        'gsdreyonstok', 'satislfl', 'tllfl', 'gsddepostoklfl',
        'gsdreyonstoklfl']

ts_of_romania_sales = TimeSeriesCreatingFromFile('ro.csv', yilaygun='yilaygun', columns=cols)
df_ts = ts_of_romania_sales.GetDf()
df = df_ts.copy()


# endregion

def YearlyDataFrameCreater(df, year, columnname_date, columnname_value):
    dfyearly = GettingTheYear(df, year)
    myyearlyvizs = TimeSeriesVizualization(dfyearly, columnname_date, columnname_value)
    seri, df = myyearlyvizs.df_to_series()
    return seri, df


seri, df = YearlyDataFrameCreater(df, 2018, "ds", "y")

df_holidays = CreatingHolidayTableforPlotting("sdays_summary.xlsx", 65, "gun", "countryref", 2018)

ax = df.plot(color='blue', figsize=(8, 3), linewidth=2, fontsize=6)
fig = plt.figure(figsize=(16, 9))
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Sales', fontsize=12)
for index, row in df_holidays.iterrows():
    ax.axvline(row["gun"], color=row["rand_col"], linestyle='-', linewidth=1, alpha=0.8)  # fig.savefig('test.jpg')
plt.show()

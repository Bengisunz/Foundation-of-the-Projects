import warnings
import matplotlib.pyplot as plt
import pandas as pd
import random
import matplotlib

from statsmodels.graphics import tsaplots
from statsmodels.api import tsa
from pylab import rcParams

from Core.CorePaths import FileReader
from Foundation.SpecialDayOrganization import HolidayTableCreating

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')


class TimeSeriesVizualization(object):
    def __init__(self, df, ds, y):
        super().__init__()
        self.df = df
        self.ds = ds
        self.y = y

    def df_to_series(self):
        df_c = self.df.copy()
        df_c[self.ds] = pd.to_datetime(df_c[self.ds], errors='coerce')
        df_c.set_index(self.ds, inplace=True)
        seri = pd.Series(df_c[self.y], index=df_c.index)

        return seri, df_c

    def Subsets(self):
        sr, dfs = self.df_to_series()
        df_subset_2016 = dfs['2016':'2016']
        df_subset_2017 = dfs['2017':'2017']
        df_subset_2018 = dfs['2018':'2018']
        return df_subset_2016, df_subset_2017, df_subset_2018

    def GetSubsets(self):
        df_subset_2016, df_subset_2017, df_subset_2018 = self.Subsets()  # df_subset > df_subset[0],df_subset[1]
        return df_subset_2016, df_subset_2017, df_subset_2018

    def Plot(self):
        series, df = self.df_to_series()
        self.plot = series.plot()
        return self.plot

    def Hist(self, binsize=5000):
        series, df = self.df_to_series()
        ax2 = df.plot(kind='hist', bins=binsize)
        ax2.set_xlabel('Sales')
        ax2.set_ylabel('Frequency of Sales')
        ax2.set_title('Histogram of Sales data with ' + str(binsize) + ' bins')
        return ax2

    def BoxPlot(self):
        series, df = self.df_to_series()
        ax1 = df.boxplot()
        ax1.set_xlabel('Boxplot')
        ax1.set_ylabel('Sales')
        ax1.set_title('Boxplot of Sales')
        return ax1

    def KPlot(self):
        series, df = self.df_to_series()
        self.kplot = series.plot(style='k.')
        return self.kplot

    def KdePlot(self):
        series, df = self.df_to_series()
        self.kdeplot = series.plot(kind='kde')
        return self.kdeplot

    def DensityPlot(self):
        series, df = self.df_to_series()
        ax3 = df.plot(kind='density', linewidth=2)
        ax3.set_xlabel('Sales')
        ax3.set_ylabel('Density values of Sales')
        ax3.set_title('Density plot of Sales')
        return ax3

    def LinePlot(self):
        plt.style.use('fivethirtyeight')
        series, df = self.df_to_series()
        ax5 = df.plot(color='blue', figsize=(8, 3), linewidth=2, fontsize=6)
        ax5.set_xlabel('Date')
        ax5.set_ylabel('Number of Sales')

        # Adding markers
        # ax.axvline('1969-01-01', color='red', linestyle='--')
        # ax.axhline(4, color='green', linestyle='--')

        # Highlighting regions of interest
        # ax.axvspan('1964-01-01', '1968-01-01', color='red', alpha=0.3)
        # ax.axhspan(8, 6, color='green', alpha=0.3)
        return ax5

    def MovingAverageModel(self, windowsize=20):
        series, df = self.df_to_series()
        df_m = df.rolling(window=windowsize).mean()
        ax = df_m.plot(color='blue', figsize=(8, 3), linewidth=2, fontsize=6)
        ax.set_xlabel("Date")
        ax.set_ylabel("The values of Sales")
        ax.set_title("52 weeks rolling mean of Sales")
        return ax

    def AverageMontly(self):
        series, df = self.df_to_series()
        index_month = df.index.month
        mean_df_levels_by_month = df.groupby(index_month).mean()
        mean_df_levels_by_month.plot(color='red', figsize=(8, 3), linewidth=2, fontsize=8)
        plt.legend(fontsize=10)
        return mean_df_levels_by_month

    def AverageDaily(self):
        series, df = self.df_to_series()
        index_daily = df.index.day
        mean_df_levels_by_daily = df.groupby(index_daily).mean()
        mean_df_levels_by_daily.plot(color='orange', figsize=(8, 3), linewidth=2, fontsize=8)
        plt.legend(fontsize=10)
        return mean_df_levels_by_daily

    def AutoCorrelation_plot(self, lag=52):  # TODO: lagsize
        series, df = self.df_to_series()
        fig1 = tsaplots.plot_acf(df[self.y], lags=lag)
        return fig1

    def PACF(self):
        series, df = self.df_to_series()
        fig2 = tsaplots.plot_pacf(df[self.y], lags=24)
        return fig2

    def Decomposition(self):
        series, df = self.df_to_series()
        rcParams['figure.figsize'] = 11, 9
        decomposition = tsa.seasonal_decompose(df['y'])
        fig3 = decomposition.plot()
        return fig3

    def Trend(self):
        series, df = self.df_to_series()
        decomposition = tsa.seasonal_decompose(df)
        trend = decomposition.trend
        ax6 = trend.plot(figsize=(12, 6), fontsize=6)
        ax6.set_xlabel('Date', fontsize=10)
        ax6.set_title('Seasonal component the Sales', fontsize=10)
        return ax6


def CreatingHolidayTableforPlotting(excelname, int_countryref, ds, countryrefcolumnname, year):
    reader = FileReader()
    rawdf = reader.ReadExcel(excelname)
    myholiday = HolidayTableCreating(rawdf, ds, countryrefcolumnname, int_countryref)
    hh = myholiday.Preprocessing()
    hh = hh.drop(["definitionref", "countryref"], 1)
    colour = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "olive", "peru", "teal",
              "silver"]
    rand_colours = [random.choice(colour) for i in range(len(hh))]
    hh['year'] = hh[ds].dt.year
    hh["rand_col"] = rand_colours
    hh18 = hh[hh["year"] == year]
    return hh18


def ComparingTrendLines(data_df, datecolumn, real_value, predicted_value):
    """
    :param data_df: The main date which should be dataframe
    :param datecolumn: May be ds
    :param predicted_value: The value after forecast
    :param real_value: The groundtruth
    :return: Visualization> Comparison of the prediction value and realvalue
    """
    plt.plot(datecolumn, predicted_value, data=data_df, marker="", color='red', linewidth=2)
    plt.plot(datecolumn, real_value, data=data_df, marker='', color='blue', linewidth=2)
    plt.title("Trendline of forecasted and actual value", loc='left', fontsize=20, fontweight=0, color='black')
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    reader = FileReader()
    magdf = reader.ReadCsv("timesplitdeneme.csv")
    viz = TimeSeriesVizualization(magdf, 'ds', 'y')
    x = viz.df
    viz.AutoCorrelation_plot()

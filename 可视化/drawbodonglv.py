import tushare as ts
from time import sleep
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pandas as pd
import numpy as np
import wx
import wx.lib.plot as plot

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 100)
pd.set_option('display.width', 1000)


def stock_history_data_get(code, startTime, endTime):
    df = ts.get_hist_data(code, start=startTime, end=endTime)
    df_v1 = df.reset_index()
    # print(df_v1)

    df_v2 = df_v1[['date', 'close', 'p_change']].sort_values(by='date', ascending=True)
    df_v2['p_change'] = df_v2['p_change'] * 0.01
    stv_4 = [0, 0, 0]
    stv_8 = [0, 0, 0, 0, 0, 0, 0]
    stv_12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    stv_16 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(df_v2)):
        sample = list(df_v2['p_change'][i:i + 4])
        stv = np.std(sample)
        stv_4.append(stv)
        if i == len(df_v2) - 4:
            break
    df_v2['stv_4'] = stv_4

    for i in range(0, len(df_v2)):
        sample = list(df_v2['p_change'][i:i + 8])
        stv = np.std(sample)
        stv_8.append(stv)
        if i == len(df_v2) - 8:
            break
    df_v2['stv_8'] = stv_8

    for i in range(0, len(df_v2)):
        sample = list(df_v2['p_change'][i:i + 12])
        stv = np.std(sample)
        stv_12.append(stv)
        if i == len(df_v2) - 12:
            break
    df_v2['stv_12'] = stv_12

    for i in range(0, len(df_v2)):
        sample = list(df_v2['p_change'][i:i + 16])
        stv = np.std(sample)
        stv_16.append(stv)
        if i == len(df_v2) - 16:
            break
    df_v2['stv_16'] = stv_16

    df_v2['hv_4'] = round(df_v2['stv_4'] * 12 * 1040, 2).apply(lambda x: '%.2f%%' % (x))
    df_v2['hv_8'] = round(df_v2['stv_8'] * 12 * 1040, 2).apply(lambda x: '%.2f%%' % (x))
    df_v2['hv_12'] = round(df_v2['stv_12'] * 12 * 1040, 2).apply(lambda x: '%.2f%%' % (x))
    df_v2['hv_16'] = round(df_v2['stv_16'] * 12 * 1040, 2).apply(lambda x: '%.2f%%' % (x))
    # df_v2.to_csv('//Users//hejie//AnacondaProjects//181902PythonInFinace//50.csv', index=True)
    df_v2.to_csv('50.csv', index=True)


def getDF(code, startTime, endTime):
    stock_history_data_get(code, startTime, endTime)
    df = pd.read_csv('./50.csv', header=0)
    return df


def getData(df):
    df = pd.read_csv('./50.csv', header=0)
    dataList = []
    for index, item in enumerate(df['hv_4'].tolist()):
        dataList.append([index, item[:-1]])
    return dataList
    # print(dataList)


class MyFrame(wx.Frame):
    def __init__(self):
        self.frame1 = wx.Frame(None, title="sz50股票波动率", id=-1, size=(500, 350))
        self.panel1 = wx.Panel(self.frame1)
        self.panel1.SetBackgroundColour("white")
        self.code = wx.TextCtrl(self.panel1, value="sz50", pos=(100, 220), size=(150, 20))
        wx.StaticText(self.panel1, -1, "标签代码：", pos=(30, 220), size=(60, 20))
        wx.StaticText(self.panel1, -1, "股票时间：", pos=(30, 260), size=(60, 20))
        self.startTime = wx.TextCtrl(self.panel1, value="2018-03-01", pos=(100, 260), size=(100, 20))
        self.endTime = wx.TextCtrl(self.panel1, value="2019-05-03", pos=(230, 260), size=(100, 20))
        Button1 = wx.Button(self.panel1, -1, "查找", (280, 215))
        Button1.Bind(wx.EVT_BUTTON, self.redraw)

        plotter = plot.PlotCanvas(self.panel1)
        plotter.SetInitialSize(size=(500, 200))
        code = self.code.GetValue()
        startTime = self.startTime.GetValue()
        endTime = self.endTime.GetValue()
        self.df = getDF(code, startTime, endTime)
        data = getData(self.df)
        line = plot.PolyLine(data, colour='red', width=1)

        gc = plot.PlotGraphics([line], 'sz50股票波动率', '时间', '波动率')
        plotter.Draw(gc)

        self.frame1.Show(True)

    def redraw(self, event):
        plotter = plot.PlotCanvas(self.panel1)
        plotter.SetInitialSize(size=(500, 200))
        code = self.code.GetValue()
        startTime = self.startTime.GetValue()
        endTime = self.endTime.GetValue()
        self.df = getDF(code, startTime, endTime)
        for i in range(len(self.df)):
            data2 = getData(self.df[:i])
            line = plot.PolyLine(data2, colour='red', width=1)
            gc = plot.PlotGraphics([line], code + '股票波动率', '时间', '波动率')
            plotter.Draw(gc)


app = wx.App()
f = MyFrame()
app.MainLoop()

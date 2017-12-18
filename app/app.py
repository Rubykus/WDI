import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np

from os import path
from tkinter import messagebox
from PIL import ImageTk, Image

from .spinner import Spinner

DIR_PATH = path.abspath(path.dirname(__file__))


class App:
    CHART_TYPES = ['Plot', 'Bar', 'Stacker Bar', 'Area', 'Pie']

    current_chart = 0
    current_country = (0,)
    current_indicator = 0

    def __init__(self, master, queue):
        self.master = master
        self.queue = queue

        self.spinner = Spinner(self.master)

    def setup_ui(self):
        # main frame
        self.main_frame = tk.Frame()
        self.main_frame.pack(fill=tk.BOTH)

        # image UI
        self.img = ImageTk.PhotoImage(Image.open(path.join(DIR_PATH, '../assets/img/world.jpg')).resize((900, 200), Image.ANTIALIAS))
        self.img_label = tk.Label(self.main_frame, image=self.img)
        self.img_label.image = self.img
        self.img_label.pack()

        # lists UI
        self.lists_frame = tk.Frame(self.main_frame)
        self.lists_frame.pack(fill=tk.X)
        self.setup_countries_list()
        self.setup_indicators_list()
        self.setup_chart_list()

        self.label_current_pick = tk.Label(self.main_frame, height=2)
        self.label_current_pick.pack()

        self.range_frame = tk.Frame(self.main_frame, height=2)
        self.range_frame.pack()
        # self.setup_range_frame()

        self.btn = tk.Button(self.main_frame, text='Generate', command=self.build_chart)
        self.btn.pack(side=tk.BOTTOM)

        self.calculate_chart()

    def setup_range_frame(self):
        self.entry_Ymin = tk.Entry(self.range_frame, validate="key", width=5)
        self.entry_Ymin['validatecommand'] = (self.entry_Ymin.register(self.val_years), '%P', '%i', '%d')
        self.entry_Ymin.pack(side=tk.LEFT)
        self.label_Ymin = tk.Label(self.range_frame)
        self.label_Ymin.pack(side=tk.LEFT)

        self.label_divider = tk.Label(self.range_frame, text='-')
        self.label_divider.pack(side=tk.LEFT)

        self.entry_Ymax = tk.Entry(self.range_frame, validate="key", width=5)
        self.entry_Ymax['validatecommand'] = (self.entry_Ymax.register(self.val_years), '%P', '%i', '%d')
        self.entry_Ymax.pack(side=tk.LEFT)
        self.label_Ymax = tk.Label(self.range_frame)
        self.label_Ymax.pack(side=tk.LEFT)

        self.label_text_freq = tk.Label(self.range_frame, text='  Freq. - ')
        self.label_text_freq.pack(side=tk.LEFT)
        self.entry_freq = tk.Entry(self.range_frame, validate="key", width=2)
        self.entry_freq['validatecommand'] = (self.entry_freq.register(self.val_freq), '%P', '%i', '%d')
        self.entry_freq.pack(side=tk.LEFT)

    def val_years(self, inStr, i, acttyp):
        ind = int(i)
        if ind == 4:
            return False

        if acttyp == '1':
            char = inStr[ind]
            if not char.isdigit():
                return False

            str_len = len(inStr)
            if not (int(inStr) >= int(str(self.Ymin)[:str_len]) and int(inStr) <= int(str(self.Ymax)[:str_len])):
                return False

        return True

    def val_freq(self, inStr, i, acttyp):
        ind = int(i)
        if ind == 2:
            return False

        if acttyp == '1':
            char = inStr[ind]
            if not char.isdigit():
                return False

            if inStr[0] == '0':
                return False

        return True

    def setup_chart_list(self):
        self.listbox_chart = tk.Listbox(self.lists_frame, exportselection=0, width=30, height=5)

        for i in self.CHART_TYPES:
            self.listbox_chart.insert(tk.END, i)

        self.listbox_chart.pack(side=tk.BOTTOM)

        self.listbox_chart.select_set(0)
        self.listbox_chart.bind("<<ListboxSelect>>", self.select_chart)

    def select_chart(self, event):
        self.current_chart = self.listbox_chart.curselection()[0]

    def setup_countries_list(self):
        self.scrollbar_countries = tk.Scrollbar(self.lists_frame)
        self.scrollbar_countries.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox_countries = tk.Listbox(self.lists_frame, exportselection=0, width=30, height=25,
                                            yscrollcommand=self.scrollbar_countries.set, selectmode=tk.MULTIPLE)

        truncated_list_items = ((x[:35] + '...') if len(x) > 35 else x for x in tuple(self.df_country.iloc[:, 1]))
        for i in truncated_list_items:
            self.listbox_countries.insert(tk.END, i)

        self.listbox_countries.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar_countries.config(command=self.listbox_countries.yview)

        self.listbox_countries.select_set(0)
        self.listbox_countries.bind("<<ListboxSelect>>", self.select_country)

    def select_country(self, event):
        selected = self.listbox_countries.curselection()

        if not len(selected):
            self.listbox_countries.select_set(self.current_country)
            return
        elif len(selected) > 3:
            for i in selected:
                if i not in self.current_country:
                    self.listbox_countries.selection_clear(i)

        self.current_country = self.listbox_countries.curselection()

        self.calculate_chart()

    def setup_indicators_list(self):
        self.scrollbar_indicators = tk.Scrollbar(self.lists_frame)
        self.scrollbar_indicators.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_indicators = tk.Listbox(self.lists_frame, exportselection=0, width=60, height=25,
                                             yscrollcommand=self.scrollbar_indicators.set)

        truncated_list_items = ((x[:72] + '...') if len(x) > 72 else x for x in tuple(self.df_indicator_names.iloc[:, 0]))
        for i in truncated_list_items:
            self.listbox_indicators.insert(tk.END, i)

        self.listbox_indicators.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.scrollbar_indicators.config(command=self.listbox_indicators.yview)

        self.listbox_indicators.select_set(0)
        self.listbox_indicators.bind("<<ListboxSelect>>", self.select_indicator)

    def select_indicator(self, event):
        self.current_indicator = self.listbox_indicators.curselection()[0]

        self.calculate_chart()

    def calculate_chart(self):
        for widget in self.range_frame.winfo_children():
            widget.destroy()

        self.btn['state'] = tk.DISABLED
        self.master.update()

        country_codes = self.df_country.iloc[list(self.current_country), 0].values
        indicator = self.df_indicator_names.iloc[self.current_indicator, 0]

        plot_data = []

        for country_code in country_codes:
            indicator_data = self.df_indicators.loc[(self.df_indicators['IndicatorName'] == indicator) &
                                                    (self.df_indicators['CountryCode'] == country_code)]

            if not indicator_data.size:
                messagebox.showwarning("Error", "Data for this prameters don't exist.")
                return

            indicator_data.columns = ['CountryCode', 'IndicatorName', 'Year', indicator_data.iloc[0, 0]]
            indicator_data = indicator_data[['Year', indicator_data.iloc[0, 0]]].set_index('Year')

            plot_data.append(indicator_data)

        self.df_plot = plot_data[0].join(plot_data[1:], how='inner')

        self.Ymax = self.df_plot.index.max()
        self.Ymin = self.df_plot.index.min()

        self.update_ui()

    def update_ui(self):
        self.btn['state'] = tk.NORMAL

        self.label_current_pick['text'] = ', '.join(self.df_country.iloc[list(self.current_country), 1].values) + ' - ' +\
            self.df_indicator_names.iloc[self.current_indicator, 0]

        self.setup_range_frame()

        self.label_Ymin['text'] = '('+str(self.Ymin)+')'
        self.label_Ymax['text'] = '('+str(self.Ymax)+')'

        self.entry_Ymin.delete(0, tk.END)
        self.entry_Ymin.insert(0, self.Ymin)

        self.entry_Ymax.delete(0, tk.END)
        self.entry_Ymax.insert(0, self.Ymax)

        self.entry_freq.delete(0, tk.END)
        self.entry_freq.insert(0, 1)

    def build_chart(self):
        y_max = int(self.entry_Ymax.get())
        y_min = int(self.entry_Ymin.get())
        diff = y_max - y_min

        if (diff > self.Ymax - self.Ymin) or (diff < 0):
            messagebox.showwarning("Error", "Wrong year range.")
            return

        freq = int(self.entry_freq.get())

        if (diff == 0 and freq == 1):
            pass
        elif freq > diff:
            messagebox.showwarning("Error", "Wrong freq.")
            return

        df_plot = self.df_plot.loc[(self.df_plot.index >= y_min) & (self.df_plot.index <= y_max)]
        df_plot = df_plot.cumsum()

        if self.current_chart == 0:
            df_plot.plot()
        elif self.current_chart == 1 or self.current_chart == 2:
            if (diff == freq):
                df_plot.loc[y_max] = self.df_plot.sum()
                df_plot = df_plot.loc[df_plot.index == y_max]
            else:
                plot_data = []
                curr_year = y_min
                for i in range(0, int(diff / freq)):
                    df = df_plot.loc[(df_plot.index >= curr_year) & (df_plot.index <= curr_year + freq - 1)]
                    df.loc[curr_year + freq - 1] = df.sum()
                    plot_data.append(df.loc[df.index == curr_year + freq - 1])
                    curr_year += freq

                df_plot = pd.concat(plot_data)

            if self.current_chart == 1:
                df_plot.plot(kind='bar')
            else:
                df_plot.plot(kind='bar', stacked=True)
        elif self.current_chart == 3:
            df_plot.plot(kind='area')
        elif self.current_chart == 4:
            ds_plot_avg = pd.Series(index=df_plot.columns)

            for index in ds_plot_avg.index.tolist():
                ds_plot_avg[index] = df_plot[index].sum()

            ds_plot_avg.plot(kind='pie', autopct='%.2f')

        indicator = self.df_indicator_names.iloc[self.current_indicator, 0]
        plt.title(', '.join(self.df_country.iloc[list(self.current_country), 1].values) + ' - ' + indicator)

        if self.current_chart == 4:
            plt.ylabel('')
        else:
            plt.xlabel('years')

            if not (self.current_chart == 1 or self.current_chart == 2):
                plt.xticks(np.arange(y_min, y_max + 1, freq), rotation=90)
            plt.grid(True)

        mng = plt.get_current_fig_manager()
        mng.window.attributes("-fullscreen", True)
        mng.window.bind('<Escape>', lambda _: mng.window.destroy())
        plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk

from os import path
from tkinter import messagebox
from PIL import ImageTk, Image

DIR_PATH = path.abspath(path.dirname(__file__))


class App:
    def __init__(self, master):
        self.main_frame = tk.Frame()
        self.main_frame.pack(fill=tk.BOTH)

        # read datsets
        self.read_datasets()

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
        self.setup_type_chart_list()

        self.currents_chart = 0
        self.current_country = (0,)
        self.current_indicator = 0

        label_text = ', '.join(self.df_country.iloc[list(self.current_country), 1].values) + ' - ' +\
            self.df_indicator_names.iloc[self.current_indicator, 0]
        self.label_current_pick = tk.Label(
            self.main_frame,
            height=4,
            text=label_text,
        )
        self.label_current_pick.pack()

        self.btn = tk.Button(self.main_frame, text='Generate', command=self.build_chart)
        self.btn.pack(side=tk.BOTTOM)

    def read_datasets(self):
        self.df_country = pd.read_csv(path.join(DIR_PATH, '../dataset/Country.csv'),
                                      usecols=['CountryCode', 'ShortName'])

        self.df_indicator_names = pd.read_csv(path.join(DIR_PATH, '../dataset/IndicatorsName.csv'), sep='\t')

        self.df_indicators = pd.read_csv(path.join(DIR_PATH, '../dataset/Indicators.csv'),
                                         usecols=['CountryCode', 'IndicatorName', 'Year', 'Value'])

    def setup_type_chart_list(self):
        self.listbox_chart = tk.Listbox(self.lists_frame, exportselection=0, width=30, height=5)

        for i in ['Plot', 'Bar', 'Stacker Bar', 'Area', 'Pie']:
            self.listbox_chart.insert(tk.END, i)

        self.listbox_chart.pack(side=tk.BOTTOM)

        self.listbox_chart.select_set(0)
        self.listbox_chart.bind("<<ListboxSelect>>", self.select_chart)

    def select_chart(self, event):
        self.currents_chart = self.listbox_chart.curselection()[0]

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

        if len(selected) > 3:
            for i in selected:
                if i not in self.current_country:
                    self.listbox_countries.selection_clear(i)

        self.current_country = self.listbox_countries.curselection()
        self.label_current_pick['text'] = ', '.join(self.df_country.iloc[list(self.current_country), 1].values) + ' - ' +\
            self.df_indicator_names.iloc[self.current_indicator, 0]

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
        self.label_current_pick['text'] = ', '.join(self.df_country.iloc[list(self.current_country), 1].values) + ' - ' +\
            self.df_indicator_names.iloc[self.current_indicator, 0]

    def build_chart(self):
        country_codes = self.df_country.iloc[list(self.current_country), 0].values
        indicator = self.df_indicator_names.iloc[self.current_indicator, 0]

        if not (country_codes.size and indicator):
            messagebox.showwarning("Error", "Please, select parameters.")
            return

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

        df_plot = plot_data[0].join(plot_data[1:], how='inner')
        df_plot.index = df_plot.index.map(str)
        df_plot = df_plot.cumsum()

        if self.currents_chart == 0:
            df_plot.plot()
        elif self.currents_chart == 1:
            df_plot.plot(kind='bar')
        elif self.currents_chart == 2:
            df_plot.plot(kind='bar', stacked=True)
        elif self.currents_chart == 3:
            df_plot.plot(kind='area')
        elif self.currents_chart == 4:
            ds_plot_avg = pd.Series(index=df_plot.columns)

            for index in ds_plot_avg.index.tolist():
                ds_plot_avg[index] = df_plot[index].mean()

            ds_plot_avg.plot(kind='pie', autopct='%.2f')

        plt.title(', '.join(self.df_country.iloc[list(self.current_country), 1].values) + ' - ' + indicator)

        if self.currents_chart == 4:
            plt.ylabel('')
        else:
            plt.xlabel('years')
            plt.grid(True)

        mng = plt.get_current_fig_manager()
        mng.window.attributes("-fullscreen", True)
        mng.window.bind('<Escape>', lambda _: mng.window.destroy())
        plt.show()

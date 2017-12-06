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

        self.current_country = 0
        self.current_indicator = 0
        self.label_current_pick = tk.Label(
            self.main_frame,
            height=4,
            text=self.country_names_list[self.current_country] + ' - ' + self.indicator_names_list[self.current_indicator],
        )
        self.label_current_pick.pack()

        self.btn = tk.Button(self.main_frame, text='Generate', command=self.build_chart)
        self.btn.pack(side=tk.BOTTOM)

    def read_datasets(self):
        self.df_country = pd.read_csv(path.join(DIR_PATH, '../dataset/Country.csv'),
                                      index_col='CountryCode', usecols=['CountryCode', 'ShortName'])
        self.country_names_list = tuple(self.df_country['ShortName'])

        self.df_indicator_names = pd.read_csv(path.join(DIR_PATH, '../dataset/IndicatorsName.csv'), sep='\t')
        self.indicator_names_list = tuple(self.df_indicator_names['IndicatorName'])

        self.df_indicators = pd.read_csv(path.join(DIR_PATH, '../dataset/Indicators.csv'),
                                         usecols=['CountryCode', 'IndicatorName', 'Year', 'Value'])

    def setup_countries_list(self):
        self.scrollbar_countries = tk.Scrollbar(self.lists_frame)
        self.scrollbar_countries.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox_countries = tk.Listbox(self.lists_frame, exportselection=0, width=30, height=25,
                                            yscrollcommand=self.scrollbar_countries.set)

        truncated_list_items = ((x[:35] + '...') if len(x) > 35 else x for x in self.country_names_list)
        for i in truncated_list_items:
            self.listbox_countries.insert(tk.END, i)

        self.listbox_countries.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar_countries.config(command=self.listbox_countries.yview)

        self.listbox_countries.select_set(0)
        self.listbox_countries.bind("<<ListboxSelect>>", self.select_country)

    def select_country(self, event):
        self.current_country = self.listbox_countries.curselection()[0]
        self.label_current_pick['text'] = self.country_names_list[self.current_country] + ' - ' \
            + self.indicator_names_list[self.current_indicator]

    def setup_indicators_list(self):
        self.scrollbar_indicators = tk.Scrollbar(self.lists_frame)
        self.scrollbar_indicators.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_indicators = tk.Listbox(self.lists_frame, exportselection=0, width=60, height=25,
                                             yscrollcommand=self.scrollbar_indicators.set)

        truncated_list_items = ((x[:72] + '...') if len(x) > 72 else x for x in self.indicator_names_list)
        for i in truncated_list_items:
            self.listbox_indicators.insert(tk.END, i)

        self.listbox_indicators.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.scrollbar_indicators.config(command=self.listbox_indicators.yview)

        self.listbox_indicators.select_set(0)
        self.listbox_indicators.bind("<<ListboxSelect>>", self.select_indicator)

    def select_indicator(self, event):
        self.current_indicator = self.listbox_indicators.curselection()[0]
        self.label_current_pick['text'] = self.country_names_list[self.current_country] + ' - ' \
            + self.indicator_names_list[self.current_indicator]

    def build_chart(self):
        country = self.country_names_list[self.current_country]
        indicator = self.indicator_names_list[self.current_indicator]

        country_code = self.df_country.loc[self.df_country['ShortName'] == country].index[0]
        indicator_data = self.df_indicators.loc[(self.df_indicators['IndicatorName'] == indicator) &
                                                (self.df_indicators['CountryCode'] == country_code)]

        if not indicator_data.size:
            messagebox.showwarning("Error", "Data for this prameters don't exist.")
            return

        x_values = tuple(indicator_data['Year'])
        y_values = tuple(indicator_data['Value'])

        plt.plot(x_values, y_values, color='g', linewidth=3.0)
        plt.title(country + ' - ' + indicator)
        plt.xlabel('years')
        mng = plt.get_current_fig_manager()
        mng.window.attributes("-fullscreen", True)
        mng.window.bind('<Escape>', lambda _: mng.window.destroy())
        plt.show()

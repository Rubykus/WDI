import threading
import queue
import pandas as pd

from os import path

from .app import App

DIR_PATH = path.abspath(path.dirname(__file__))


class ThreadedClient:
    def __init__(self, master):
        self.master = master
        self.queue = queue.Queue()

        self.gui = App(self.master, self.queue)

        t = threading.Thread(target=self.read_datasets)
        t.start()

        self.listen_for_read_result()

    def read_datasets(self):
        self.gui.df_country = pd.read_csv(path.join(DIR_PATH, '../dataset/Country.csv'),
                                          usecols=['CountryCode', 'ShortName'])

        self.gui.df_indicator_names = pd.read_csv(path.join(DIR_PATH, '../dataset/IndicatorsName.csv'), sep='\t')

        self.gui.df_indicators = pd.read_csv(path.join(DIR_PATH, '../dataset/Indicators.csv'),
                                             usecols=['CountryCode', 'IndicatorName', 'Year', 'Value'])

        self.queue.put(1)

    def listen_for_read_result(self):
        try:
            self.queue.get(0)
            self.gui.spinner.destroy()
            self.gui.setup_ui()
        except queue.Empty:
            self.master.after(100, self.listen_for_read_result)

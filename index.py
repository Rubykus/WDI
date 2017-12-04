import pandas as pd
import matplotlib.pyplot as plt

df_country = pd.read_csv('./dataset/Country.csv', index_col='CountryCode', usecols=['CountryCode', 'ShortName'])
df_indicators = pd.read_csv('./dataset/Indicators.csv', usecols=['CountryCode', 'IndicatorName', 'Year', 'Value'])


def build_chart(country, indicator):
    country_code = df_country.loc[df_country['ShortName'] == country].index[0]
    indicator_data = df_indicators.loc[(df_indicators['IndicatorName'] == indicator) & (df_indicators['CountryCode'] == country_code)]

    x_values = tuple(indicator_data['Year'])
    y_values = tuple(indicator_data['Value'])

    plt.plot(x_values, y_values, color='g', linewidth=3.0)
    plt.title(country + ' - ' + indicator)
    plt.xlabel('years')
    plt.show()


build_chart('Ukraine', 'Agricultural machinery, tractors')

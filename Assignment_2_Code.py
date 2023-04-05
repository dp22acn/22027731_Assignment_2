import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def read_csv_data(filename):
    """
    Read and process a CSV file containing country-level indicator data, and return two pandas dataframes: 
    one with years as columns and countries as rows, and the other with countries as columns and years as rows.

    Parameters:
    ----------
    filename: str
        A string representing the path of the CSV file to be read.

    Returns:
    --------
    dfYears: pandas DataFrame
        A pandas DataFrame in which the rows represent countries and the columns represent years, with the values 
        being the indicator values for each country-year combination. 
    dfCountries: pandas DataFrame
        A pandas DataFrame in which the rows represent years and the columns represent countries, with the values 
        being the indicator values for each country-year combination.
    """
    # Read the given csv file, except the first four unwanted rows
    ccDf = pd.read_csv(filename, skiprows=4)

    # drop unnecessary columns
    ccDf = ccDf.drop(columns=['Country Code', 'Indicator Code', 'Unnamed: 66'])

    # melt the dataframe and use pivot_table to create the desired dataframe format
    ccDf = ccDf.melt(
        id_vars=['Country Name', 'Indicator Name'], var_name='Year', value_name='Value')
    ccDf = ccDf.pivot_table(values='Value', columns='Indicator Name', index=[
                            'Country Name', 'Year']).reset_index()

    # drop null values from both the rows and columns
    ccDf = ccDf.dropna(thresh=int(0.25 * ccDf.shape[0]), axis=1)
    ccDf = ccDf.dropna(thresh=int(0.25 * ccDf.shape[1]))

    # set years as columns
    dfYears = ccDf.set_index(['Year', 'Country Name']).unstack(
        level=0).swaplevel(axis=1).sort_index(axis=1, level=0)

    # set countries as columns
    dfCountries = ccDf.set_index(['Year', 'Country Name']).unstack(
        level=1).swaplevel(axis=1).sort_index(axis=1, level=0)

    return dfYears, dfCountries
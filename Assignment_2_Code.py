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


dfYears, dfCountries = read_csv_data("worldBankData.csv")

countries = ['United States', 'Greece', 'Lower middle income',
             'Pacific island small states', 'Dominican Republic']
indicators = [
    'Electricity production from natural gas sources (% of total)',
    'CO2 intensity (kg per kg of oil equivalent energy use)',
    'Annual freshwater withdrawals, total (billion cubic meters)',
    'Population growth (annual %)',
    'Energy use (kg of oil equivalent) per $1,000 GDP (constant 2017 PPP)',
    'Agricultural land (sq. km)',
    'Agricultural land (% of land area)',
    'Foreign direct investment, net inflows (% of GDP)',
    'School enrollment, primary and secondary (gross), gender parity index (GPI)'
]

df = dfYears[[str(i) for i in range(1990, 2019)]
             ].unstack().unstack(level=1).reset_index()
df = df[df["Country Name"].isin(
    countries)][indicators+['Country Name', 'Year']].reset_index(drop=True)


# create a new column for mortality rate categories
df['Electricity NG Categories'] = pd.cut(df['Electricity production from natural gas sources (% of total)'], bins=[
                                         0, 25, 50, 75, 100], labels=['Very Low', 'Low', 'Medium', 'High'])

# create a horizontal bar plot
ax = sns.barplot(x='Population growth (annual %)',
                 y='Electricity NG Categories', data=df, hue='Country Name')
plt.savefig('eng.png')

# create a pivot dataframe using two features for creating a stacked bar plot
pd.crosstab(pd.cut(df['School enrollment, primary and secondary (gross), gender parity index (GPI)'],
            10), df['Country Name']).plot.bar(stacked=True)
plt.savefig('ct.png')

# create a multiple line plot
sns.lineplot(x='Year', y='CO2 intensity (kg per kg of oil equivalent energy use)',
             hue='Country Name', data=df[df.Year.isin([str(i) for i in range(1990, 2016, 5)])])
plt.savefig('co2.png')

# create a multiple line plot
sns.lineplot(x='Year', y='Energy use (kg of oil equivalent) per $1,000 GDP (constant 2017 PPP)',
             hue='Country Name', data=df[df.Year.isin([str(i) for i in range(1990, 2016, 5)])])

# Let us select data of Agricultural land for three years 1995, 2005 and 2015 and save the dataframe as csv
col = 'Agricultural land (% of land area)'
agDf = dfYears[[('1995', col), ('2005', col), ('2015', col)]].loc[countries]
agDf.columns = agDf.columns.droplevel(1)
agDf.to_csv('table.csv')

# create a bar plot for the agricultural land and save it
ax = sns.barplot(x='Country Name', y='Agricultural land (% of land area)', hue='Year',
                 data=dfYears[['1990', '1995', '2000', '2005', '2010', '2015']].loc[countries].unstack().unstack(level=1).reset_index())
plt.xticks(fontsize=5)
plt.savefig('al.png')

# generate a heatmap for Greece and save it
ax = sns.heatmap(dfCountries['Greece'][indicators].corr(), annot=True)
ax.set_title("Correlation Matrix for Greece")
plt.savefig('corrGreece.png')

# generate a heatmap for Dominican Republic and save it
ax = sns.heatmap(dfCountries['Dominican Republic']
                 [indicators].corr(), annot=True)
ax.set_title("Correlation Matrix for Dominican Republic")
plt.savefig('corrDR.png')
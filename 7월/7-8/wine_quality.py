import pandas as pd

red_df = pd.read_csv('winequality-red.csv', header = 0, engine ='python')
#print(red_df)
white_df = pd.read_csv('winequality-white.csv', header = 0, engine ='python')
#print(white_df)

red_df.insert(0, column='type', value='red')
# print(red_df.head())
# print(red_df.shape)

white_df.insert(0, column='type', value='white')
# print(white_df.head())
# print(white_df.shape)

wine = pd.concat([red_df, white_df])
# print(wine.shape)
# print(wine.head())
# print(wine.tail())

#wine.to_csv('wine.csv', index = False)

print(wine.info())

wine.columns = wine.columns.str.replace(' ', '_')
print(wine.head())
print(wine.describe())

print(sorted(wine.quality.unique()))
print(wine.quality.value_counts())

print( wine.groupby('type')['quality'].describe() )
print( wine.groupby('type')['quality'].mean() )
print( wine.groupby('type')['quality'].std() )
print( wine.groupby('type')['quality'].agg(['mean', 'std']) )

from scipy import stats
from statsmodels.formula.api import ols

red_wine_quality = wine.loc[wine['type'] == 'red', 'quality']
#print( red_wine_quality )
white_wine_quality = wine.loc[wine['type'] == 'white', 'quality']
#print( white_wine_quality )

print( stats.ttest_ind(red_wine_quality, white_wine_quality, equal_var = False) )

Rformula = 'quality ~ fixed_acidity + volatile_acidity + citric_acid + \
residual_sugar + chlorides + free_sulfur_dioxide + total_sulfur_dioxide + \
density + pH + sulphates + alcohol'

regression_result = ols(Rformula, data = wine).fit()
print( regression_result.summary() )
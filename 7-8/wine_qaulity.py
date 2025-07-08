import pandas as pd

red_df = pd.read_csv('winequality-red.csv', header = 0, engine = 'python')
#print(red_df)
white_df = pd.read_csv('winequality-white.csv', header = 0, engine = 'python')
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
from statsmodels.formula.api import ols, glm

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

# 품질 예측
sample1 = wine[wine.columns.difference(['quality', 'type'])]
sample1 = sample1[0:5][:]
#print( sample1 )

sample1_predict = regression_result.predict(sample1)
print(sample1_predict)
print( wine[0:5]['quality'] )

data = {"fixed_acidity" : [8.5, 8.1],
        "volatile_acidity":[0.8, 0.5],
        "citric_acid":[0.3, 0.4],
        "residual_sugar":[6.1, 5.8],
        "chlorides":[0.055, 0.04],
        "free_sulfur_dioxide":[30.0, 31.0],
        "total_sulfur_dioxide":[98.0, 99],
        "density":[0.996, 0.91],
        "pH":[3.25, 3.01],
        "sulphates":[0.4, 0.35],
        "alcohol":[9.0, 0.88] }

sample2 = pd.DataFrame(data, columns=sample1.columns)
#print(sample2)
sample2_predict = regression_result.predict(sample2)
print(sample2_predict)

# 결과 시각화
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')
sns.distplot(red_wine_quality, kde = True, color = "red", label = 'red wine')
sns.distplot(white_wine_quality, kde = True, color = "blue", label = 'white wine')
plt.title("Quality of wine Type")
plt.legend()
#plt.show()

# 부분 회귀플롯으로 시각화 하기
import statsmodels.api as sm
others = list(set(wine.columns).difference(set(["quality", "fixed_acidity"])))
p, resids = sm.graphics.plot_partregress("quality", "fixed_acidity", \
                                         others, data = wine, ret_coords = True)

fig = plt.figure(figsize = (8, 13))
print(fig)
sm.graphics.plot_partregress_grid(regression_result, fig = fig)
plt.show()

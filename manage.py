import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ma'lumotlarni yuklash
df = pd.read_csv('your_data.csv')

# Ma'lumotlarni o'rganish
print(df.head())
print(df.describe())
print(df.info())

# Vizualizatsiyalar
# Histograma
plt.figure(figsize=(10, 6))
sns.histplot(df['your_column'])
plt.title('Your Column Distribution')
plt.show()

# Pairplot
sns.pairplot(df)
plt.show()

# Correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

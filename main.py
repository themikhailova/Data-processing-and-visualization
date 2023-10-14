import pandas as pd

# данные
df1 = pd.read_excel('all.xlsx')
df2 = pd.read_excel('composite.xlsx')

df1['id'] = range(1, len(df1) + 1)

# соединение по столбцу "Код ОКН" и "Код объекта"
merged_df = df1.merge(df2, left_on='Код ОКН', right_on='Код объекта', how='outer')
merged_df['Код ОКН'] = merged_df['Код ОКН'].fillna(merged_df['Код объекта'])
merged_df.drop('Код объекта', axis=1, inplace=True)

# порядок колонок
new_order = ['id'] + [col for col in merged_df.columns if col != 'id']
merged_df = merged_df[new_order]

merged_df.to_excel('data.xlsx', index=False)

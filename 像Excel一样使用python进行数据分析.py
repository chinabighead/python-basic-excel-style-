# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 21:39:54 2017

@author: n7171
"""

############像Excel一样使用python进行数据分析################
########http://www.cnblogs.com/nxld/p/6756492.html#########




import numpy as np
import pandas as pd
#导入数据表
df=pd.DataFrame(pd.read_csv('E:\jjl.csv',names=['a','b','c','d']))
df_2=pd.read_table('E:\jjl_test_w.txt',names=['a','b','c','d','aa','bb','cc','dd'])
df=pd.DataFrame(pd.read_excel('name.xlsx'))
#创建数据表
df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
                   "date":pd.date_range('20130102', periods=6),
                   "city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
                   "age":[23,44,54,32,34,32],
                   "category":['100-A','100-B','110-A','110-C','210-A','130-F'],
                   "price":[1200,np.nan,2133,5433,np.nan,4432]},
                   columns =['id','date','city','category','age','price'])

#查看数据表的维度
df.shape
#数据表信息
df.info()
df.describe()
#obj=pd.Series(['a','a','b','c']*4)
#obj.describe()
#查看数据表各列格式
df.dtypes
#查看单列格式
df['id'].dtype


#检查数据空值
df.isnull()
#检查特定列空值
df['price'].isnull()
#查看city列中的唯一值
df['city'].unique()
#查看数据表的值
df.values
#查看列名称
df.columns
#查看前3行数据
df.head(3)
#查看最后3行
df.tail(3)
#删除数据表中含有空值的行
df.dropna(how='any')
df.drop('city',axis=1)
df.drop(1)
#使用数字0填充数据表中空值
df.fillna(value=0)
#使用price均值对NA进行填充
df['price']=df['price'].fillna(df['price'].mean())
#清除city字段中的字符空格 
df['city']=df['city'].map(str.strip)
#更改数据格式
df['price'].astype('int')
#更改列名称
df.rename(columns={'category': 'category-size'})
#df.reindex(,axis=1)
df['city']
#删除后出现的重复值
df['city'].drop_duplicates()
#删除先出现的重复值
df['city'].drop_duplicates(keep='last')
#数据替换
df['city'].replace('sh', 'shanghai')

#4，数据预处理
#创建df1数据表
df1=pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006,1007,1008],
"gender":['male','female','male','female','male','female','male','female'],
"pay":['Y','N','Y','Y','N','Y','N','Y',],
"m-point":[10,12,20,40,40,40,30,20]})
#数据表匹配合并，inner模式
df_inner=pd.merge(df,df1,how='inner') #join
#其他数据表匹配模式
df_left=pd.merge(df,df1,how='left')
df_right=pd.merge(df,df1,how='right')
df_outer=pd.merge(df,df1,how='outer')
#设置索引列
df_inner=df_inner.set_index('id')
#按特定列的值排序
df_inner.sort_values(by=['age'])
#按索引列排序
df_inner.sort_index()
#如果price列的值>3000，group列显示high，否则显示low
df_inner['group'] = np.where(df_inner['price'] > 3000,'high','low') #case when
#对复合多个条件的数据进行分组标记
#df_inner.loc[(df_inner['gender'] == 'male') & (df_inner['price'] >= 3000), 'sign']=1
df_inner['sign'] = np.where((df_inner['gender'] == 'male') & (df_inner['price'] >= 3000),1,0) #case when
#对category字段的值依次进行分列，并创建数据表，索引值为df_inner的索引列，列名称为category和size
split=pd.DataFrame((x.split('-') for x in df_inner['category']),index=df_inner.index,columns=['category','size'])
#将完成分列后的数据表与原df_inner数据表进行匹配
df_inner=pd.merge(df_inner,split,right_index=True, left_index=True) #on

#5，数据提取
#按索引提取单行的数值
df_inner.loc[3]
#按索引提取区域行数值
df_inner.loc[0:5]
#重设索引
df_inner.reset_index()
#设置日期为索引
df_inner=df_inner.set_index('date')
#提取4日之前的所有数据
df_inner[:'2013-01-04']
#使用iloc按位置区域提取数据
df_inner.iloc[:3,:2]
#使用iloc按位置单独提取数据
df_inner.iloc[[0,2,5],[4,5]]
#使用ix按索引标签和位置混合提取数据

df_inner=df_inner.sort_values(by=['city'])
df_inner.ix[:'2013-01-03',:4]
#判断city列的值是否为beijing
df_inner['city'].isin(['beijing'])
#先判断city列里是否包含beijing和shanghai，然后将复合条件的数据提取出来。
df_inner.loc[df_inner['city'].isin(['beijing','shanghai'])]
category=df_inner['category']
pd.DataFrame(category.str[:3])

#6，数据筛选
#使用“与”条件进行筛选
df_inner.loc[(df_inner['age'] > 25) & (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']]
#使用“或”条件筛选
df_inner.loc[(df_inner['age'] > 25) | (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']].sort_values(by=['age'])
df_inner.loc[(df_inner['age'] > 25) | (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']].sort_values(by=['age']).age.mean()
#使用“非”条件进行筛选
df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort_values(by=['id'])
#使用query函数进行筛选
df_inner.query('city == ["beijing", "shanghai"]')
#对筛选后的结果按price进行求和
df_inner.query('city == ["beijing", "shanghai"]').price.sum()

#7，数据汇总
#对所有列进行计数汇总
df_inner.groupby('gender').count()
#对特定的列进行计数汇总
df_inner.groupby('gender')['id'].count()
df_inner.groupby('gender')['age'].sum()
df_inner.groupby('gender').sum()
#对两个字段进行汇总计数
a=df_inner.groupby(['gender','pay'])['id'].count()
#对city字段进行汇总并计算price的合计和均值。
df_inner.groupby('gender')['price'].agg([len,np.sum, np.mean])
#数据透视表
pd.pivot_table(df_inner,index=["city"],values=["price"],columns=["pay"],aggfunc=[len,np.sum],fill_value=0,margins=True)


#8，数据统计
#简单的数据采样
df_inner.sample(n=3)
#手动设置采样权重
weights = [0, 0, 0, 0, 0.5, 0.5]
df_inner.sample(n=2, weights=weights)
#采样后不放回
df_inner.sample(n=6, replace=False)
#采样后放回
df_inner.sample(n=6, replace=True)

#数据表描述性统计
df_inner.describe().round(2).T
#标准差
df_inner['price'].std()
#两个字段间的协方差
df_inner['price'].cov(df_inner['m-point'])
#相关性分析
df_inner.cov()
#相关性分析
df_inner['price'].corr(df_inner['m-point'])

#输出到excel格式
df_inner.to_excel('excel_to_python.xlsx', sheet_name='bluewhale_cc')
#输出到CSV格式
df_inner.to_csv('E:/excel_to_python.csv')


#创建数据表
df = pd.DataFrame({"id":[1001,1002,1003,1004,1005,1006],
"date":pd.date_range('20130102', periods=6),
"city":['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
"age":[23,44,54,32,34,32],
"category":['100-A','100-B','110-A','110-C','210-A','130-F'],
"price":[1200,np.nan,2133,5433,np.nan,4432]},
columns =['id','date','city','category','age','price'])

#创建自定义函数
def table_info(x):
    shape=x.shape
    types=x.dtypes
    colums=x.columns
    print("数据维度(行，列):\n",shape)
    print("数据格式:\n",types)
    print("列名称:\n",colums)
#调用自定义函数获取df数据表信息并输出结果
table_info(df)








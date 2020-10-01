
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


df = pd.read_csv("/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject/exonerations.csv")

display(df.head(5))


df = df.drop(['lastname', 'firstname', 'state', 'region', 'statefips', 'pctopposedeathpenalty', 'pctcourtstooharsh',
       'stateabbr','statepop', 'county', 'postingdate', 'date_witnessreform', 'date_recordinginterrog', 'sentence', 'date_postconvictiondna'], 1)



df['yearsSentenced'] = df['exonerated'] - df['convicted']
df = df.drop(['convicted', 'exonerated'], 1)
df = df.dropna()


ax = sns.stripplot(x=df['race'], y=df['yearsSentenced'], data=df)
races = ['White', 'Black', 'N. American', 'Hispanic', 'Other', 'Asian']
ax.set_xticklabels(races, rotation=45)
ax.set_xlabel("Race")
ax.set_title("Racial Disparities in Sentencing Length")


df['race'].value_counts()

#Creating dummy variables for categorical variables (sex, race, worstcrime)
target = df[['yearsSentenced']]
dummies = pd.get_dummies(df['sex']).rename(columns=lambda x: 'Sex_' + str(x))
df = pd.concat([df, dummies], axis=1)
df = df.drop(['sex'], 1)

dummies2 = pd.get_dummies(df['race']).rename(columns=lambda x: 'Race_' + str(x))
df = pd.concat([df, dummies2], axis=1)
df = df.drop(['race'], 1)

dummies3 = pd.get_dummies(df['worstcrime']).rename(columns=lambda x: 'C_' + str(x))
df = pd.concat([df, dummies3], axis=1)
df = df.drop(['worstcrime'], 1)

#list the current columns in the dataframe
df.columns

display(df.head(5))


#Standardization: Only standardize the continous variables to the range [0,1] and keep the binary variables as is
from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
df[['age', 'yearsSentenced']] = mms.fit_transform(df[['age', 'yearsSentenced']]) #only scale the continous variables, leave binary variables [0,1]


#check the data types of all the columns
df.dtypes


from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


pca = PCA(n_components=14)
pca.fit(df)


#As a general rule, try to keep 80% of the variance so we choose  14 pc's
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.ylim(0.0,1.0)
plt.xlim(0,23)
plt.title('Explained Variance by Number of Components')

pca_explained_var = pca.explained_variance_ratio_
print(sum(pca_explained_var)) #82% of the variance is explained with 14 vars, 93% with 20 variables


#We need only the calculated resulting components scores for the elements in our data set
scores_pca = pca.transform(df)
#scores_pca.shape #(2649, 14), the number of PCA componetns 



#you are asking it to project each row of your data into the vector space that was learned when fit was called
#incorporate the newly obtained PCA scores in the K-means algorithm. 
#That’s how we can perform segmentation based on principal components scores instead of the original features.

#Fit K-means using the transformed PCA data 
wccs = []
for i in range(1, 15): #number of clusters we are testing
    kmeans_pca = KMeans(n_clusters=i, random_state=0)
    kmeans_pca.fit(scores_pca)
    wccs.append(kmeans_pca.inertia_) #Sum of squared distances of samples to their closest cluster center.
    

plt.figure(figsize=(10,8))
plt.plot(range(1,15),wccs, marker='o', linestyle='--')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.title('K-Means Clustering with PCA')
plt.show()
#4 clusters (elbow) is appropriate

kmeans_pca = KMeans(n_clusters=4, random_state=0)
kmeans_pca.fit(scores_pca)

df_pca_kmeans = pd.concat([df.reset_index(drop=True), pd.DataFrame(scores_pca)],axis=1) #used 14 components
df_pca_kmeans.columns.values[-14:] = ['Component 1', 'Component 2','Component 3','Component 4',
                                      'Component 5','Component 6','Component 7','Component 8',
                                      'Component 9','Component 10','Component 11','Component 12',
                                      'Component 13','Component 14']


df_pca_kmeans['Cluster_Assignment'] = kmeans_pca.labels_ #Labels of each point from clusters

display(df_pca_kmeans.head(5))


df_pca_kmeans['Cluster_Assignment'].value_counts()



df_pca_kmeans['Segment'] = df_pca_kmeans['Cluster_Assignment'].map({0:'first', 1: 'second', 
                                                                   2:'third', 3: 'fourth'
                                                                    }) 


#Plot Data by the principal components, Y axis is the first component and X axis is the second component 
x_axis = df_pca_kmeans['Component 2']
y_axis = df_pca_kmeans['Component 1']
plt.figure(figsize=(10,8))
sns.scatterplot(x_axis, y_axis, hue=df_pca_kmeans['Segment'], palette='deep')
plt.title('Clusters by PCA Components')
plt.show()


##PCA Results: Most important features in the first 2 principle components
col_name_list = df.columns

# number of components
n_pcs= pca.components_.shape[0]
# get the index of the most important feature on EACH component
pc_0 =  np.abs(pca.components_[0])
pca_sorted = np.flip(np.argsort(pc_0)) #from largest to smallest
#argsort returns the indeces that would sort the array

pc_1=  np.abs(pca.components_[1])
pca_sorted_1 = np.flip(np.argsort(pc_1))

most_important_1_features = []
for i in pca_sorted_1:
  most_important_1_features.append(col_name_list[i])


most_important_0_features = []
for i in pca_sorted:
  most_important_0_features.append(col_name_list[i])

print(most_important_0_features[:10])
print(most_important_1_features[:10])
##The important features are the ones that influence more the components and thus, have a large absolute value/score on the component.


cluster_0 = df_pca_kmeans.loc[df_pca_kmeans['Cluster_Assignment'] == 0]
cluster_1 = cluster_0 = df_pca_kmeans.loc[df_pca_kmeans['Cluster_Assignment'] == 1]

cluster_2 = cluster_0 = df_pca_kmeans.loc[df_pca_kmeans['Cluster_Assignment'] == 2]

cluster_3 = cluster_0 = df_pca_kmeans.loc[df_pca_kmeans['Cluster_Assignment'] == 3]


df_stats = df_pca_kmeans.describe()
df_stats.to_csv('/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject/dfStats.csv')


cluster_0.shape #(514, 76) observations x features
cluster0_stats = cluster_0.describe()
cluster0_stats.to_csv('/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject/cluster_0.csv')
cluster_0['Race_Black'].value_counts()/cluster_0.shape[0]


cluster1_stats = cluster_1.describe()
cluster1_stats.to_csv('/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject/cluster_1.csv')
cluster_1['Race_Black'].value_counts()/cluster_1.shape[0]


cluster2_stats = cluster_2.describe()
cluster2_stats.to_csv('/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject/cluster_2.csv')
cluster_2['Race_Black'].value_counts()/cluster_2.shape[0]


cluster3_stats = cluster_3.describe()
cluster3_stats.to_csv('/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject/cluster_3.csv')
cluster_3['Race_Black'].value_counts()/cluster_3.shape[0]


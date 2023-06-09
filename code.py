#!/usr/bin/env python
# coding: utf-8

# ---
# 
# # **Part I: Research Question**
# 
# ## Research Question
# 
# My dataset for this data mining exercise includes data on a telco company’s current and former subscribers, with an emphasis on customer churn (whether customers are maintaining or discontinuing their subscription to service).  Data analysis performed on the dataset will be aimed with this research question in mind: can I use k-means clustering to identify a customer's likelihood to churn based on the continuous numerical data included in the dataset?  Continuous numerical data will include numerical data which includes a measurable variable, rather than numerical data used as a label.

# ---
# 
# ## Objectives and Goals
# 
# Conclusions gleaned from the analysis of this data can benefit stakeholders by revealing information on how customers can be grouped based on their characteristics.  Such information may be used to predict future customer events based on another variable the telco company may be interested in.  My goal will be to determine if the results of my k-means clustering exercise might be useful in predicting which customers are more or less likely to churn.

# ---
# 
# # **Part II: Technique Justification**
# 
# ## K-means Clustering
# 
# K-means clustering is an unsupervised learning algorithm.  It helps to group similar data points (rows in a data set) together, while attempting to maintain distance between each cluster to eliminate overlap.  Before beginning the clustering process there must be a known value for "k".  This value reflects the number of clusters to be generated by the algorithm (Nagar, 2020).
# 
# The expected outcome will be "k" clusters, in this case groups of customers, with a similar number of customers in each cluster.  The clusters should group together customers with similar characteristics, and analysis of the clusters should reveal which characteristics are most prevalent in each cluster.
# 
# One assumption of k-means clustering is that the resulting clusters will be similar in size.  This assumption helps in determing where the boundaries of each cluster should be and how many data points should make up its members (Perceptive Analytics, 2017).  K-means also assumes the clusters will be of a generally spherical shape, as the data points within a cluster would only fall within a specified maximum distance from its center (Nagar, 2020).

# ---
# 
# ## Tool Selection
# 
# All code execution was carried out via Jupyter Lab, using Python 3.  I used Python as my selected programming language due to prior familiarity and broader applications when considering programming in general.  R is a very strong and robust language tool for data analysis and statistics but finds itself somewhat limited to that niche role (Insights for Professionals, 2019).  I utilized the NumPy, Pandas, and Matplotlib libraries to perform many of my data analysis tasks, as they are among the most popular Python libraries employed for this purpose and see widespread use.  Seaborn is included primarily for its versatility and pleasing aesthetics when created visulizations.  
# 
# Beyond these libraries, I relied upon the scikit-learn library.  Scikit-learn supports k-means clustering, variable scaling, accuracy scoring and principal component analysis (KMeans, StandardScaler, silhouette_score and PCA functions, respectively), and the course material relied upon its use.  I also used the parallel_coordinates function from pandas' plotting module for use in creating visualizations for the purpose of analyzing k-means clustering results.

# In[1]:


# Imports and housekeeping
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from pandas.plotting import parallel_coordinates


# ---
# 
# # **Part III: Data Preparation**
# 
# ## Data Preparation Goals and Data Manipulations
# 
# I would like my data to include only variables relevant to my research question, and to be clean and free of missing values and duplicate rows.  K-means clustering can only operate on continuous variables, so my first goal in data preparation is to make sure the data I will be working with contains no categorical data.
# 
# 
# A list of the variables I will be using for my analysis is included below, along with their variable types and a brief description of each.
# 
# * Population - **continuous** - *Population within a mile radius of customer*
# * Children - **continuous** - *Number of children in customer’s household*
# * Age - **continuous** - *Age of customer*
# * Income - **continuous** - *Annual income of customer*
# * Outage_sec_perweek - **continuous** - *Average number of seconds per week of system outages in the customer’s neighborhood*
# * Email - **continuous** - *Number of emails sent to the customer in the last year*
# * Contacts - **continuous** - *Number of times customer contacted technical support*
# * Yearly_equip_failure - **continuous** - *The number of times customer’s equipment failed and had to be reset/replaced in the past year*
# * Tenure - **continuous** - *Number of months the customer has stayed with the provider*
# * MonthlyCharge - **continuous** - *The amount charged to the customer monthly*
# * Bandwidth_GB_Year - **continuous** - *The average amount of data used, in GB, in a year by the customer*
# * Item1: Timely response - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# * Item2: Timely fixes - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# * Item3: Timely replacements - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# * Item4: Reliability - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# * Item5: Options - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# * Item6: Respectful response - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# * Item7: Courteous exchange - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# * Item8: Evidence of active listening - **continuous** - *survey response - scale of 1 to 8 (1 = most important, 8 = least important)*
# 
# ---
# 
# 
# My first steps will be to import the complete data set and execute functions that will give me information on its size and the data types of its variables.  I will then narrow the data set to a new dataframe containing only the variables I am concerned with, and then utilize functions to determine if any null values or duplicate rows exist.  By using the index_col parameter in my import I utilize CaseOrder, the data set's natural index column, as the index column in my pandas dataframe.

# In[2]:


# Import the main dataset
df = pd.read_csv('churn_clean.csv', dtype={'locationid':np.int64}, index_col=[0])


# In[3]:


# Display dataset info
df.info()


# In[4]:


# Display dataset top 5 rows
df.head()


# In[5]:


# Trim data set to variables relevant to research question
columns = ['Population', 'Children', 'Age', 'Income', 'Outage_sec_perweek', 'Email', 'Contacts', 
           'Yearly_equip_failure', 'Tenure', 'MonthlyCharge', 'Bandwidth_GB_Year', 'Item1', 'Item2', 
           'Item3', 'Item4', 'Item5', 'Item6', 'Item7', 'Item8']
df_data = pd.DataFrame(df[columns])
# Store the data set in variable 'X'
X = df_data


# In[6]:


# Check data for null or missing values
df_data.isna().any()


# In[7]:


# Check data for duplicated rows
df_data.duplicated().sum()


# In[8]:


df_data.head()


# ---
# 
# ## Summary Statistics
# 
# I can use the describe() function to display the summary statistics for the entire dataframe, as well as each variable I'll be evaluating for inclusion in the k-means clustering exercise.

# In[9]:


# Display summary statistics for entire dataset - continuous variables
df_data.describe()


# ---
# 
# ## Further Preparation Steps
# 
# I will use the StandardScaler function to scale my variables for more accurate attribute weighting.  StandardScaler transforms each variable value to have a mean of 0 and a variance of 1.  Once done, every variable value will fall between -1 and 1, and the data set values can be considered "standardized".  The standardized data set is then assigned to variable "X_scaled".

# In[10]:


# Scaling continuous variables with StandardScaler
scaler = StandardScaler()
scaler.fit(X)
StandardScaler(copy=True, with_mean=True, with_std=True)
X_scaled = scaler.transform(X)


# ---
# 
# ## Copy of Prepared Data Set
# 
# Below is the code used to export the prepared data set to CSV format.

# In[11]:


df_prepared = pd.DataFrame(X_scaled, columns=df_data.columns)
# Export prepared dataframe to csv
df_prepared.to_csv(r'C:\Users\wstul\d212\churn_clean_prepared.csv')


# ---
# 
# # **Part IV: Analysis**
# 
# ## Determining the Optimal Value for "k"
# 
# Using the best "k" value, or number of clusters, is critical in order to receive good results from the clustering.  With 19 features, this data frame is more likely to benefit from a lower "k" value.  I will use an iterative loop to help ultimately determine which value is best, but before doing that I will need to initialize a couple of arrays.  The first array contains the numbers 1-10, and will represent the k values used in the iterative loop.  The second array will be empty, intended to store the results from each iteration.

# In[12]:


# Initializing the kvalues and inertia arrays
kvalues = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
inertia = np.array([])


# ---
# 
# ## Iterative Loop and Inertia Values
# 
# The iterative loop will run the k-means algorithm for "i" number of clusters, "i" being each number in the "kvalues" array.  It will then fit the model to X_scaled, our standardized data set, print the resulting inertia value, and then add that inertia value to the "inertia" array.

# In[13]:


# Iterative loop to determine best k value
for i in kvalues:
    kmeans = KMeans(n_clusters=i)
    kmeans.fit(X_scaled)
    print(kmeans.inertia_)
    # At the end of each loop the inertia observed during clustering is added to the inertia array
    inertia = np.append(inertia, kmeans.inertia_)


# ---
# 
# Being able to see the inertia values is good, but generating a visualization based on the inertia values and their related "k" values will be more helpful in spotting the optimal value for "k".  The below code will generate that visualization.

# In[14]:


# Create a figure containing a single axes.
fig, ax = plt.subplots()
# Plot the kvalue and inertia data on the axes.
ax.plot(inertia, kvalues);


# ---
# 
# I can see that the "elbow" in the visualization falls at the "k" value 4, indicating 4 is the optimal value of "k" for this data set.  I can then run the k-means algorithm specifying a "k" value of 4, and use the results to create clusters using KMeans.predict().

# In[15]:


# k-means for 4 clusters
kmeans = KMeans(n_clusters=4)
kmeans.fit(X_scaled)
print(kmeans.inertia_)
clusters = kmeans.predict(X_scaled)


# ---
# 
# ## Data Analysis Process
# 
# I will use the series of functions documented below to create visualizations based on the k-means clusters, which will allow me to better analyze the results.
# 
# * display_factorial_planes - utilizes matplotlib to generate a scatter plot on a factorial plane, one for each factorial plane, and highlight cluster centroids
# * display_parallel_coordinates - utilizes matplotlib to display a parallel coordinates plot for the clusters
# * display_parallel_coordinates_centroids - utilizes matplotlib to display a parallel coordinates plot for the centroids
# * addAlpha - used to manipulate color and opacity

# In[16]:


def display_factorial_planes(X_projected, n_comp, pca, axis_ranks, labels=None, alpha=1, illustrative_var=None):
    # Display a scatter plot on a factorial plane, one for each factorial plane

    # For each factorial plane
    for d1,d2 in axis_ranks:
        if d2 < n_comp:
 
            # Initialise the matplotlib figure      
            fig = plt.figure(figsize=(7,6))
        
            # Display the points
            if illustrative_var is None:
                plt.scatter(X_projected[:, d1], X_projected[:, d2], alpha=alpha)
            else:
                illustrative_var = np.array(illustrative_var)
                for value in np.unique(illustrative_var):
                    selected = np.where(illustrative_var == value)
                    plt.scatter(X_projected[selected, d1], X_projected[selected, d2], alpha=alpha, label=value)
                plt.legend()

            # Display the labels on the points
            if labels is not None:
                for i,(x,y) in enumerate(X_projected[:,[d1,d2]]):
                    plt.text(x, y, labels[i],
                              fontsize='14', ha='center',va='center') 
                
            # Define the limits of the chart
            boundary = np.max(np.abs(X_projected[:, [d1,d2]])) * 1.1
            plt.xlim([-boundary,boundary])
            plt.ylim([-boundary,boundary])
        
            # Display grid lines
            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            # Label the axes, with the percentage of variance explained
            plt.xlabel('PC{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('PC{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Projection of points (on PC{} and PC{})".format(d1+1, d2+1))
            #plt.show(block=False)


# In[17]:


def display_parallel_coordinates(df, num_clusters):
    # Display a parallel coordinates plot for the clusters 

    # Select data points for individual clusters
    cluster_points = []
    for i in range(num_clusters):
        cluster_points.append(df[df.cluster==i])
    
    # Create the plot
    fig = plt.figure(figsize=(16, 15))
    title = fig.suptitle("Parallel Coordinates Plot for the Clusters", fontsize=18)
    fig.subplots_adjust(top=0.95, wspace=0)

    # Display one plot for each cluster, with the lines for the main cluster appearing over the lines for the other clusters
    for i in range(num_clusters):    
        plt.subplot(num_clusters, 1, i+1)
        for j,c in enumerate(cluster_points): 
            if i!= j:
                pc = parallel_coordinates(c, 'cluster', color=[addAlpha(palette[j],0.2)])
        pc = parallel_coordinates(cluster_points[i], 'cluster', color=[addAlpha(palette[i],0.5)])

        # Stagger the axes
        ax=plt.gca()
        for tick in ax.xaxis.get_major_ticks()[1::2]:
            tick.set_pad(20)


# In[18]:


def display_parallel_coordinates_centroids(df, num_clusters):
    # Display a parallel coordinates plot for the centroids

    # Create the plot
    fig = plt.figure(figsize=(16, 5))
    title = fig.suptitle("Parallel Coordinates plot for the Centroids", fontsize=18)
    fig.subplots_adjust(top=0.9, wspace=0)

    # Draw the chart
    parallel_coordinates(df, 'cluster', color=palette)

    # Stagger the axes
    ax=plt.gca()
    for tick in ax.xaxis.get_major_ticks()[1::2]:
        tick.set_pad(20)


# In[19]:


def addAlpha(colour, alpha):
    # Add an alpha to the RGB colour
    
    return (colour[0],colour[1],colour[2],alpha)


# ---
# 
# My feature set currently has 19 dimensions, too many to visualize.  Using principal component analysis I can narrow this down to 2 and create a new data frame with the PCA results, adding my cluster labels as an additional column.

# In[20]:


# Create a PCA model to reduce our data to 2 dimensions for visualisation
pca = PCA(n_components=2)
pca.fit(X_scaled)

# Transform the scaled data to the new PCA space
X_reduced = pca.transform(X_scaled)

# Convert to a data frame
X_reduceddf = pd.DataFrame(X_reduced, index=X.index, columns=['PC1','PC2'])
X_reduceddf['cluster'] = clusters

X_reduceddf.head()


# I will use PCA again on my cluster centers so I can have them appear as part of the visualized clusters as well.

# In[21]:


centers_reduced = pca.transform(kmeans.cluster_centers_)


# Using the display_factorial_planes function I can view the clusters and their centroids in a scatter plot and observe if any significant overlap has occurred.

# In[22]:


display_factorial_planes(X_reduced, 2, pca, [(0,1)], illustrative_var = clusters, alpha = 0.8)
plt.scatter(centers_reduced[:, 0], centers_reduced[:, 1],
            marker='s', color='w', zorder=10)


# I'll add the cluster labels, the numbers 0-3, to my standardized data set in a new data frame, "X_clustered".  I can then see the distribution of variables in each cluster by using parallel coordinates plots.

# In[23]:


# Add the cluster number to the original scaled data
X_clustered = pd.DataFrame(X_scaled, index=X.index, columns=X.columns)
X_clustered["cluster"] = clusters

# Display parallel coordinates plots, one for each cluster
palette = sns.color_palette("bright", 10)
display_parallel_coordinates(X_clustered, 4)


# The parallel coordinates plots reveal a great deal about which features are represented in each cluster, and to what degree.  Drilling down further, I can use the same type of plot to view the centroids for each cluster.

# In[24]:


# Create a data frame containing our centroids
centroids = pd.DataFrame(kmeans.cluster_centers_, columns=X.columns)
centroids['cluster'] = centroids.index

display_parallel_coordinates_centroids(centroids, 10)


# ---
# 
# # **Part V: Data Summary and Implications**
# 
# ## Clustering Accuracy
# 
# I used the silhouette_score function to judge the accuracy of the k-means clustering.

# In[25]:


# compute an average silhouette score for each point and print the score
silhouette_score_average = silhouette_score(X_scaled, kmeans.predict(X_scaled))
print(silhouette_score_average)


# The score was .076 rounded up.  The score is above 0, which indicates above average accuracy, but may also improve with adjustments to the "k" value used in the algorithm.

# ---
# 
# ## Summary of Findings
# 
# The k-means algorithm identified 4 clusters.  Clusters exhibit uniformity across the Population, Children, Age, Income, Outage_sec_perweek, Email, Contacts, and Yearly_equip_failure variables.  For the Tenure, Bandwidth_GB_Year, and Item1 - Item8 variables, we begin to see significant divergence from the mean.  Characteristics of the clusters are listed below.
# 
# * Cluster 0 - Low Tenure, Bandwidth_GB_Year, Items 1, 2, 3, and 6 
# * Cluster 1 - High Tenure and Bandwidth_GB_Year, High Items 1, 2, 3, 6 and 7 
# * Cluster 2 - High Tenure and Bandwidth_GB_Year, Low Items 1, 2, 3 and 6
# * Cluster 3 - Low Tenure and Bandwidth_GB_Year, High Items 1, 2, 3 and 6
# 
# ---
# 
# ## Limitations
# 
# The most significant limitation when using k-means clustering is its restriction to numerical data.  While I am able to use the results of the clustering to compare against categorical variables, I cannot use those variables in the process of creating the clusters unless they are re-expressed as numerical.
# 
# ## Recommended Course of Action
# 
# My recommendation to the business team would be to explore further data analysis of a more predictive nature using the cluster data.
# 
# One example of this might be to see if one or more customer clusters are more likely to churn.  For example, the cluster labels, in this case the numbers 0-3, can be added to the original data set.

# In[26]:


df_clusters = pd.read_csv('churn_clean.csv', dtype={'locationid':np.int64}, index_col=[0])
df_clusters['cluster'] = clusters


# In[27]:


df_clusters[['Customer_id','cluster']]


# Once available with the original set of features, a countplot reveals that customers in clusters 1 and 2 appear far less likely to churn, while customers in clusters 0 and 3 are equally likely to churn or not churn.

# In[28]:


sns.countplot(data=df_clusters, x="Churn", hue="cluster")


# ---
# 
# ## Conclusion
# 
# With an above average accuracy score and four distinct clusters, the exercise confirms a "yes" response to the research question "can I use k-means clustering to identify a customer's likelihood to churn based on the continuous numerical data included in the dataset?".

# ---
# 
# # **Part VI: Demonstration**
# 
# **Panopto Video Recording**
# 
# A link for the Panopto video has been provided separately.  The demonstration includes the following:
# 
# •  Demonstration of the functionality of the code used for the analysis
# 
# •  Identification of the version of the programming environment
# 

# ---
# 
# # **Web Sources**
# 
# https://openclassrooms.com/en/courses/5869986-perform-an-exploratory-data-analysis/6177861-analyze-the-results-of-a-k-means-clustering
# 
# https://enjoymachinelearning.com/blog/k-means-accuracy-python-silhouette/
# 
# https://stackoverflow.com/questions/36519086/how-to-get-rid-of-unnamed-0-column-in-a-pandas-dataframe-read-in-from-csv-fil
# 
# https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers
# 
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html
# 
# https://scikit-learn.org/stable/modules/clustering.html#k-means

# ---
# 
# # **References**
# 
# 
# Insights for Professionals. (2019, February 26). *5 Niche Programming Languages (And Why They're Underrated).* https://www.insightsforprofessionals.com/it/software/niche-programming-languages
# 
# 
# Nagar, Akanksha.  (2020, January 26).  *K-means Clustering — Everything you need to know.*  Medium.  https://medium.com/analytics-vidhya/k-means-clustering-everything-you-need-to-know-175dd01766d5#5ac5
# 
# 
# Perceptive Analytics.  (2017, August 7).  *Exploring Assumptions of K-means Clustering using R.*  R-bloggers.  https://www.r-bloggers.com/2017/08/exploring-assumptions-of-k-means-clustering-using-r/
# 

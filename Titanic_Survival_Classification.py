
# coding: utf-8

# In[2]:


# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')



# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier




# ## Workflow goals
# The data science solutions workflow solves for seven major goals.
# 
# ## Classifying. 
# We may want to classify or categorize our samples. We may also want to understand the implications or correlation of different classes with our solution goal.
# 
# ## Correlating. 
# One can approach the problem based on available features within the training dataset. Which features within the dataset contribute significantly to our solution goal? Statistically speaking is there a correlation among a feature and solution goal? As the feature values change does the solution state change as well, and visa-versa? This can be tested both for numerical and categorical features in the given dataset. We may also want to determine correlation among features other than survival for subsequent goals and workflow stages. Correlating certain features may help in creating, completing, or correcting features.
# 
# ## Converting.
# For modeling stage, one needs to prepare the data. Depending on the choice of model algorithm one may require all features to be converted to numerical equivalent values. So for instance converting text categorical values to numeric values.
# 
# ## Completing. 
# Data preparation may also require us to estimate any missing values within a feature. Model algorithms may work best when there are no missing values.
# 
# ## Correcting.
# We may also analyze the given training dataset for errors or possibly innacurate values within features and try to corrent these values or exclude the samples containing the errors. One way to do this is to detect any outliers among our samples or features. We may also completely discard a feature if it is not contribting to the analysis or may significantly skew the results.
# 
# ## Creating. 
# Can we create new features based on an existing feature or a set of features, such that the new feature follows the correlation, conversion, completeness goals.
# 
# ## Charting.
# How to select the right visualization plots and charts depending on nature of the data and the solution goals.

# Acquire data:
# 
# The Python Pandas packages helps us work with our datasets. We start by acquiring the training and testing datasets into Pandas DataFrames. We also combine these datasets to run certain operations on both datasets together.

# In[3]:


train_df = pd.read_csv('C:\\Users\\praya\\Data_Science\\Projects\\Titanic\\train.csv')
test_df = pd.read_csv('C:\\Users\\praya\\Data_Science\\Projects\\Titanic\\test.csv')
combine = [train_df, test_df]


# ## Analyze by describing data
# Pandas also helps describe the datasets answering following questions early in our project.

# In[4]:


print(train_df.columns.values)


# In[5]:


train_df.head(5)


# ## Which features are categorical?
# 
# These values classify the samples into sets of similar samples. Within categorical features are the values nominal, ordinal, ratio, or interval based? Among other things this helps us select the appropriate plots for visualization.
# 
# Categorical: Survived, Sex, and Embarked. Ordinal: Pclass.
# 
# ## Which features are numerical?
# 
# Which features are numerical? These values change from sample to sample. Within numerical features are the values discrete, continuous, or timeseries based? Among other things this helps us select the appropriate plots for visualization.
# 
# Continous: Age, Fare. Discrete: SibSp, Parch.

# ## Which features are mixed data types?
# 
# Numerical, alphanumeric data within same feature. These are candidates for correcting goal.
# 
# Ticket is a mix of numeric and alphanumeric data types. Cabin is alphanumeric.
# 
# ## Which features may contain errors or typos?
# 
# This is harder to review for a large dataset, however reviewing a few samples from a smaller dataset may just tell us outright, which features may require correcting.
# 
# Name feature may contain errors or typos as there are several ways used to describe a name including titles, round brackets, and quotes used for alternative or short names.

# In[6]:


train_df.tail()


# In[8]:


train_df.info()
print('_'*40)
test_df.info()


# ## Which features contain blank, null or empty values?
# 
# These will require correcting.
# 
# Cabin > Age > Embarked features contain a number of null values in that order for the training dataset.
# Cabin > Age are incomplete in case of test dataset.
# 
# ## What are the data types for various features?
# 
# Helping us during converting goal.
# 
# Seven features are integer or floats. Six in case of test dataset.
# Five features are strings (object).

# In[9]:


train_df.describe()


# ## What is the distribution of numerical feature values across the samples?
# 
# This helps us determine, among other early insights, how representative is the training dataset of the actual problem domain.
# 
# 1. Total samples are 891 or 40% of the actual number of passengers on board the Titanic (2,224).
# 2. Survived is a categorical feature with 0 or 1 values.
# 3. Around 38% samples survived representative of the actual survival rate at 32%.
# 4. Most passengers (> 75%) did not travel with parents or children.
# 5. Nearly 30% of the passengers had siblings and/or spouse aboard.
# 6. Fares varied significantly with few passengers (<1%) paying as high as $512.
# 7. Few elderly passengers (<1%) within age range 65-80.

# In[10]:


# Review survived rate using `percentiles=[.61, .62]` knowing our problem description mentions 38% survival rate.
# Review Parch distribution using `percentiles=[.75, .8]`
# SibSp distribution `[.68, .69]`
# Age and Fare `[.1, .2, .3, .4, .5, .6, .7, .8, .9, .99]`


# In[11]:


train_df.describe(include=['O'])


# ## What is the distribution of categorical features?
# 
# 1. Names are unique across the dataset (count=unique=891)
# 2. Sex variable as two possible values with 65% male (top=male, freq=577/count=891).
# 3. Cabin values have several dupicates across samples. Alternatively several passengers shared a cabin.
# 4. Embarked takes three possible values. S port used by most passengers (top=S)
# 5. Ticket feature has high ratio (22%) of duplicate values (unique=681).

# In[12]:


train_df.corr()


# ## Assumtions based on data analysis
# We arrive at following assumptions based on data analysis done so far. We may validate these assumptions further before taking appropriate actions.
# 
# ## Correlating.
# 
# We want to know how well does each feature correlate with Survival. We want to do this early in our project and match these quick correlations with modelled correlations later in the project.
# 
# ## Completing.
# 
# 1. We may want to complete Age feature as it is definitely correlated to survival.
# 2. We may want to complete the Embarked feature as it may also correlate with survival or another important feature.
# 
# ## Correcting.
# 
# 1. Ticket feature may be dropped from our analysis as it contains high ratio of duplicates (22%) and there may not be a correlation between Ticket and survival.
# 2. Cabin feature may be dropped as it is highly incomplete or contains many null values both in training and test dataset.
# 3. PassengerId may be dropped from training dataset as it does not contribute to survival.
# 4. Name feature is relatively non-standard, may not contribute directly to survival, so maybe dropped.
# 
# ## Creating.
# 
# 1. We may want to create a new feature called Family based on Parch and SibSp to get total count of family members on board.
# 2. We may want to engineer the Name feature to extract Title as a new feature.
# 3. We may want to create new feature for Age bands. This turns a continous numerical feature into an ordinal categorical feature.
# 4. We may also want to create a Fare range feature if it helps our analysis.
# 
# ## Classifying.
# 
# We may also add to our assumptions based on the problem description noted earlier.
# 
# 1. Women (Sex=female) were more likely to have survived.
# 2. Children (Age<?) were more likely to have survived.
# 3. The upper-class passengers (Pclass=1) were more likely to have survived

# ## Analyze by pivoting features
# To confirm some of our observations and assumptions, we can quickly analyze our feature correlations by pivoting features against each other. We can only do so at this stage for features which do not have any empty values. It also makes sense doing so only for features which are categorical (Sex), ordinal (Pclass) or discrete (SibSp, Parch) type.
# 
# 1. Pclass We observe significant correlation (>0.5) among Pclass=1 and Survived (classifying #3). We decide to include this feature in our model.
# 2. Sex We confirm the observation during problem definition that Sex=female had very high survival rate at 74% (classifying #1).
# 3. SibSp and Parch These features have zero correlation for certain values. It may be best to derive a feature or a set of features from these individual features (creating #1).

# In[13]:


train_df[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[14]:


train_df[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[15]:


train_df[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# In[16]:


train_df[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# ## Analyze by visualizing data
# Now we can continue confirming some of our assumptions using visualizations for analyzing the data.
# 
# ## Correlating numerical features
# Let us start by understanding correlations between numerical features and our solution goal (Survived).
# 
# A histogram chart is useful for analyzing continous numerical variables like Age where banding or ranges will help identify useful patterns. The histogram can indicate distribution of samples using automatically defined bins or equally ranged bands. This helps us answer questions relating to specific bands (Did infants have better survival rate?)
# 
# Note that x-axis in historgram visualizations represents the count of samples or passengers.
# 
# ## Observations.
# 
# 1. Infants (Age <=4) had high survival rate.
# 2. Oldest passengers (Age = 80) survived.
# 3. Large number of 15-25 year olds did not survive.
# 4. Most passengers are in 15-35 age range.
# 
# ## Decisions.
# 
# This simple analysis confirms our assumptions as decisions for subsequent workflow stages.
# 
# 1. We should consider Age (our assumption classifying #2) in our model training.
# 2. Complete the Age feature for null values (completing #1).
# 3. We should band age groups (creating #3).

# In[17]:


g = sns.FacetGrid(train_df, col='Survived')
g.map(plt.hist, 'Age', bins=20)


# In[18]:


# grid = sns.FacetGrid(train_df, col='Pclass', hue='Survived')
grid = sns.FacetGrid(train_df, col='Survived', row='Pclass', size=2.2, aspect=1.6)
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend();


# ## Correlating numerical and ordinal features
# We can combine multiple features for identifying correlations using a single plot. This can be done with numerical and categorical features which have numeric values.
# 
# ## Observations.
# 
# 1. Pclass=3 had most passengers, however most did not survive. Confirms our classifying assumption #2.
# 2. Infant passengers in Pclass=2 and Pclass=3 mostly survived. Further qualifies our classifying assumption #2.
# 3. Most passengers in Pclass=1 survived. Confirms our classifying assumption #3.
# 4. Pclass varies in terms of Age distribution of passengers.
# 
# ## Decisions.
# 
# Consider Pclass for model training.

# In[19]:


# grid = sns.FacetGrid(train_df, col='Embarked')
grid = sns.FacetGrid(train_df, row='Embarked', size=2.2, aspect=1.6)
grid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette='deep')
grid.add_legend()


# ## Correlating categorical features
# Now we can correlate categorical features with our solution goal.
# 
# ## Observations.
# 
# 1. Female passengers had much better survival rate than males. Confirms classifying (#1).
# 2. Exception in Embarked=C where males had higher survival rate. This could be a correlation between Pclass and Embarked and in turn Pclass and Survived, not necessarily direct correlation between Embarked and Survived.
# 3. Males had better survival rate in Pclass=3 when compared with Pclass=2 for C and Q ports. Completing (#2).
# 4. Ports of embarkation have varying survival rates for Pclass=3 and among male passengers. Correlating (#1).
# 
# ## Decisions.
# 
# 1. Add Sex feature to model training.
# 2. Complete and add Embarked feature to model training.

# In[20]:


# grid = sns.FacetGrid(train_df, col='Embarked', hue='Survived', palette={0: 'k', 1: 'w'})
grid = sns.FacetGrid(train_df, row='Embarked', col='Survived', size=2.2, aspect=1.6)
grid.map(sns.barplot, 'Sex', 'Fare', alpha=.5, ci=None)
grid.add_legend()


# ## Correlating categorical and numerical features
# We may also want to correlate categorical features (with non-numeric values) and numeric features. We can consider correlating Embarked (Categorical non-numeric), Sex (Categorical non-numeric), Fare (Numeric continuous), with Survived (Categorical numeric).
# 
# ## Observations.
# 
# Higher fare paying passengers had better survival. Confirms our assumption for creating (#4) fare ranges.
# Port of embarkation correlates with survival rates. Confirms correlating (#1) and completing (#2).
# 
# ## Decisions.
# 
# Consider banding Fare feature.

# ## Wrangle data
# We have collected several assumptions and decisions regarding our datasets and solution requirements. So far we did not have to change a single feature or value to arrive at these. Let us now execute our decisions and assumptions for correcting, creating, and completing goals.
# 
# ## Correcting by dropping features
# This is a good starting goal to execute. By dropping features we are dealing with fewer data points. Speeds up our notebook and eases the analysis.
# 
# 1. Based on our assumptions and decisions we want to drop the Cabin (correcting #2) and Ticket (correcting #1) features.
# 
# 2. Note that where applicable we perform operations on both training and testing datasets together to stay consistent.

# In[21]:


print("Before", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

train_df = train_df.drop(['Ticket', 'Cabin'], axis=1)
test_df = test_df.drop(['Ticket', 'Cabin'], axis=1)
combine = [train_df, test_df]

"After", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape


# ## Creating new feature extracting from existing
# We want to analyze if Name feature can be engineered to extract titles and test correlation between titles and survival, before dropping Name and PassengerId features.
# 
# In the following code we extract Title feature using regular expressions. The RegEx pattern (\w+\.) matches the first word which ends with a dot character within Name feature. The expand=False flag returns a DataFrame.
# 
# ## Observations.
# 
# When we plot Title, Age, and Survived, we note the following observations.
# 
# Most titles band Age groups accurately. For example: Master title has Age mean of 5 years.
# Survival among Title Age bands varies slightly.
# Certain titles mostly survived (Mme, Lady, Sir) or did not (Don, Rev, Jonkheer).
# 
# ## Decision.
# 
# We decide to retain the new Title feature for model training.

# In[22]:


for dataset in combine:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

pd.crosstab(train_df['Title'], train_df['Sex'])


# We can replace many titles with a more common name or classify them as Rare.

# In[23]:


for dataset in combine:
    dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col', 	'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')

    dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
    dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
    
train_df[['Title', 'Survived']].groupby(['Title'], as_index=False).mean()


# We can convert the categorical titles to ordinal.

# In[24]:


title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
for dataset in combine:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)

train_df.head()


# Now we can safely drop the Name feature from training and testing datasets. We also do not need the PassengerId feature in the training dataset.

# In[25]:


train_df = train_df.drop(['Name', 'PassengerId'], axis=1)
test_df = test_df.drop(['Name'], axis=1)
combine = [train_df, test_df]
train_df.shape, test_df.shape


# Converting a categorical feature
# Now we can convert features which contain strings to numerical values. This is required by most model algorithms. Doing so will also help us in achieving the feature completing goal.
# 
# Let us start by converting Sex feature to a new feature called Gender where female=1 and male=0.

# In[27]:


for dataset in combine:
    dataset['Sex'] = dataset['Sex'].map( {'female': 1, 'male': 0} ).astype(int)

train_df.head()


# ## Completing a numerical continuous feature
# Now we should start estimating and completing features with missing or null values. We will first do this for the Age feature.
# 
# We can consider three methods to complete a numerical continuous feature.
# 
# 1. A simple way is to generate random numbers between mean and standard deviation.
# 
# 2. More accurate way of guessing missing values is to use other correlated features. In our case we note correlation among Age, Gender, and Pclass. Guess Age values using median values for Age across sets of Pclass and Gender feature combinations. So, median Age for Pclass=1 and Gender=0, Pclass=1 and Gender=1, and so on...
# 
# 3. Combine methods 1 and 2. So instead of guessing age values based on median, use random numbers between mean and standard deviation, based on sets of Pclass and Gender combinations.
# 
# Method 1 and 3 will introduce random noise into our models. The results from multiple executions might vary. We will prefer method 2.

# In[28]:


# grid = sns.FacetGrid(train_df, col='Pclass', hue='Gender')
grid = sns.FacetGrid(train_df, row='Pclass', col='Sex', size=2.2, aspect=1.6)
grid.map(plt.hist, 'Age', alpha=.5, bins=20)
grid.add_legend()


# Let us start by preparing an empty array to contain guessed Age values based on Pclass x Gender combinations.

# In[30]:


guess_ages = np.zeros((2,3))
guess_ages


for dataset in combine:
    for i in range(0, 2):
        for j in range(0, 3):
            guess_df = dataset[(dataset['Sex'] == i) &                                   (dataset['Pclass'] == j+1)]['Age'].dropna()

            # age_mean = guess_df.mean()
            # age_std = guess_df.std()
            # age_guess = rnd.uniform(age_mean - age_std, age_mean + age_std)

            age_guess = guess_df.median()

            # Convert random age float to nearest .5 age
            guess_ages[i,j] = int( age_guess/0.5 + 0.5 ) * 0.5
            
    for i in range(0, 2):
        for j in range(0, 3):
            dataset.loc[ (dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == j+1),                    'Age'] = guess_ages[i,j]

    dataset['Age'] = dataset['Age'].astype(int)

train_df.head()


# Let us create Age bands and determine correlations with Survived.

# In[31]:


train_df['AgeBand'] = pd.cut(train_df['Age'], 5)

train_df[['AgeBand', 'Survived']].groupby(['AgeBand'], as_index=False).mean().sort_values(by='AgeBand', ascending=True)


# Let us replace Age with ordinals based on these bands.

# In[33]:


for dataset in combine:    
    dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
    dataset.loc[ dataset['Age'] > 64, 'Age']
train_df.head()


# We can not remove the AgeBand feature.

# In[35]:


train_df = train_df.drop(['AgeBand'], axis=1)
combine = [train_df, test_df]
train_df.head()


# ## Create new feature combining existing features
# We can create a new feature for FamilySize which combines Parch and SibSp. This will enable us to drop Parch and SibSp from our datasets.

# In[36]:


for dataset in combine:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1

train_df[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# We can create another feature called IsAlone.

# In[37]:


for dataset in combine:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1

train_df[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()


# Let us drop Parch, SibSp, and FamilySize features in favor of IsAlone.

# In[39]:


train_df = train_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
test_df = test_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
combine = [train_df, test_df]

train_df.head()


# We can also create an artificial feature combining Pclass and Age.

# In[40]:


for dataset in combine:
    dataset['Age*Class'] = dataset.Age * dataset.Pclass

train_df.loc[:, ['Age*Class', 'Age', 'Pclass']].head(10)


# ## Completing a categorical feature
# Embarked feature takes S, Q, C values based on port of embarkation. Our training dataset has two missing values. We simply fill these with the most common occurance.

# In[44]:


freq_port = train_df.Embarked.dropna().mode()[0]
freq_port


# In[45]:


for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].fillna(freq_port)
    
train_df[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean().sort_values(by='Survived', ascending=False)


# ## Converting categorical feature to numeric
# We can now convert the EmbarkedFill feature by creating a new numeric Port feature.

# In[46]:


for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)

train_df.head()


# ## Quick completing and converting a numeric feature
# We can now complete the Fare feature for single missing value in test dataset using mode to get the value that occurs most frequently for this feature. We do this in a single line of code.
# 
# Note that we are not creating an intermediate new feature or doing any further analysis for correlation to guess missing feature as we are replacing only a single value. The completion goal achieves desired requirement for model algorithm to operate on non-null values.
# 
# We may also want round off the fare to two decimals as it represents currency.

# In[47]:


test_df['Fare'].fillna(test_df['Fare'].dropna().median(), inplace=True)
test_df.head()


# We can now create a fare band

# In[50]:


train_df['FareBand'] = pd.qcut(train_df['Fare'], 4)
train_df[['FareBand', 'Survived']].groupby(['FareBand'], as_index=False).mean().sort_values(by='FareBand', ascending=True)


# Convert the Fare feature to ordinal values based on the FareBand.

# In[51]:


for dataset in combine:
    dataset.loc[ dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare']   = 2
    dataset.loc[ dataset['Fare'] > 31, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int)

train_df = train_df.drop(['FareBand'], axis=1)
combine = [train_df, test_df]
    
train_df.head(10)


# In[52]:


test_df.head(10)


# ## Model, predict and solve
# Now we are ready to train a model and predict the required solution. There are 60+ predictive modelling algorithms to choose from. We must understand the type of problem and solution requirement to narrow down to a select few models which we can evaluate. Our problem is a classification and regression problem. We want to identify relationship between output (Survived or not) with other variables or features (Gender, Age, Port...). We are also perfoming a category of machine learning which is called supervised learning as we are training our model with a given dataset. With these two criteria - Supervised Learning plus Classification and Regression, we can narrow down our choice of models to a few. These include:
# 
# 1. Logistic Regression
# 2. KNN or k-Nearest Neighbors
# 3. Support Vector Machines
# 4. Naive Bayes classifier
# 5. Decision Tree
# 6. Random Forrest
# 7. Perceptron
# 8. Artificial neural network
# 9. RVM or Relevance Vector Machine

# In[53]:


X_train = train_df.drop("Survived", axis=1)
Y_train = train_df["Survived"]
X_test  = test_df.drop("PassengerId", axis=1).copy()
X_train.shape, Y_train.shape, X_test.shape


# ## Logistic Regression:
# Logistic Regression is a useful model to run early in the workflow. Logistic regression measures the relationship between the categorical dependent variable (feature) and one or more independent variables (features) by estimating probabilities using a logistic function, which is the cumulative logistic distribution.
# 
# Note the confidence score generated by the model based on our training dataset.

# In[55]:


# Logistic Regression

logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
Y_pred = logreg.predict(X_test)
acc_log = round(logreg.score(X_train, Y_train) * 100, 2)
acc_log


# We can use Logistic Regression to validate our assumptions and decisions for feature creating and completing goals. This can be done by calculating the coefficient of the features in the decision function.
# 
# Positive coefficients increase the log-odds of the response (and thus increase the probability), and negative coefficients decrease the log-odds of the response (and thus decrease the probability).
# 
# 1. Sex is highest positivie coefficient, implying as the Sex value increases (male: 0 to female: 1), the probability of Survived=1 increases the most.
# 2. Inversely as Pclass increases, probability of Survived=1 decreases the most.
# 3. This way Age*Class is a good artificial feature to model as it has second highest negative correlation with Survived.
# So is Title as second highest positive correlation.

# In[58]:


coeff_df = pd.DataFrame(train_df.columns.delete(0))
coeff_df.columns = ['Feature']
coeff_df["Correlation"] = pd.Series(logreg.coef_[0])

coeff_df.sort_values(by='Correlation', ascending=False)


# ## SVM:
# Next we model using Support Vector Machines which are supervised learning models with associated learning algorithms that analyze data used for classification and regression analysis. Given a set of training samples, each marked as belonging to one or the other of two categories, an SVM training algorithm builds a model that assigns new test samples to one category or the other, making it a non-probabilistic binary linear classifier. 
# 
# Note that the model generates a confidence score which is higher than Logistics Regression model.

# In[59]:


# Support Vector Machines

svc = SVC()
svc.fit(X_train, Y_train)
Y_pred = svc.predict(X_test)
acc_svc = round(svc.score(X_train, Y_train) * 100, 2)
acc_svc


# ## KNN
# In pattern recognition, the k-Nearest Neighbors algorithm (or k-NN for short) is a non-parametric method used for classification and regression. A sample is classified by a majority vote of its neighbors, with the sample being assigned to the class most common among its k nearest neighbors (k is a positive integer, typically small). If k = 1, then the object is simply assigned to the class of that single nearest neighbor. 
# 
# KNN confidence score is better than Logistics Regression but worse than SVM.
# 
# 

# In[60]:


knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train, Y_train)
Y_pred = knn.predict(X_test)
acc_knn = round(knn.score(X_train, Y_train) * 100, 2)
acc_knn


# ## Naive Bayes
# In machine learning, naive Bayes classifiers are a family of simple probabilistic classifiers based on applying Bayes' theorem with strong (naive) independence assumptions between the features. Naive Bayes classifiers are highly scalable, requiring a number of parameters linear in the number of variables (features) in a learning problem. Reference Wikipedia.
# 
# The model generated confidence score is the lowest among the models evaluated so far.

# In[61]:


# Gaussian Naive Bayes

gaussian = GaussianNB()
gaussian.fit(X_train, Y_train)
Y_pred = gaussian.predict(X_test)
acc_gaussian = round(gaussian.score(X_train, Y_train) * 100, 2)
acc_gaussian


# ## Perceptron:
# The perceptron is an algorithm for supervised learning of binary classifiers (functions that can decide whether an input, represented by a vector of numbers, belongs to some specific class or not). It is a type of linear classifier, i.e. a classification algorithm that makes its predictions based on a linear predictor function combining a set of weights with the feature vector. The algorithm allows for online learning, in that it processes elements in the training set one at a time. Reference Wikipedia.

# In[62]:


# Perceptron

perceptron = Perceptron()
perceptron.fit(X_train, Y_train)
Y_pred = perceptron.predict(X_test)
acc_perceptron = round(perceptron.score(X_train, Y_train) * 100, 2)
acc_perceptron


# In[63]:


# Linear SVC

linear_svc = LinearSVC()
linear_svc.fit(X_train, Y_train)
Y_pred = linear_svc.predict(X_test)
acc_linear_svc = round(linear_svc.score(X_train, Y_train) * 100, 2)
acc_linear_svc


# In[64]:


# Stochastic Gradient Descent

sgd = SGDClassifier()
sgd.fit(X_train, Y_train)
Y_pred = sgd.predict(X_test)
acc_sgd = round(sgd.score(X_train, Y_train) * 100, 2)
acc_sgd


# ## Decision Tree
# This model uses a decision tree as a predictive model which maps features (tree branches) to conclusions about the target value (tree leaves). Tree models where the target variable can take a finite set of values are called classification trees; in these tree structures, leaves represent class labels and branches represent conjunctions of features that lead to those class labels. Decision trees where the target variable can take continuous values (typically real numbers) are called regression trees. Reference Wikipedia.
# 
# The model confidence score is the highest among models evaluated so far.

# In[65]:


# Decision Tree

decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, Y_train)
Y_pred = decision_tree.predict(X_test)
acc_decision_tree = round(decision_tree.score(X_train, Y_train) * 100, 2)
acc_decision_tree


# ## Random Forest
# The next model Random Forests is one of the most popular. Random forests or random decision forests are an ensemble learning method for classification, regression and other tasks, that operate by constructing a multitude of decision trees (n_estimators=100) at training time and outputting the class that is the mode of the classes (classification) or mean prediction (regression) of the individual trees. 
# 
# The model confidence score is the highest among models evaluated so far. 

# In[66]:


# Random Forest

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_train, Y_train)
acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
acc_random_forest


# ## Model evaluation
# We can now rank our evaluation of all the models to choose the best one for our problem. While both Decision Tree and Random Forest score the same, we choose to use Random Forest as they correct for decision trees' habit of overfitting to their training set.

# In[68]:


models = pd.DataFrame({
    'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression', 
              'Random Forest', 'Naive Bayes', 'Perceptron', 
              'Stochastic Gradient Decent', 'Linear SVC', 
              'Decision Tree'],
    'Score': [acc_svc, acc_knn, acc_log, 
              acc_random_forest, acc_gaussian, acc_perceptron, 
              acc_sgd, acc_linear_svc, acc_decision_tree]})
models.sort_values(by='Score', ascending=False)


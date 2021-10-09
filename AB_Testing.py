################################################################################
                            # AB_TESTING #
################################################################################

# Normality Assumption Check ====> shapiro test

# Checking Variance Homogeneity Assumption ====> levene test

# If assumptions are provided: Parametric Methods (mean)
# If assumptions are not provided: Nonparametric Methods (median)

# If the assumption of normality is met, but the assumption of homogeneity of variance is not
# In t test, an argument is entered to the t test function (equal_var=False).

# If the assumption of normality is not provided (even for 1 group), nonparametric test is performed.

# If p_value < 0.05, H0 is rejected.

# Ttest H0 hypothesis
# H0 = No significant difference between the two groups.

# Normality H0 hypothesis
# There is no significant difference between the theoretical normal distribution and the sample normal distribution.

# Variance Homogeneity H 0 hypothesis
# H0 = Variance distribution is homogeneous.


# TWO SAMPLES RATIO TEST(AB TESTING) (proportions_ztest)
# It is used to compare two rates (like conversion rate etc.)
# H0 hypothesis: There is no statistically significant difference between the two cases.
# Assumption;
# n1 > 30 (group 1 observation number)
# n2 > 30 (group 2 observations)


# Correlation Analysis Hypothesis
# H0 : p = 0 ==> There is no statistically significant correlation between the two variables.
# Correlation Analysis Assumptions
# Assumption of normality for both variables
# Pearson correlation coefficient if the assumption is met
# Spearman Correlation Coefficient if assumption is not met


################################################################################
                           # Data Preprocessing #
################################################################################

import pandas as pd
import numpy as np
from statsmodels.stats import proportion as pr
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import statsmodels.stats.api as sms
warnings.filterwarnings("ignore")


def check_data(dataframe, head=5):
    print ("####### SHAPE #######")
    print (dataframe.shape)
    print ("####### INFO #######")
    print (dataframe.info ())
    print ("####### DESCRIBE #######")
    print (dataframe.describe ([0.01, 0.1, 0.25, 0.50, 0.75, 0.9, 0.95, 0.99]))
    print ("####### NA VALUES #######")
    print (dataframe.isnull ().sum ())
    print ("####### FIRST {} ROWS #######".format (head))
    print (dataframe.head (head))


# Maximum Cost Bidding vs Average Cost Bidding
# https://incipia.co/post/app-marketing/facebook-ads-launches-average-cost-and-maximum-cost-bidding/

# Control Group (Maximum bidding)
control_df = pd.read_excel (r"C:\Users\hp\PycharmProjects\VBO\WEEK_05\ab_testing.xlsx", sheet_name="Control Group")

check_data(control_df)

sns.distplot(control_df["Purchase"], hist=False)      # Graphical observation of the normal distribution
plt.show()

# Test Group (Average_bidding)
test_df = pd.read_excel (r"C:\Users\hp\PycharmProjects\VBO\WEEK_05\ab_testing.xlsx", sheet_name="Test Group")

check_data(test_df)

sns.distplot(test_df["Purchase"], hist=False)        # Graphical observation of the normal distribution
plt.show();

desc_compare_df = pd.DataFrame({"Control_Purchase" : control_df["Purchase"].describe(),
              "Test_Purchase" : test_df["Purchase"].describe()})

desc_compare_df
# Although the mean and median of the test group were high,
# standard deviation is also high, so let's check if there is a significant difference.

earning_df = pd.DataFrame({"Control_Earning" : control_df["Earning"].describe(),
              "Test_Earning" : test_df["Earning"].describe()})
earning_df

# Confidence Interval Evaluation
sms.DescrStatsW(control_df["Purchase"]).tconfint_mean()
# (508.0041754264924, 593.7839421139709) 95% confidence interval values for the control group

sms.DescrStatsW(test_df["Purchase"]).tconfint_mean()
# (530.5670226990062, 633.6451705979289) Test group 95% confidence interval values


################################################################################
               # CONTROL GROUP NORMALITY ASSUMPTION CONTROL #
################################################################################

# H0 : There is no statistically significant difference between the theoretical normal
# distribution and the purchase sample normal distribution.
# H1 : There is a statistically significant difference between the theoretical normal
# distribution and the purchase normal distribution.

from scipy.stats import shapiro
ttest, p_value = shapiro(control_df["Purchase"])
print("ttest statistic: {}\np_value: {}".format(ttest, p_value))
# We cannot reject the H0 hypothesis because the p_value is greater than 0.05.
# Therefore, we can say that the control_df["Purchase"] values are normally distributed.


################################################################################
                     # TEST GROUP ASSUMPTION CONTROL #
################################################################################

# H0 : There is no statistically significant difference between the theoretical normal
# distribution and the purchase sample normal distribution.
# H1 : There is a statistically significant difference between the theoretical normal
# distribution and the purchase normal distribution.

from scipy.stats import shapiro
ttest, p_value = shapiro(test_df["Purchase"])
print("ttest statistic: {}\np_value: {}".format(ttest, p_value))
# We cannot reject the H0 hypothesis because the p_value is greater than 0.05.
# Therefore, we can say that the test_df["Purchase"] values are normally distributed.


################################################################################
                         # HOMOGENCY OF VARIANCE #
################################################################################

# H0: There is no statistically significant difference between the
# variance variance of the purchase variables of the 2 groups.
# H1: There is a statistically significant difference between the
# variance variance of the purchase variables of the 2 groups.

from scipy.stats import levene
ttest_lev, p_value_lev = levene(control_df["Purchase"], test_df["Purchase"])
print("ttest statistic: {}\np_value: {}".format(ttest_lev, p_value_lev))
# We cannot reject the H0 hypothesis because the p_value is greater than 0.05.
# Therefore, we can say that there is no statistically significant difference between the
# variance distributions of the purchase values of the 2 groups.


################################################################################
                     # INDEPENDENT TWO SAMPLE T TEST #
################################################################################

# Normality and Variance Homogeneity assumptions were met.
#      # H0: There is no statistically significant difference between the mean of the
#      purchase variable of the control group and the mean of the purchase variable of the test group.
#      # H1: There is a statistically significant difference between the mean of the
#      purchase variable of the control group and the mean of the purchase variable of the test group.

from scipy.stats import ttest_ind

ttest_ind, p_value_ind = ttest_ind(control_df["Purchase"], test_df["Purchase"], equal_var=True)
print("ttest statisticv: {}\np_value: {}".format(ttest_ind, p_value_ind))


# H0 cannot be rejected because the p_value is greater than 0.05.
# Therefore, we can say that there is no statistically significant difference between the
# mean purchase variable of the two groups.


################################################################################
                        # TWO SAMPLE RATIO TEST #
################################################################################

# H0 : There is no statistically significant difference between the
# control group purchase conversion rate and the test group purchase conversion rate.
# H1 : There is a statistically significant difference between the
# purchase conversion rate of the control group and the conversion rate of the test group.

control_df["Purchase"].shape[0]         # Observation count 40, n1>30 assumption provided.
test_df["Purchase"].shape[0]            # Observation count 40, n2>30 assumption provided.

control_df["Purchase"].sum()
control_df["Impression"].sum()

test_df["Purchase"].sum()
test_df["Impression"].sum()

from statsmodels.stats.proportion import proportions_ztest
basari_sayisi = np.array([control_df["Purchase"].sum(), test_df["Purchase"].sum()])
gozlem_sayisi = np.array([control_df["Impression"].sum(), test_df["Impression"].sum()])

ttest_z, p_value_z = proportions_ztest(basari_sayisi, gozlem_sayisi)
print("ttest statistic: {}\np_value: {:.10f}".format(ttest_z, p_value_z))
# H0 hypothesis is rejected because p_value is less than 0.05.
# In other words, there is a significant difference between the purchase conversion rates of the two groups.

control_df["Purchase"].sum()/control_df["Impression"].sum()
# The number of purchases per view in maximum bidding is better than average bidding.

test_df["Purchase"].sum()/test_df["Impression"].sum()
# This difference in conversion rates is in favor of the Control group(maximum_bidding), as we calculated above.


# 1) How would you describe the hypothesis of this A/B test?
# H0 : There is no statistically significant difference between the control group purchase
# conversion rate and the test group purchase conversion rate.
# H1 : There is a statistically significant difference between the purchase
# conversion rate of the control group and the conversion rate of the test group.

# 2) Can we draw statistically significant conclusions?
# When we look at the purchase conversion rate statistically, it is observed that the maximum_bidding conversion rate is higher,
# As a result of the observation in the two independent sample t-test, no significant difference was observed in the purchase numbers.

# 3) What test can be used? Why?
# The Two Sample Ratio Test can be used to compare conversion rates.

# 4) What is your advice to the client?
# Based on the conversion rate, since the conversion rate of maximum_bidding is statistically higher,
# I recommend maximum_bidding with the available data.


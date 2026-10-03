\# Customer Experience Root-Cause \& Experimentation Analytics



\## Overview



An end-to-end customer experience analytics project designed to identify factors associated with poor customer experience, quantify their statistical relationship, and translate the findings into a proposed experimentation strategy and business recommendation.



The project combines:



\* SQL analytics

\* Customer experience metrics

\* Root-cause analysis

\* Statistical hypothesis testing

\* Multivariate predictive modeling

\* Experiment design

\* Power analysis

\* Experiment simulation

\* Business impact analysis

\* Executive-style recommendations



The project uses the Brazilian E-Commerce Public Dataset by Olist.



> \*\*Important methodological note:\*\* The Olist dataset is observational. Historical relationships are interpreted as associations, not causal effects. No historical A/B test is claimed. The experiment section represents a proposed randomized experiment and a synthetic simulation.



\---



\## Business Problem



Customer experience can be affected by multiple operational factors such as delivery performance, seller behavior, order characteristics, and product categories.



The core business question is:



> \*\*What factors are associated with poor customer experience, and what intervention should the business test to improve it?\*\*



The analysis focuses on:



1\. Measuring the baseline customer experience.

2\. Identifying operational factors associated with poor experience.

3\. Quantifying the relationship between delivery performance and review outcomes.

4\. Controlling for seller, category, and order-value differences.

5\. Designing a statistically valid experiment.

6\. Estimating potential business impact.

7\. Translating analytical findings into a business recommendation.



\---



\# Project Pipeline



```text

Raw Olist Data

&#x20;     │

&#x20;     ▼

Data Validation

&#x20;     │

&#x20;     ▼

SQL Data Relationships

&#x20;     │

&#x20;     ▼

Customer Experience Metrics

&#x20;     │

&#x20;     ├──────────────► Delivery Analysis

&#x20;     │

&#x20;     ├──────────────► Category Analysis

&#x20;     │

&#x20;     └──────────────► Seller Analysis

&#x20;                        │

&#x20;                        ▼

&#x20;               Root-Cause Analysis

&#x20;                        │

&#x20;                        ▼

&#x20;             Statistical Hypothesis Tests

&#x20;                        │

&#x20;                        ▼

&#x20;            Multivariate Logistic Model

&#x20;                        │

&#x20;                        ▼

&#x20;                Experiment Design

&#x20;                        │

&#x20;                        ▼

&#x20;                  Power Analysis

&#x20;                        │

&#x20;                        ▼

&#x20;               Experiment Simulation

&#x20;                        │

&#x20;                        ▼

&#x20;               Business Impact Analysis

&#x20;                        │

&#x20;                        ▼

&#x20;             Business Recommendation

```



\---



\# Dataset



Source:



\*\*Brazilian E-Commerce Public Dataset by Olist\*\*



The analysis uses the following Olist tables:



\* Customers

\* Orders

\* Order Items

\* Order Payments

\* Order Reviews

\* Products

\* Sellers

\* Geolocation

\* Product Category Translation



The raw dataset is intentionally excluded from this repository through `.gitignore`.



\---



\# Customer Experience Definition



For the analysis, a \*\*poor customer experience\*\* is defined as:



```text

review\_score <= 2

```



This converts the customer review score into a business-oriented binary outcome suitable for:



\* segmentation

\* statistical testing

\* predictive modeling

\* experiment design

\* business impact estimation



\---



\# Baseline Customer Experience



Across the complete order population:



| Metric               | Result |

| -------------------- | -----: |

| Total orders         | 99,441 |

| Average review score |  4.086 |

| Poor-experience rate | 16.01% |

| Late-delivery rate   |  8.11% |

| Average order value  | 160.83 |



For the final controlled analysis population, after applying the representative seller/category methodology:



| Metric               | Result |

| -------------------- | -----: |

| Analysis orders      | 95,830 |

| Poor-experience rate | 12.77% |

| Late-delivery rate   |  8.00% |



\---



\# Data Quality \& Grain Validation



A key issue discovered during analysis was that the raw review table contains multiple review records for some orders.



Therefore, the project explicitly validates review grain before statistical analysis.



Observed:



\* Raw review rows: \*\*99,224\*\*

\* Unique reviewed orders: \*\*98,673\*\*

\* Additional review rows: \*\*551\*\*



To prevent duplicated review observations from biasing the analysis, the project creates an order-level review representation using the average review score per order.



This is an important analytical safeguard because customer-experience metrics should be evaluated at the appropriate business grain.



\---



\# Delivery \& Customer Experience Analysis



Delivery performance shows a strong relationship with customer review outcomes.



Among reviewed orders:



| Delivery Status | Orders | Avg Review | Poor Experience |

| --------------- | -----: | ---------: | --------------: |

| On-time / Early | 88,168 |      4.294 |          10.00% |

| 1–3 days late   |  1,852 |      3.291 |          37.67% |

| 4–7 days late   |  1,748 |      2.106 |          75.03% |

| 8–14 days late  |  1,447 |      1.672 |          87.86% |

| 15+ days late   |  2,615 |      2.856 |          51.99% |

| Unknown         |  2,843 |      1.753 |          84.41% |



The relationship is \*\*nonlinear\*\*, particularly because the 15+ day bucket does not continue the same monotonic pattern.



Therefore, the project avoids claiming that every additional day of delay necessarily produces a continuously increasing customer-experience effect.



\---



\# Statistical Analysis



\## Welch's t-test



The project compares average review scores between late and on-time/early deliveries.



Results:



\* Late-delivery mean: \*\*2.567\*\*

\* On-time/early mean: \*\*4.294\*\*

\* Difference: \*\*-1.728 review points\*\*

\* Welch t-statistic: \*\*-89.38\*\*

\* p-value: \*\*< 0.001\*\*

\* 95% CI: \*\*\[-1.766, -1.690]\*\*

\* Cohen's d: \*\*-1.45\*\*



The observed difference is statistically significant.



However:



> This is an observational association and should not be interpreted as proof that late delivery alone caused the lower review scores.



\---



\# Poor-Experience Association



For the binary poor-experience outcome:



\* Late-delivery poor-experience rate: \*\*53.98%\*\*

\* On-time/early poor-experience rate: \*\*9.19%\*\*

\* Relative risk: \*\*5.87\*\*

\* Odds ratio: \*\*11.59\*\*

\* Cramer's V: \*\*0.364\*\*

\* Chi-square: \*\*12,688.98\*\*

\* p-value: \*\*< 0.001\*\*



Interpretation:



> In this observational dataset, late-delivery orders had approximately \*\*5.87× the observed risk\*\* of being classified as poor experience compared with on-time/early orders.



This is an association, not a causal estimate.



\---



\# Root-Cause Modeling



To move beyond a simple two-group comparison, the project builds a multivariate logistic regression model.



\### Target



```text

poor\_experience = review\_score <= 2

```



\### Features



\* Late delivery

\* Log-transformed order value

\* Seller

\* Product category group



Categorical variables are encoded using one-hot encoding.



The model uses:



\* 80/20 stratified train-test split

\* StandardScaler

\* OneHotEncoder

\* L2-regularized Logistic Regression

\* Balanced class weights



\### Model Results



| Metric                 | Result |

| ---------------------- | -----: |

| Accuracy               |  0.778 |

| ROC-AUC                |  0.727 |

| PR-AUC                 |  0.367 |

| Poor-experience recall |  0.530 |

| Poor-experience F1     |  0.378 |



The model is intended primarily for \*\*analytical interpretation\*\*, rather than production deployment.



\### Delivery Effect



The late-delivery coefficient corresponds to modeled odds of approximately:



```text

Odds Ratio = 2.03

```



Interpretation:



> After controlling for order value, seller, and category in this model, late delivery is associated with approximately \*\*2.03× higher modeled odds\*\* of poor experience.



Again, this is observational and does not establish causality.



\---



\# Proposed Experiment



The historical dataset cannot prove whether an intervention will improve customer experience.



Therefore, the project converts the observational finding into a proposed randomized experiment.



\## Proposed intervention



Test a delivery-risk intervention for eligible orders, such as proactive operational intervention for orders predicted to have elevated delivery risk.



Potential intervention components could include:



\* earlier fulfillment escalation

\* proactive exception handling

\* delivery-risk monitoring

\* operational escalation for high-risk orders



The exact operational intervention would need to be validated by the business and fulfillment teams.



\---



\# Experiment Population



Eligible analysis population:



```text

95,830 orders

```



Observed baseline:



```text

Poor-experience rate = 12.77%

```



The experiment design uses:



\* Control group

\* Treatment group

\* Binary poor-experience outcome

\* Two-sided significance level

\* 80% statistical power



\---



\# Power Analysis



The design assumes a \*\*15% relative reduction\*\* in poor-experience rate.



\### Design assumptions



| Parameter                  |  Value |

| -------------------------- | -----: |

| Baseline rate              | 12.77% |

| Assumed relative reduction |    15% |

| Expected treatment rate    | 10.86% |

| Alpha                      |   0.05 |

| Statistical power          |   0.80 |

| Required control size      |  4,449 |

| Required treatment size    |  4,449 |

| Total required sample      |  8,898 |



The 15% reduction is a \*\*design assumption\*\*, not an observed historical result.



\---



\# Synthetic Experiment Simulation



A synthetic randomized experiment is simulated using the calculated sample size.



Simulation output:



| Metric              |                  Result |

| ------------------- | ----------------------: |

| Control rate        |                  12.36% |

| Treatment rate      |                  10.56% |

| Absolute difference | -1.80 percentage points |

| Relative change     |                 -14.55% |

| p-value             |                  0.0078 |



The simulated result is statistically significant under this particular synthetic draw.



> \*\*Important:\*\* This is a simulation, not an actual experiment conducted on customers.



\---



\# Business Impact



Using the observed eligible population of 95,830 orders and the 15% design assumption:



```text

Baseline poor-experience orders ≈ 12,240

Expected poor-experience orders after intervention ≈ 10,404

Expected reduction ≈ 1,836 orders

```



This represents a scenario estimate based on the assumed treatment effect.



It should not be presented as realized business impact.



\---



\# Volume Sensitivity



The project also evaluates the potential number of poor-experience orders avoided under different order volumes.



| Annual Orders | 10% Reduction | 15% Reduction | 20% Reduction |

| ------------: | ------------: | ------------: | ------------: |

|        10,000 |           128 |           192 |           255 |

|        50,000 |           639 |           958 |         1,277 |

|       100,000 |         1,277 |         1,916 |         2,555 |

|       500,000 |         6,386 |         9,579 |        12,773 |

|     1,000,000 |        12,773 |        19,159 |        25,545 |



These are scenario calculations rather than observed outcomes.



\---



\# Business Recommendation



The analysis identifies delivery performance as a strong observational signal associated with poor customer experience.



Therefore, the recommended next analytical step is \*\*not to immediately claim causality\*\*, but to validate the relationship through a controlled experiment.



The proposed decision process is:



```text

Identify high-risk delivery orders

&#x20;         ↓

Randomly assign eligible orders

&#x20;         ↓

Control vs Treatment

&#x20;         ↓

Measure poor-experience rate

&#x20;         ↓

Estimate treatment effect + confidence interval

&#x20;         ↓

Check statistical significance

&#x20;         ↓

Evaluate operational cost

&#x20;         ↓

Evaluate customer-experience improvement

&#x20;         ↓

Decide whether to scale

```



A production decision should consider both statistical evidence and operational economics.



\---



\# Key Analytical Lessons



\### 1. Business grain matters



Review duplication can materially distort customer-level metrics. The analysis explicitly validates order-level review grain before modeling.



\### 2. Association is not causation



Late delivery is strongly associated with poor experience, but observational data alone cannot establish a causal effect.



\### 3. Simple averages are insufficient



The analysis examines delivery buckets, seller effects, category effects, and a multivariate model rather than relying on one correlation.



\### 4. Statistical significance is not business impact



A statistically significant treatment effect still needs to be evaluated against implementation cost and operational feasibility.



\### 5. Experimentation converts analysis into a decision framework



The project moves from:



```text

"What happened?"

```



to:



```text

"What should we test?"

```



and finally:



```text

"How should we decide whether to scale it?"

```



\---



\# Repository Structure



```text

customer-experience-root-cause-experimentation/

│

├── .gitignore

├── README.md

│

├── reports/

│   ├── business\_recommendation.md

│   │

│   ├── business\_impact/

│   │   ├── business\_impact\_summary.csv

│   │   └── business\_impact\_scenarios.csv

│   │

│   ├── experiment/

│   │   ├── experiment\_population.csv

│   │   └── experiment\_simulation\_results.csv

│   │

│   └── model/

│       ├── root\_cause\_feature\_effects.csv

│       └── root\_cause\_model\_metrics.csv

│

├── sql/

│   ├── 01\_data\_relationships.sql

│   ├── 02\_customer\_experience\_base.sql

│   ├── 03\_delivery\_cx\_analysis.sql

│   ├── 04\_review\_grain\_validation.sql

│   ├── 05\_corrected\_delivery\_cx.sql

│   ├── 06\_statistical\_test\_data.sql

│   ├── 07\_poor\_experience\_test\_data.sql

│   ├── 08\_category\_root\_cause.sql

│   ├── 09\_seller\_root\_cause.sql

│   ├── 10\_seller\_delivery\_control.sql

│   ├── 11\_root\_cause\_model\_data.sql

│   └── 12\_experiment\_design.sql

│

├── src/

│   ├── inspect\_dataset.py

│   ├── run\_sql.py

│   ├── run\_customer\_experience\_sql.py

│   ├── run\_delivery\_cx.py

│   ├── run\_corrected\_delivery\_cx.py

│   ├── run\_review\_validation.py

│   ├── run\_statistical\_test.py

│   ├── run\_poor\_experience\_test.py

│   ├── run\_category\_root\_cause.py

│   ├── run\_seller\_root\_cause.py

│   ├── run\_seller\_delivery\_control.py

│   ├── run\_root\_cause\_model.py

│   ├── run\_experiment\_design.py

│   ├── run\_experiment\_power.py

│   ├── run\_experiment\_simulation.py

│   └── run\_business\_impact.py

│

└── tests/

&#x20;   └── test\_project3.py

```



Raw data and generated database files are intentionally excluded from Git.



\---



\# Reproducibility



Create and activate a virtual environment:



```bash

python -m venv .venv

```



Install dependencies:



```bash

python -m pip install pandas numpy scipy statsmodels scikit-learn matplotlib seaborn jupyter duckdb pytest

```



Run the test suite:



```bash

python -m pytest -q

```



Expected:



```text

6 passed

```



\---



\# Tech Stack



\### Programming



\* Python

\* SQL



\### Data Analysis



\* Pandas

\* NumPy

\* DuckDB



\### Statistics



\* SciPy

\* Statsmodels



\### Machine Learning



\* Scikit-learn

\* Logistic Regression



\### Visualization



\* Matplotlib

\* Seaborn



\### Engineering



\* Git

\* GitHub

\* Pytest



\---



\# Amazon Data Scientist Skill Mapping



This project intentionally demonstrates capabilities relevant to data-science internship work:



| Amazon DS-style capability     | Demonstrated in project                        |

| ------------------------------ | ---------------------------------------------- |

| Analytical modeling            | Logistic regression                            |

| Statistical analysis           | Welch test, chi-square, effect sizes           |

| Customer experience analysis   | Review-score and poor-experience metrics       |

| Identify predictors/causes     | Root-cause analysis and multivariate modeling  |

| Business problem solving       | Delivery/CX investigation                      |

| Experimentation                | Randomized experiment design                   |

| Forecasting/prediction mindset | Predictive modeling and intervention targeting |

| Quantitative decision making   | Power analysis and impact scenarios            |

| Written recommendations        | Business recommendation report                 |

| SQL analytics                  | Multi-table SQL analysis                       |

| Automation/reproducibility     | Python runners + tests                         |

| Business communication         | Executive-style recommendation                 |



\---



\# Limitations



1\. The dataset is observational.

2\. Historical associations cannot establish causality.

3\. Seller/category assignment uses a representative order-level methodology for analysis.

4\. The experiment has not actually been conducted.

5\. The 15% treatment effect is a design assumption.

6\. The experiment result is synthetic simulation.

7\. Business impact estimates depend on the assumed treatment effect.

8\. The project does not claim production deployment.



\---



\# Final Takeaway



This project demonstrates an end-to-end analytical workflow:



```text

SQL

&#x20; ↓

Customer Experience Metrics

&#x20; ↓

Root-Cause Analysis

&#x20; ↓

Statistical Testing

&#x20; ↓

Multivariate Modeling

&#x20; ↓

Experiment Design

&#x20; ↓

Power Analysis

&#x20; ↓

Simulation

&#x20; ↓

Business Impact

&#x20; ↓

Recommendation

```



The central analytical lesson is:



> \*\*Use observational data to identify and quantify signals, but use controlled experimentation to validate whether an intervention actually improves customer outcomes.\*\*




\# Customer Experience Root-Cause \& Experimentation Analytics



\## Executive Summary



This project analyzes customer-experience outcomes using the Brazilian Olist e-commerce dataset.



The primary business question is:



> What factors are associated with poor customer experience, and what intervention should the business test to improve it?



The analysis combines SQL analytics, customer-experience metrics, root-cause modeling, statistical testing, experiment design, power analysis, experiment simulation, and business-impact estimation.



The historical dataset contains 95,830 orders in the final experiment-analysis population.



The observed baseline poor-experience rate was 12.77%, corresponding to approximately 12,240 poor-experience orders.



Delivery performance showed a strong association with customer experience. In the observational dataset, late-delivery orders had substantially worse review outcomes than on-time/early orders.



A multivariate logistic-regression model was then used to control for order value, representative seller, and representative product category. Late delivery remained positively associated with poor experience, with modeled odds approximately 2.03 times higher than the reference condition.



Because the dataset is observational, these relationships are interpreted as associations rather than causal effects.



\---



\# 1. Business Problem



Customer experience can be affected by operational factors such as delivery delays, seller performance, order characteristics, and product categories.



The objective is to identify measurable predictors associated with poor customer experience and translate those findings into a testable business intervention.



The proposed intervention is:



> Proactively communicate expected delivery delays to customers and evaluate whether this reduces poor-experience outcomes.



The intervention is proposed for a future randomized experiment. It was not actually deployed in the historical Olist dataset.



\---



\# 2. Dataset



Source:



Brazilian Olist e-commerce dataset.



Relevant tables include:



\- orders

\- order\_items

\- order\_reviews

\- customers

\- sellers

\- products

\- product\_category\_name\_translation



The project performs order-level analysis while explicitly handling review duplication and multi-item orders.



\---



\# 3. Customer Experience Definition



The primary customer-experience outcome is:



```text

poor\_experience = average review score <= 2


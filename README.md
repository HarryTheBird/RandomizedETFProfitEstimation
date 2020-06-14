# RandomizedETFProfitEstimation
This tool implements a Monte-Carlo-Estimation based on randomized/empiric ETF (e.g. MSCI World) growth rates to estimate the profit given a monthly saving rate and an investment horizon.

Have you ever ask how much money you can earn through a monthly saving rate after a specified time? - This algorithm is an easy-to-understand-approach to estimate possible returns and compare it to a naive intrest-based investment.

Basically, the capital is build through a monthly saving rate. Profits of an investment rely on anual fluctuations of a choosen stock share. The development of the economy can be considered as a random process. The corresponding random variable is anually drawn from a distribution. The current implementations supports two approaches:
1) An uniform distribution between a lower expected value of economic growth (hyperparameter) and an upper value of economic growth. The latter one is computed by an expected anual growth rate (further hyperparameter).
2) A empiric Weibull-distribution is computed based on transformed historic data of the economy. 

The anual drawing of the growth rate as a random variable renders the observed return at the investment horizon a random variable itself. Rather than analytically estimate the expected return, a Monte-Carlo-Estimation is suggested.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

class EstimateGrowth():
    def __init__(self, csv_file='world_etf_data.csv'):
        self.data = pd.read_csv(csv_file, sep=',',header=None).values[:, 1]
        self.transformed_data = - self.data
        self.min = self.transformed_data.min()
        self.transformed_data = self.transformed_data - self.transformed_data.min()
        self.max = self.transformed_data.max()
        self.transformed_data = self.transformed_data / self.max
        self.xdata = np.linspace(self.transformed_data.min(), self.transformed_data.max(), 100)
        self.distribution = None
        self.simulated_data = []
    def illustrate(self, inverse_transform=True):  # True not well implemented
        if inverse_transform:
            #self.xdata = np.linspace(self.data.min(), self.data.max(), 100)
            data = self.distribution.pdf(self.xdata)
            xdata = -(self.xdata * self.max + self.min)
            plt.plot(xdata, data / 100, label='Weibull fit')
            _ = plt.hist(self.data, density=True, alpha=0.5, label='Historical distribution')
            if len(self.simulated_data) > 0:
                self.simulated_data = -(np.stack(self.simulated_data) * self.max + self.min)
                _ = plt.hist(self.simulated_data, density=True, alpha=0.5, label='Simulated distribution')
            plt.legend()
            plt.show()
        else:
            plt.plot(self.xdata, self.distribution.pdf(self.xdata), label='Weibull fit')
            _ = plt.hist(self.transformed_data, density=True, alpha=0.5, label='Historical distribution')
            if len(self.simulated_data) > 0:
                self.simulated_data = np.stack(self.simulated_data)
                _ = plt.hist(self.simulated_data, density=True, alpha=0.5, label='Simulated distribution')
            plt.legend()
            plt.show()
    def fit_weibull(self):
        self.distribution = stats.weibull_min(*stats.weibull_min.fit(self.transformed_data, 10, loc=0, scale=1))
        return self.distribution
    def sample(self, inverse_transform=True):
        data = self.distribution.rvs()
        self.simulated_data.append(data)
        if inverse_transform:
            data = -(data * self.max + self.min)
        return data

def EstimateInvestment(rate, dynamization, saving_years, interest=0.0, estimation_mode='uniform', expected_growth=3.0, lower_growth_bound=-2, initial_capital=0.0, admission_rate = 1.5, randomize_growth=True, monte_carlo_steps=10000, verbose=False):
    # pre-computations according to monte-carlo:
    if estimation_mode == 'data':
        growth_rate_sampler = EstimateGrowth()
        growth_rate_sampler.fit_weibull()
    monto_carlo_counter = 0
    monte_carlo_capital = []
    capital_list = []
    growth_list = []
    while monto_carlo_counter < monte_carlo_steps:
        capital = initial_capital
        naive_saving = initial_capital
        year_counter = 0
        for time_step in range(saving_years * 12):
            naive_saving += rate * (1 + dynamization/100) ** year_counter
            capital += rate * (1 - admission_rate / 100) * (1 + dynamization/100) ** year_counter
            if np.mod(time_step, 12) == 0 and time_step > 0:
                year_counter += 1
                naive_saving *= (1 + interest / 100)
                if randomize_growth:
                    upper_growth_bound = 2 * expected_growth - lower_growth_bound
                    # for monitoring, explicit computation:
                    if estimation_mode == 'uniform':
                        current_growth = np.random.uniform(low=lower_growth_bound, high=upper_growth_bound, size=None) / 100 + 1
                    elif estimation_mode == 'data':
                        current_growth = growth_rate_sampler.sample() / 100 + 1
                    else:
                        print('No valid estimation mode. Supported modes are uniform or data')
                        raise ValueError
                    capital *= current_growth
                    current_growth = np.round((current_growth - 1) * 100, 2)
                    growth_list.append(current_growth)
                    if monte_carlo_steps == 1:
                        print('Capital after ' + str(year_counter) + ' years: ' + str(np.round(capital, 2)) + '(€). Growth rate was ' + str(current_growth))
                else:
                    capital *= (1 + expected_growth / 100)
                    print('Capital after ' + str(year_counter) + ' years: ' + str(np.round(capital, 2)) + '(€)')
                capital_list.append(capital)
        if monte_carlo_steps > 1 and randomize_growth:
            monte_carlo_capital.append(capital)
            print('Capital in ' + str(monto_carlo_counter) + '-th MCS: ' + str(np.round(capital, 2)))
            monto_carlo_counter += 1
        else:
            monto_carlo_counter = monte_carlo_steps + 1
    if randomize_growth:
        if monte_carlo_steps == 1 or not randomize_growth:
            print('Capital at time horizon (' + str(saving_years) + ' years): ' + str(np.round(capital, 2)) + '(€)')
            print('Compare it to naive saving at investment horizon: ' + str(np.round(naive_saving, 2)) + '(€)')
        else:
            monte_carlo_capital = np.stack(monte_carlo_capital)
            print('Mean capital at time horizon (' + str(saving_years) + ' years): ' + str(np.round(monte_carlo_capital.mean(), 2)) + '(€) with standard deviation of ' + str(np.round(monte_carlo_capital.std(), 2)) + ' and effective ratio ' + str(np.round(monte_carlo_capital.mean() / naive_saving, 2)) + ' +/- ' + str(np.round(monte_carlo_capital.std() / naive_saving, 2)))
            print('Compare it to naive saving at investment horizon: ' + str(np.round(naive_saving, 2)) + '(€)')
    else:
        print('Capital at time horizon (' + str(saving_years) + ' years): ' + str(np.round(capital, 2)) + '(€) and a ratio of ' + str(np.round(capital / naive_saving, 2)))
        print('Compare it to naive saving at investment horizon: ' + str(np.round(naive_saving, 2)) + '(€)')
    if verbose:
        if monte_carlo_steps > 1 and randomize_growth:
            fig, ax = plt.subplots(1, 2)
            plt.sca(ax[0])
            plt.axvline(x=naive_saving, c='k', label='Baseline')
            plt.hist(monte_carlo_capital, bins=int(monte_carlo_steps/100), label='Absolute outcome')
            plt.legend()
            plt.xlabel('Capital [€]')
            plt.ylabel('Counts [1]')
            plt.grid()
            plt.sca(ax[1])
            plt.axvline(x=0.0, c='k', label='Baseline')
            plt.hist((monte_carlo_capital / naive_saving - 1) * 100, bins=int(monte_carlo_steps/100), label='Relative outcomes')
            plt.legend()
            plt.xlabel('Profit [%]')
            plt.ylabel('Counts [1]')
            plt.grid()
            plt.show()
        else:
            fig, ax = plt.subplots(1, 2)
            plt.sca(ax[0])
            baseline = [initial_capital + step * 12 * rate for step in range(saving_years)]
            plt.plot(baseline, c='k', label='Baseline')
            plt.plot(capital_list, label='Actual Capital [€]')
            plt.legend(loc='upper left')
            plt.xlabel('Time [a]')
            plt.ylabel('Capital [€]')
            plt.grid()
            plt.sca(ax[1])
            plt.axhline(y=expected_growth, c='k', label='Expected growth')
            plt.plot(growth_list, label='Simulated growth')
            plt.legend(loc='upper right')
            plt.xlabel('Time [a]')
            plt.ylabel('Growth rate [%]')
            plt.grid()
            plt.show()
    if estimation_mode == 'data':
        growth_rate_sampler.illustrate()
    if monte_carlo_steps > 1 and randomize_growth:
        return monte_carlo_capital, None, None
    elif monte_carlo_steps == 1:
        return capital, capital_list, growth_list
    else:
        return None, None, None


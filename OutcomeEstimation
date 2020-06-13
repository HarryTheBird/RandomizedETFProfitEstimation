import numpy as np
# parameter:
rate = 25.00  # monthly saving rate (euro)
admission_rate = 1.5  # admission rate (percent)
saving_years = 35  # time horizon to save (years)
initial_capital = 1000.0  # capital investment to start with (euro)
expected_growth = 3  # expected annual growth (mean value, percent)
randomize_growth = True  # sample from normal distribution
monte_carlo_steps = 1000
lower_growth_bound = 0

# pre-computations according to monte-carlo:
monto_carlo_counter = 0
monte_carlo_capital = []

naive_saving = rate * saving_years * 12 + initial_capital
while monto_carlo_counter < monte_carlo_steps:
    capital = initial_capital
    year_counter = 0
    for time_step in range(saving_years * 12):
        capital += rate * (1 - admission_rate / 100)
        if np.mod(time_step, 12) == 0:
            year_counter += 1
            if randomize_growth:
                upper_growth_bound = 2 * expected_growth - lower_growth_bound
                # for monitoring, explicit computation:
                current_growth = np.random.uniform(low=lower_growth_bound, high=upper_growth_bound, size=None) / 100 + 1
                capital *= current_growth
                current_growth = np.round((current_growth - 1) * 100, 2)
                if monte_carlo_steps == 1:
                    print('Capital after ' + str(year_counter) + ' years: ' + str(np.round(capital, 2)) + '(€). Growth rate was ' + str(current_growth))
            else:
                capital *= (1 + expected_growth / 100)
                print('Capital after ' + str(year_counter) + ' years: ' + str(np.round(capital, 2)) + '(€)')
    if monte_carlo_steps > 1 and randomize_growth:
        monte_carlo_capital.append(capital)
        print('Capital in ' + str(monto_carlo_counter) + '-th MCS: ' + str(np.round(capital, 2)))
        monto_carlo_counter += 1
    else:
        monto_carlo_counter = monte_carlo_steps + 1
if randomize_growth:
    if monte_carlo_steps == 1 or not randomize_growth:
        print('Capital at time horizon (' + str(saving_years) + ' years): ' + str(np.round(capital, 2)) + '(€)')
        print('Compare it to naive saving at time horizon: ' + str(np.round(rate * saving_years * 12, 2)) + '(€)')
    else:
        monte_carlo_capital = np.stack(monte_carlo_capital)
        print('Mean capital at time horizon (' + str(saving_years) + ' years): ' + str(np.round(monte_carlo_capital.mean(), 2)) + '(€) with standard deviation of ' + str(np.round(monte_carlo_capital.std(), 2)) + ' and effective ratio ' + str(np.round(monte_carlo_capital.mean() / naive_saving, 2)) + ' +/- ' + str(np.round(monte_carlo_capital.std() / naive_saving, 2)))
        print('Compare it to naive saving at time horizon: ' + str(np.round(rate * saving_years * 12, 2)) + '(€)')
else:
    print('Capital at time horizon (' + str(saving_years) + ' years): ' + str(np.round(capital, 2)) + '(€) and a ratio of ' + str(np.round(np.stack(capital).sum() / naive_saving, 2)))
    print('Compare it to naive saving at time horizon: ' + str(np.round(naive_saving, 2)) + '(€)')

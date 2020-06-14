from utils import *

# parameter:
rate = 700.0  # monthly saving rate (euro)
dynamization = 2  # Dynamisierungssatz (percent)
interest = 2.0  # Assumed interests for baseline
admission_rate = 1.5  # admission rate (percent)
saving_years = 30  # time horizon to save (years)
initial_capital = 1000.0  # capital investment to start with (euro)
# advanced:
expected_growth = 5.0  # expected annual growth (mean value, percent)
randomize_growth = True  # sample growth from uniform distribution with given lower bound and expected growth
estimation_mode = 'uniform'  # 'uniform' or 'data'
monte_carlo_steps = 10000
lower_growth_bound = -3
verbose = True

print('Starting...')
if monte_carlo_steps > 1 and randomize_growth:
    monte_carlo_capital, _, _ = \
        EstimateInvestment(rate, dynamization, saving_years, interest=interest, estimation_mode=estimation_mode, expected_growth=expected_growth, lower_growth_bound=lower_growth_bound, initial_capital=initial_capital,
                   admission_rate=admission_rate, randomize_growth=randomize_growth, monte_carlo_steps=monte_carlo_steps, verbose=verbose)
elif monte_carlo_steps == 1:
    capital, capital_list, growth_list = \
        EstimateInvestment(rate, dynamization, saving_years, interest=interest, estimation_mode=estimation_mode, expected_growth=expected_growth, lower_growth_bound=lower_growth_bound,
                       initial_capital=initial_capital,
                       admission_rate=admission_rate, randomize_growth=randomize_growth,
                       monte_carlo_steps=monte_carlo_steps, verbose=verbose)
else:
    EstimateInvestment(rate, dynamization, saving_years, interest=interest, estimation_mode=estimation_mode, expected_growth=expected_growth, lower_growth_bound=lower_growth_bound,
                       initial_capital=initial_capital,
                       admission_rate=admission_rate, randomize_growth=randomize_growth,
                       monte_carlo_steps=monte_carlo_steps, verbose=verbose)

print('... executed.')

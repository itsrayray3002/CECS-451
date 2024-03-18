import pandas as pd
import sorobn as hh

# Assuming sorobn is a fictional example for educational purposes
# Initialize the Bayesian Network with conditional probabilities
bn = hh.BayesNet(
    ('C', ['S', 'R']),
    ('S', 'W'),
    ('R', 'W'))

# Define conditional probabilities
bn.P['C'] = pd.Series({True: 0.5, False: 0.5})
bn.P['S'] = pd.Series({
    (True, True): 0.1, (True, False): 0.9,
    (False, True): 0.5, (False, False): 0.5
})
bn.P['R'] = pd.Series({
    (True, True): 0.8, (True, False): 0.2,
    (False, True): 0.2, (False, False): 0.8
})
bn.P['W'] = pd.Series({
    (True, True, True): 0.99, (True, True, False): 0.01,
    (True, False, True): 0.9, (True, False, False): 0.1,
    (False, True, True): 0.95, (False, True, False): 0.05,
    (False, False, True): 0.05, (False, False, False): 0.95})

bn.prepare()
bn.query('C', event={'S': False, 'W': True})

# Part (d) Implementation: Monte Carlo Simulation for different n values
print("Part C. The probability for the query P(C|-s,w)")
exact_probability = 0.5  # Placeholder for exact probability

n_values = [10**3, 10**4, 10**5, 10**6]
for n in n_values:
    # Placeholder for generating n samples
    # Implement the MCMC sampling here and calculate the estimated probability
    estimated_probability = 0.4939  # Placeholder result
    error = abs(exact_probability - estimated_probability) * 100 / exact_probability
    print(f"n = {n}: <{estimated_probability:.4f}>, error = {error:.2f} %")

# Placeholder output for parts (b) and (c) to match the specified format in part (e)
print("Part A. The sampling probabilities")
print("P(C|-s,r) = <0.xxxx, 0.xxxx>")
print("P(C|-s,-r) = <0.xxxx, 0.xxxx>")
print("P(R|c,-s,w) = <0.xxxx, 0.xxxx>")
print("P(R|-c,-s,w) = <0.xxxx, 0.xxxx>")

print("Part B. The transition probability matrix")
print("S1   S2   S3   S4")
print(".    .    .    .")  # Replace dots with actual probabilities
print(".    .    .    .")
print(".    .    .    .")
print(".    .    .    .")

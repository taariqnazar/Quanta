import numpy as np
from scipy.stats import norm


def greeks_call(S0, K, T, sigma, r):
    d1 = (np.log(S0/K) + (r + sigma**2 / 2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    delta = norm.cdf(d1)
    gamma = norm.pdf(d1)/(S0*sigma*np.sqrt(T))
    vega = S0*norm.pdf(d1)*np.sqrt(T)
    theta = (-(S0*sigma*norm.pdf(d1))/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2))
    rho = T*K*np.exp(-r*T)*norm.cdf(d2)

    return [delta, gamma, vega, theta, rho]


def greeks_put(S0, K, T, sigma, r):
    d1 = (np.log(S0/K) + (r + sigma**2 / 2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    delta = norm.cdf(d1) - 1
    gamma = norm.pdf(d1)/(S0*sigma*np.sqrt(T))
    vega = S0*norm.pdf(d1)*np.sqrt(T)
    theta = -(S0*norm.pdf(d1)*sigma)/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2)
    rho = -T*K*np.exp(-r*T)*norm.cdf(-d2)

    return [delta, gamma, vega, theta, rho]


def black_scholes_call_option_price(S0, K, T, sigma, r):
    d1 = (np.log(S0/K) + (r + sigma**2 / 2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    return S0*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)

def black_scholes_put_option_price(S0, K, T, sigma, r):
    c = black_scholes_call_option_price(S0, K, T, sigma, r)

    return c - S0 + K*np.exp(-r*T)
    

if __name__ == '__main__':
    S0 = 100
    K = 95
    T = 1
    sigma = 0.2
    r = 0.1

    cp = black_scholes_call_option_price(S0, K, T, sigma, r)
    print(cp)

    # pp = black_scholes_put_option_price(S0, K, T, sigma, r)
    # print(pp)

    print(greeks_call(S0, K, T, sigma, r))
    print(greeks_put(S0, K, T, sigma, r))

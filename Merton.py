import numpy as np
from scipy.stats import norm


class Merton:
    def __init__(self, S, V, D, r, sigma_s, T, epsilon=10e-5, max_iter=10000):
        self.S = S
        self.V = V
        self.D = D
        self.r = r
        self.sigma_s = sigma_s
        self.T = T  
        self.epsilon = epsilon
        self.max_iter = max_iter                                       

    # function that compute the zero coupon risk free rate with the input SWAP OIS rate
    def rff(self):
        return -(365/(self.T * 365.25)) * np.log(1/(1 + self.r * ((self.T * 365.25)/360)))

    # function to compute with the initial params the discounted parameter
    def B_t(self):
        B_t = np.exp(-self.rff() * self.T)
        return B_t
    
    # function to compute with the initial params the probability term d1 
    def d1(self, V_t, sigma_s):
        return (np.log(V_t / (self.D)) + (self.rff() + (sigma_s ** 2) * 0.5) * self.T) / (sigma_s * np.sqrt(self.T))
    
    # function to compute with the initial params the probability term d1 
    def d2(self, V_t, sigma_s):
        return self.d1(V_t, sigma_s) - sigma_s * np.sqrt(self.T)
    
    # function to compute with the initial params the cumulative distribution function until the term d1
    def N(self, x):
        return norm.cdf(x)
    
    # function to compute with the initial params the h1 term which is a modified version of d1 by express the V_t term using the debt leverage formula 
    def h1(self, sigma_s, V_t):
        return ((np.log(1 / ((self.D * self.B_t()) / V_t)) + (sigma_s ** 2) * 0.5) * self.T) / (sigma_s * np.sqrt(self.T))
    
    # function to compute with the initial params the h2 term which is a modified version of d2 by express the V_t term using the debt leverage formula
    def h2(self, sigma_s, V_t):
        return self.h1(sigma_s, V_t) - sigma_s * np.sqrt(self.T)
    
    # function to compute with the initial params the function that express V as function of other parameters
    def g1(self, d1, d2):
        return (self.S + self.D * self.B_t() * self.N(d2)) / self.N(d1)
    
    # function to compute with the initial params the function that express sigma_v as function of other parameters
    def g2(self, sigma_s, V_t, d1):
        return (sigma_s * self.S) / (self.N(d1) * V_t)
    
    # function of convergence that iterates through the function g1 and g2 to find the values of V and sigma_v
    def convergence(self):

        # Initial guess
        V_t_n, sigma_V_n = self.V, self.sigma_s
        iter = 0
        while True:

            # Update values using g1 and g2
            V_t_n1 = self.g1(self.d1(V_t_n ,sigma_V_n), self.d2(V_t_n, sigma_V_n))
            sigma_V_n1 = self.g2(self.sigma_s, V_t_n1, self.d1(V_t_n1, sigma_V_n))
            
            # Check for convergence
            delta_V = abs(V_t_n1 - V_t_n)
            delta_sigma_V = abs(sigma_V_n1 - sigma_V_n)
            
            if (delta_V < self.epsilon) and (delta_sigma_V < self.epsilon):
                break

            # Update the values for the next iteration
            V_t_n = V_t_n1
            sigma_V_n = sigma_V_n1

            iter += 1

            if iter >= self.max_iter:
                break

        self.V_t_converged = V_t_n
        self.sigma_V_converged = sigma_V_n

        return self.V_t_converged, self.sigma_V_converged

    def sigma_converged(self):
        V_t, sigma_v = self.convergence()
        return sigma_v
    
    # function that compute the default probability
    def default_proba(self):
        V_t, sigma_v = self.convergence()
        return (self.N(-self.d2(V_t, sigma_v))) * 100
    
    # function that computes the recovery rate (anticipated) is de ned as the ratio of the anticipated value at t of the value of assets at maturity over the nominal value of the debt
    def recovery_rate(self):
        V_t, sigma_v = self.convergence()
        delta_t = (V_t * self.N(-self.d1(V_t, sigma_v))) / (self.D * self.B_t() * self.N(-self.d2(V_t, sigma_v)))
        return (delta_t) * 100
    
    # function that computes the debt leverage is, by definition, the ratio between the current value of the value nominal value of debt D and value of assets Vt.
    def debt_leverage(self):
        V_t, sigma_v = self.convergence()
        return ((self.D * self.B_t()) / V_t)
    
    # function that computes the (implicit) credit spread is defined as the difference between the interest rate of the company debt (risky) and the risk-free interest rate (maturity T)
    def credit_spread(self):
        V_t, sigma_v = self.convergence()
        spread = -(1 / self.T) * np.log((self.N(-self.h1(sigma_v, V_t)) / self.debt_leverage()) + self.N(self.h2(sigma_v, V_t)))
        return spread












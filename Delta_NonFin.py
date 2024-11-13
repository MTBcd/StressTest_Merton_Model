
import numpy as np
from Merton import Merton

class DeltaCalculationNonFinancial(Merton):
    def __init__(self, S, V, D, r, sigma_s, T, ebitda, NetDebt, w=None, MSA_Biodiv=None, Tax_Carbon=None, CapImpct=-0.5, Tax_c=50, Tax_b=5000000):
        # Initialize the base class Merton with the given parameters
        super().__init__(S, V, D, r, sigma_s, T)
        
        # Assign the provided parameters to instance variables
        self.MSA_Biodiv = MSA_Biodiv
        self.Tax_Carbon = Tax_Carbon
        self.w = w
        self.ebitda = ebitda
        self.NetDebt = NetDebt
        self.CapImpct = CapImpct
        self.Tax_c = Tax_c
        self.Tax_b = Tax_b

        if self.Tax_Carbon is not None:
            self.Tax_Carbon = 0.0000001 if self.Tax_Carbon <= 0.0000001 else self.Tax_Carbon
        #if self.Tax_Carbon is not None:
        #    self.Tax_Carbon = self.Tax_Carbon if self.Tax_Carbon > 100000 else self.Tax_Carbon * 100000

        # Ensure at least one MSA value (Biodiversity or Carbon) is provided
        if (self.MSA_Biodiv and self.Tax_Carbon) is False:
            raise TypeError("The function must have an MSA value to perform the Delta calculation")
        
        # Ensure EBITDA is not None
        if self.ebitda is None:
            raise TypeError("The EBITDA variable can't be NoneType")

        # Set weight to 1 if not provided
        if self.w is not None:
            self.w = w
        else:
            self.w = 1

        if self.ebitda <= 0:
            self.ebitda = 1
        else:
            self.ebitda = ebitda
    
    def delta_biodiv(self):
        # Calculate the impact of biodiversity tax
        return -self.MSA_Biodiv * self.Tax_b

    def delta_carbon(self):
        # Calculate the impact of carbon tax
        return -self.Tax_Carbon * self.Tax_c

    def Value_to_Ebitda(self):
        # Calculate the ratio of the value to EBITDA
        return np.divide((self.S + self.D), self.ebitda)

    def delta_calculation(self):
        # Calculate the numerator based on the provided MSA values
        if self.MSA_Biodiv:
            numerator = self.Value_to_Ebitda() * (self.ebitda + self.delta_biodiv()) - self.NetDebt
        if self.Tax_Carbon:
            numerator = self.Value_to_Ebitda() * (self.ebitda + self.delta_carbon()) - self.NetDebt
        if (self.MSA_Biodiv and self.Tax_Carbon):
            numerator = self.Value_to_Ebitda() * (self.ebitda + (self.delta_biodiv() + self.delta_carbon())) - self.NetDebt
        
        # Calculate the denominator for the delta calculation
        denominator = self.Value_to_Ebitda() * self.ebitda - self.NetDebt

        # Return the maximum value between the calculated ratio and the CapImpct
        return np.maximum(((numerator / denominator) - 1), self.CapImpct)

    def delta_portfolio(self):
        # Calculate the weighted delta for the portfolio
        return self.w * self.delta_calculation()




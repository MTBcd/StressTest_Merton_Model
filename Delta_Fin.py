

import numpy as np
from Merton import Merton


class DeltaCalculationFinancial(Merton):
    def __init__(self, S, V, D, r, sigma_s, T, OpeIncm, CurrRate=None, w=None, MSA_Biodiv=None, Tax_Carbon=None, CapImpct=-0.50, Tax_c=50, Tax_b=5000000):
        # Initialize the base class Merton with the given parameters
        super().__init__(S, V, D, r, sigma_s, T)
        
        # Assign the provided parameters to instance variables
        self.w = w
        self.CurrRate = CurrRate
        self.OpeIncm = OpeIncm
        self.CapImpct = CapImpct
        self.MSA_Biodiv = MSA_Biodiv
        self.Tax_Carbon = Tax_Carbon
        self.Tax_c = Tax_c
        self.Tax_b = Tax_b


        if self.Tax_Carbon is not None:
            self.Tax_Carbon = 0.0000001 if self.Tax_Carbon <= 0.0000001 else self.Tax_Carbon
        #if self.Tax_Carbon is not None:
        #    self.Tax_Carbon = self.Tax_Carbon if self.Tax_Carbon > 100000 else self.Tax_Carbon * 100000

        # Set weight to 1 if not provided
        if self.w is not None:
            self.w = w
        else:
            self.w = 1

        # Set Currency Rate to 1 if not provided
        if self.CurrRate is not None:
            self.CurrRate = CurrRate
        else:
            self.CurrRate = 1

        # Set Currency Rate to 1 if it's inferior to 0
        if self.OpeIncm <= 0:
            self.OpeIncm = 1
        else:
            self.OpeIncm = OpeIncm

        # Ensure at least one MSA value (Biodiversity or Carbon) is provided
        if (self.MSA_Biodiv and self.Tax_Carbon) is False:
            raise TypeError("The function must have an MSA value to perform the Delta calculation")
        
    def delta_biodiv(self):
        # Calculate the impact of biodiversity tax
        return -self.MSA_Biodiv * self.Tax_b

    def delta_carbon(self):
        # Calculate the impact of carbon tax
        return -self.Tax_Carbon * self.Tax_c

    def Ratio(self):
        # Calculate the ratio of the company's market capitalization to the product of the current rate and operating income
        return self.S / (self.CurrRate * self.OpeIncm)

    def NewOpeIncm(self):
        # Calculate the new operating income after applying biodiversity or carbon tax impacts
        if self.MSA_Biodiv:
            return self.OpeIncm * self.CurrRate + self.delta_biodiv()
        if self.Tax_Carbon:
            return self.OpeIncm * self.CurrRate + self.delta_carbon()
        if (self.MSA_Biodiv and self.Tax_Carbon):
            return self.OpeIncm * self.CurrRate + (self.delta_biodiv() + self.delta_carbon())

    def delta_calculation(self):
        # Calculate the numerator for the delta calculation
        numerator = self.NewOpeIncm() * self.Ratio()
        # Return the maximum value between the calculated ratio and the CapImpct
        return np.maximum(((numerator / self.S) - 1), self.CapImpct)

    def delta_portfolio(self):
        # Calculate the weighted delta for the portfolio
        return self.w * self.delta_calculation()



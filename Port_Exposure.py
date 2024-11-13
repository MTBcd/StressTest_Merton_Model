
from  Merton import Merton
from Delta_Fin import DeltaCalculationFinancial
from Delta_NonFin import DeltaCalculationNonFinancial
import pandas as pd


class PortfolioImpact:
    def __init__(self, dataset, CapImpct=-0.5):
        self.dataset = dataset
        self.CapImpct = CapImpct

    def delta_calculation(self):

        #modified_duration = self.dataset["Modified Duration"]
        #market_value = self.dataset['Market Value %']
        #Port_Duration = np.sum(modified_duration * market_value)

        for index, row in self.dataset.iterrows():

            S_1 = row["Market Cap (m)"]
            D_1 = row['Total Debt']
            r_1 = row['Risk_free_rate (anser)']
            ebitda = row['EBITDA']
            Carbon_tax_ = row['Emissions Intensity (Sales) - Latest(Wt Avg-PORT Delta NMV)']
            Biodiv_tax_ = row['corpoFIImpactTerrestrialDynamic']
            OpeIncm = row['Operating Income']
            CurrRate = row['CurrencyRate']
            NetDebt = row['Net Debt']
            T_1 = 1.0 ##Port_Duration
            sigma_1 = row['Volatilité (bloom)']

            if float(row['Volatilité (bloom)']) > 1:
                sigma_1 = float(row['Volatilité (bloom)'])/100
            else:
                sigma_1 = float(row['Volatilité (bloom)'])

            if pd.isna(row['Total Debt']) | pd.isna(row['MARKET_CAP']) | pd.isna(row['Risk_free_rate (anser)']) | pd.isna(row['Volatilité (bloom)']) | pd.isna(row['EBITDA']) | pd.isna(row['Emissions Intensity (Sales) - Latest(Wt Avg-PORT Delta NMV)']) | pd.isna(row['Operating Income']) | pd.isna(row['CurrencyRate']) | pd.isna(row['Net Debt']):
                self.dataset.at[index, 'Delta_spread_multiplier_c'] = pd.NA
            else:
                merton = Merton(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1)
                spread_init = merton.credit_spread()

                while spread_init <= 0.000001:
                    merton = Merton(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1)
                    spread_init = merton.credit_spread()
                    sigma_1 += 0.01

                if row['GICS Sector'] == 'Financials':
                    delta_c = DeltaCalculationFinancial(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1, OpeIncm, CurrRate, MSA_Biodiv=None, Tax_Carbon=Carbon_tax_, CapImpct=self.CapImpct)
                else:
                    delta_c = DeltaCalculationNonFinancial(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1, ebitda, NetDebt, MSA_Biodiv=None, Tax_Carbon=Carbon_tax_, CapImpct=self.CapImpct)

                # Alpha is the parameter that allow us to calibrate volatility relative to market cap variation
                alpha = 0.5187

                # Calculate the stressed market capitalization and company value
                Market_cap_stressed_c = (S_1 * (1 + delta_c.delta_calculation()))

                Company_Value_Stressed_c = ((S_1 * (1 + delta_c.delta_calculation())) + D_1)

                # Calibrate the equity volatility
                Calibrated_Sigma_c = sigma_1 * (1 - alpha * delta_c.delta_calculation())

                # Initialize the Merton model with the stressed parameters
                merton_c = Merton(Market_cap_stressed_c, Company_Value_Stressed_c, D_1, r_1, Calibrated_Sigma_c, T_1)

                spread_c = merton_c.credit_spread()

                #self.dataset.at[index, 'Market_cap_stressed_c'] = Market_cap_stressed_c

                #self.dataset.at[index, 'variation_c'] = delta_c.delta_calculation()

                self.dataset.at[index, 'Delta_spread_multiplier_c'] = spread_c / spread_init

                #self.dataset.at[index, 'spread_c'] = spread_c


            if pd.isna(row['Total Debt']) | pd.isna(row['MARKET_CAP']) | pd.isna(row['Risk_free_rate (anser)']) | pd.isna(row['Volatilité (bloom)']) | pd.isna(row['EBITDA']) | pd.isna(row['corpoFIImpactTerrestrialDynamic']) | pd.isna(row['Operating Income']) | pd.isna(row['CurrencyRate']) | pd.isna(row['Net Debt']):
                self.dataset.at[index, 'Delta_spread_multiplier_b'] = pd.NA
            else:
                merton = Merton(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1)
                spread_init = merton.credit_spread()

                while spread_init <= 0.000001:
                    merton = Merton(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1)
                    spread_init = merton.credit_spread()
                    sigma_1 += 0.01

                if row['GICS Sector'] == 'Financials':
                    delta_b = DeltaCalculationFinancial(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1, OpeIncm, CurrRate, MSA_Biodiv=Biodiv_tax_, Tax_Carbon=None, CapImpct=self.CapImpct)
                else:
                    delta_b = DeltaCalculationNonFinancial(S_1, (S_1 + D_1), D_1, r_1, sigma_1, T_1, ebitda, NetDebt, MSA_Biodiv=Biodiv_tax_, Tax_Carbon=None, CapImpct=self.CapImpct)

                alpha = 0.5187

                Market_cap_stressed_b = (S_1 * (1 + delta_b.delta_calculation()))

                Company_Value_Stressed_b = ((S_1 * (1 + delta_b.delta_calculation())) + D_1)

                Calibrated_Sigma_b = sigma_1 * (1 - alpha * delta_b.delta_calculation())

                merton_b = Merton(Market_cap_stressed_b, Company_Value_Stressed_b, D_1, r_1, Calibrated_Sigma_b, T_1)

                spread_b = merton_b.credit_spread()

                #self.dataset.at[index, 'Market_cap_stressed_b'] = Market_cap_stressed_b

                #self.dataset.at[index, 'variation_b'] = delta_b.delta_calculation()

                self.dataset.at[index, 'Delta_spread_multiplier_b'] = spread_b / spread_init

                #self.dataset.at[index, 'spread_b'] = spread_b

        for index, row in self.dataset.iterrows():
            spread_c = row["Delta_spread_multiplier_c"]
            spread_b = row['Delta_spread_multiplier_b']
            price = row['Price']
            spread_duration = row['Spread Duration']
            spread_convexity = row['Spread Convexity']
            CDS = row['OAS']/10000

            if pd.isna(row['Delta_spread_multiplier_c']) | pd.isna(row['Price']) | pd.isna(row['Spread Duration']) | pd.isna(row['Spread Convexity']) | pd.isna(row['OAS']):
                self.dataset.at[index, 'stressed_price_c'] = pd.NA
            else:
                reprincing_c = price - spread_duration * ((CDS * spread_c) - CDS) * price + (1/2) * spread_convexity * (((CDS * spread_c) - CDS) ** 2) * price
                self.dataset.at[index ,'stressed_price_c'] = max(-reprincing_c, price * (-self.CapImpct)) if reprincing_c > price else max(reprincing_c, price * (-self.CapImpct))

            if pd.isna(row['Delta_spread_multiplier_b']) | pd.isna(row['Price']) | pd.isna(row['Spread Duration']) | pd.isna(row['Spread Convexity']) | pd.isna(row['OAS']):
                self.dataset.at[index, 'stressed_price_b'] = pd.NA
            else:
                reprincing_b = price - spread_duration * ((CDS * spread_b) - CDS) * price + (1/2) * spread_convexity * (((CDS * spread_b) - CDS) ** 2) * price
                self.dataset.at[index ,'stressed_price_b'] = max(-reprincing_b, price * (-self.CapImpct)) if reprincing_b > price else max(reprincing_b, price * (-self.CapImpct))

        for index, row in self.dataset.iterrows():
            price = row['Price']
            stressed_price_c = row['stressed_price_c']
            stressed_price_b = row['stressed_price_b']
            weight = row['Market Value %']

            if pd.isna(row['stressed_price_c']) | pd.isna(row['Price']) | pd.isna(row['Market Value %']):
                self.dataset.at[index, 'delta_position_c'] = pd.NA
            else:
                self.dataset.at[index, 'delta_position_c'] = weight * ((stressed_price_c - price) / price)

            if pd.isna(row['stressed_price_b']) | pd.isna(row['Price']) | pd.isna(row['Market Value %']):
                self.dataset.at[index, 'delta_position_b'] = pd.NA
            else:
                self.dataset.at[index, 'delta_position_b'] = weight * ((stressed_price_b - price) / price)

        return self.dataset[['Issuer Legal Entity Identifier', 'Issuer ID', 'ISIN', 'Currency',
                            'Issuer Name', 'Coupon Type',
                            'GICS Sector', 'Maturity',
                            'Market Value %', 'Price Date',
                            'Price', 'Total Debt',
                            'Current Face (m)', 'Market Value (m)',
                            'MV(MktVal/CurrFace)', 'Net Debt',
                            'Operating Income', 'EBITDA',
                            'CurrencyRate', 'Emissions Intensity (Sales) - Latest(Wt Avg-PORT Delta NMV)',
                            'Spread Duration', 'Spread Convexity', 'OAS', 'corpoFIImpactTerrestrialDynamic', 
                            'MARKET_CAP', 'Volatilité (bloom)', 'Risk_free_rate (anser)',
                            'stressed_price_c','stressed_price_b', 'delta_position_c', 'delta_position_b']]
#                            'variation_b', 'Delta_spread_multiplier_b',
#                            'variation_c', 'Delta_spread_multiplier_c',
#                            'spread_init', 'spread_c', 'spread_b']]









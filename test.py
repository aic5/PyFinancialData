from __future__ import division

import pandas as pd
import urllib2
import matplotlib.pyplot as plt


class PyMarket:

	units = '3' #1 = None 2 = Thousands 3 = Millions 4 = Billions
	df_tickers = pd.DataFrame()

	def __init(self):
		pass

	# Get the ticker list and Market Cap from NASDAQ	
	def get_tickers(self):   
	    # NASDAQ URL (csv download)
	    url = 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
	    
	    # Read CSV into pandas
	    df = pd.read_csv(url, skiprows=0, index_col=0)

	    # Scale data accordingly (MarketCap data in $1.00 USD)
	    df.rename(columns={'MarketCap': 'MarketCap_original'}, inplace=True)
	    if self.units == '2':
	    	factor = 10**3
	    elif self.units == '3':
	    	factor = 10**6
	    elif self.units == '4':
	    	factor = 10**9
	    else:
	    	factor = 1

	    df['MarketCap'] =  df['MarketCap_original'] / factor

	    return df

	# Source: NASDAQ
	def get_industries(self):
		# Download tickers if necessary
		if self.df_tickers.empty: 
			self.df_tickers = self.get_tickers()

		return self.df_tickers['Industry'].unique()

	# Source: NASDAQ
	def get_sectors(self):
		# Download tickers if necessary
		if self.df_tickers.empty: 
			self.df_tickers = self.get_tickers()

		return self.df_tickers['Sector'].unique()

	# Source: NASDAQ
	def get_symbols(self):
		# Download tickers if necessary
		if self.df_tickers.empty: 
			self.df_tickers = self.get_tickers()

		return self.df_tickers.index.tolist()

	# Source: NASDAQ
	def market_cap(self):
		# Download tickers if necessary
		if self.df_tickers.empty: 
			self.df_tickers = self.get_tickers()

		# Pandas display format
		pd.options.display.float_format = '{:,.2f}'.format

		return self.df_tickers['MarketCap'].describe()

	# Change units from Thousands, Millions, Billions, or None	
	# Source: MorningStar
	def set_scale(self, units = 'millions'):
		if units.lower() == 'thousands' or units.lower() == 't':
			self.units = '2'
		elif units.lower() == 'millions' or units.lower() == 'mil' or units.lower() == 'm':
			self.units = '3'
		elif units.lower() == 'billions' or units.lower() == 'bil' or units.lower() == 'b':
			self.units = '4'
		elif units.lower() == 'none':
			self.units = '1'
		else:
			return False

		return True

	def get_scale(self, text = True):
		if self.units == '1':
			if text:
				return 'None'
			else:
				return self.units
		elif self.units == '2':
			if text:
				return 'Thousands'
			else:
				return self.units
		elif self.units == '3':
			if text:
				return 'Millions'
			else:
				return self.units
		elif self.units == '4':
			if text:
				return 'Billions'
			else:
				return self.units
		else: 
			return self.units 


	# Returns a DataFrame object containing 
	# Balance Sheet (bs == default), Income Statement (is), or Cash Flow (cf)
	# Source: MorningStar
	def get_financials(self, ticker, report = 'bs', frequency = 'A'):
	    if frequency.lower() == 'a':
	        frequency = '12'
	    elif frequency.lower() == 'q':
	        frequency = '3'
	    
	    # MorningStar URL (csv download)
	    url = 'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?&t='+ticker+'&region=usa&culture=en-US&cur=USD&reportType='+report+'&period='+frequency+'&dataType=R&order=desc&columnYear=10&rounding=3&view=raw&r=640081&denominatorView=raw&number='+self.units
	    
	    # Read CSV into pandas
	    df = pd.read_csv(url, skiprows=1, index_col=0)
	    return df


print '-' * 30 + ' Start ' + '-' * 30


## Testing
data = PyMarket()

# Get financials
#data.scale('b')
#df = data.get_financials('GOOGL','is','a')

# Get ticker list
#df = data.get_tickers()
#print df.head()

# Get industry list
#data.get_tickers()


# Market Cap
# print df.head()

# Listing all sectors - TBD
# print df['IPOyear'].value_counts()
# df_plot = df['IPOyear'].value_counts()
# df_plot.dropna()
# df_plot.plot()

# ---- easier functions ------
# print data.get_sectors()
# print data.get_industries()


data.set_scale('billions')
print data.market_cap()
print data.get_scale()



# Listing all sectors
#print df['Sector'].unique()

# Listing all industries
#print df['Industry'].unique()

print '-' * 30 + ' Done ' + '-' * 30
import pandas as pd
import matplotlib.pyplot as plt

def custom_date_parser(date):
    try:
        return pd.to_datetime(date, format='%Y-%m-%d')
    except ValueError:
        # Handle the exception or return a default value
        return pd.NaT  # Not a Time, used for missing datetime values

df = pd.read_csv('exchangerates.csv', parse_dates=['date'], date_parser=custom_date_parser)

# Set 'date' as the index
df.set_index('date', inplace=True)

# Resample annually and calculate percentage change
annual_data = df.resample('A').last().pct_change()*100

# output the annual_date.index.year
print(annual_data.index.year)

# Set the figure size (width, height) in inches
plt.figure(figsize=(24, 16))  # Increase the size as needed
plt.rcParams.update({'font.size': 11})  # Adjust font size as needed

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Plot separate charts for each year if data is available and save as PNG
for year in [2022, 2023, 2024]:
    # Check if 'year' is in the index's year
    if year in annual_data.index.year:
        # Select data for the specific 'year'
        year_data = annual_data[annual_data.index.year == year]
        # Plot if 'year_data' is not empty
        if not year_data.empty:
            ax = year_data.plot(kind='bar', title=f'Percentage Change in {year}')
            ax.set_xlabel('')
            ax.set_ylabel('Percentage Change')
            # Save the figure
            plt.savefig(f'Percentage_Change_{year}.png', dpi=300, bbox_inches='tight')
            plt.show()
        else:
            print(f"No data available for {year}")
    else:
        print(f"No data available for {year}")


# Plot trend over time
df.resample('A').last().plot(title='Trend Over Time')
plt.ylabel('Exchange Rate')
plt.savefig('Trend_Over_Time.png', dpi=300, bbox_inches='tight')
plt.show()

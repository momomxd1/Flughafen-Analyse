import pandas as pd
import matplotlib.pyplot as plt

# Laden der CSV-Dateien
flights = pd.read_csv('Dataset/flights.csv')

# Konvertieren von DEPARTURE_DELAY in eine numerische Form
flights['DEPARTURE_DELAY'] = pd.to_numeric(flights['DEPARTURE_DELAY'], errors='coerce')

# Negative Verspätungen auf 0 setzen, da wir nur an tatsächlichen Verspätungen interessiert sind
flights['DEPARTURE_DELAY'] = flights['DEPARTURE_DELAY'].apply(lambda x: max(x, 0))

# Umwandlung der SCHEDULED_DEPARTURE in eine Stunde des Tages
flights['SCHEDULED_DEPARTURE'] = flights['SCHEDULED_DEPARTURE'].apply(lambda x: '{:04d}'.format(int(x)))
flights['SCHEDULED_DEPARTURE'] = pd.to_datetime(flights['SCHEDULED_DEPARTURE'], format='%H%M', errors='coerce').dt.hour

# Filterung der Daten auf Januar 2015 und SEA Airport
flights_sea = flights[(flights['MONTH'] == 1) & (flights['ORIGIN_AIRPORT'] == 'SEA')]

# Zeitliche Analyse der Verspätungen für SEA
hourly_delays_sea = flights_sea.groupby('SCHEDULED_DEPARTURE')['DEPARTURE_DELAY'].mean()

plt.figure(figsize=(12, 6))
hourly_delays_sea.plot(kind='bar', color='skyblue')
plt.xlabel('Stunde des Tages')
plt.ylabel('Durchschnittliche Verspätung (Minuten)')
plt.title('Durchschnittliche Verspätung nach Stunde des Tages im Januar 2015 für SEA')
plt.tight_layout()
plt.show()

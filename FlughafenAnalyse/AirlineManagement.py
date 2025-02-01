import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Laden der CSV-Dateien
flights = pd.read_csv('Dataset/flights.csv')
airports = pd.read_csv('Dataset/airports.csv')
airlines = pd.read_csv('Dataset/airlines.csv')

# Konvertieren der relevanten Spalten in numerische Werte und Filtern auf 'Virgin America'
flights['DEPARTURE_DELAY'] = pd.to_numeric(flights['DEPARTURE_DELAY'], errors='coerce')
vx_flights = flights[flights['AIRLINE'] == 'VX']  # Angenommen 'VX' ist der Code für 'Virgin America'

# Join der Flugdaten mit den Flughafennamen
vx_flights = vx_flights.merge(airports[['IATA_CODE', 'AIRPORT']], left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')

# Aggregation der Verspätungsdaten nach Flugnummer und Flughafen
delays_by_flight_number = vx_flights.groupby(['FLIGHT_NUMBER', 'AIRPORT'])['DEPARTURE_DELAY'].mean().reset_index()

# Sortieren der Daten nach durchschnittlicher Verspätungsdauer
top_delays = delays_by_flight_number.sort_values(by='DEPARTURE_DELAY', ascending=False).head(10)

# Visualisierung der Flugnummern mit der höchsten durchschnittlichen Verspätungsdauer
plt.figure(figsize=(16, 9))  # Größere Figur
barplot = sns.barplot(x='FLIGHT_NUMBER', y='DEPARTURE_DELAY', hue='AIRPORT', data=top_delays, palette='deep')
plt.xlabel('Flugnummer')
plt.ylabel('Durchschnittliche Verspätung (Minuten)')
plt.xticks(rotation=45)

# Anpassen der Größe der Labels und Position der Legende
plt.setp(barplot.get_xticklabels(), fontsize=12)
plt.setp(barplot.get_yticklabels(), fontsize=12)
plt.legend(title='Flughafen', bbox_to_anchor=(1.05, 1), loc='upper left')

# Titel mittig und innerhalb der Figur platzieren
plt.suptitle('Top 10 Flugnummern von Virgin America mit der höchsten durchschnittlichen Verspätung nach Flughafen', fontsize=16, va='top', ha='center')

# Layout anpassen, um Überlappungen zu verhindern und die Legende sichtbar zu machen
plt.tight_layout(rect=[0.05, 0.05, 0.9, 0.9])  # Ränder anpassen

plt.show()

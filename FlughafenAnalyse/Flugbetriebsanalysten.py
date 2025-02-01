import pandas as pd
import matplotlib.pyplot as plt

# Daten laden
flights = pd.read_csv('Dataset/flights.csv')
airports = pd.read_csv('Dataset/airports.csv')  

delay_columns = ['WEATHER_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY']
for column in delay_columns + ['DEPARTURE_DELAY']:
    flights[column] = pd.to_numeric(flights[column].fillna(0))

# Top 5 Flughäfen mit den meisten Verspätungen
top_airports_delays = flights.groupby('ORIGIN_AIRPORT')['DEPARTURE_DELAY'].sum().nlargest(5)
top_airports = top_airports_delays.index

# Namen der Flughäfen für die Legende extrahieren
airport_names = airports[airports['IATA_CODE'].isin(top_airports)][['IATA_CODE', 'AIRPORT']].set_index('IATA_CODE')
airport_labels = [f"{code} - {name}" for code, name in airport_names['AIRPORT'].items()]

# Farbpalette für die Diagramme auswählen
colors = plt.cm.Paired(range(len(delay_columns)))

# Kuchendiagramm für die Top 5 Flughäfen
fig, axs = plt.subplots(1, 5, figsize=(20, 8))  # Adjust the size as needed

# Einzelne Kuchendiagramme erstellen
for i, airport in enumerate(top_airports):
    airport_delays = flights[flights['ORIGIN_AIRPORT'] == airport][delay_columns].sum()
    wedges, texts, autotexts = axs[i].pie(airport_delays, autopct='%1.1f%%', startangle=140, colors=colors)
    axs[i].set_title(airport)

# Legende für Verspätungsgründe hinzufügen
plt.figlegend(wedges, airport_delays.index, loc='upper right', bbox_to_anchor=(1, 1), title='Verspätungsgründe')

# Zweite Legende für Flughäfen hinzufügen
plt.figlegend([plt.Line2D([0], [0], color='w', marker='o', markerfacecolor='k', label=lbl) for lbl in airport_labels],
              airport_labels, loc='upper left', bbox_to_anchor=(0, 1), title='Flughäfen')

plt.suptitle('Aufteilung der Verspätungsgründe für die Top 5 Flughäfen')
plt.tight_layout()
plt.show()

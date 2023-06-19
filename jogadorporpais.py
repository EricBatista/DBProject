import matplotlib.pyplot as plt
import sqlalchemy
import PySimpleGUI as sg
from sqlalchemy import create_engine, text

# Connect to the database
engine = create_engine('postgresql://postgres:admin@localhost/postgres')
connection = engine.connect()

# Execute the query
query = text("""
SELECT pa.Nome, COUNT(*) AS NumPlayers
FROM PESSOA p
JOIN PAIS pa ON pa.ID_Pais = p.ID_Pais
GROUP BY pa.Nome
""")
result = connection.execute(query)

# Extract the data
countries = []
num_players = []
for row in result:
    country_name = ' '.join(row[0].split()).replace("       ", " ")
    countries.append(country_name)
    num_players.append(row[1])

# Close the database connection
connection.close()

# Create the bar chart using Matplotlib
fig, ax = plt.subplots()
ax.bar(countries, num_players)
ax.set_xlabel('Country')
ax.set_ylabel('Number of Players')
ax.set_title('Number of Players per Country')

# Save the figure as an image file
image_file = 'bar_chart.png'
fig.savefig(image_file)

# Define the layout for the GUI
layout = [
    [sg.Image(image_file)],
    [sg.Button('Close')]
]

# Create the GUI window
window = sg.Window('Player Count per Country', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Close':
        break

# Close the GUI window
window.close()


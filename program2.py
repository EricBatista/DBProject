import PySimpleGUI as sg
import sqlalchemy
from sqlalchemy import create_engine, text

# Connect to the database
engine = create_engine('postgresql://postgres:admin@localhost/postgres')
connection = engine.connect()

# Execute the query
query = text("""
SELECT j.ID_Jogos, COUNT(jp.ID_Jogadas) AS NumMoves
FROM JOGOS j
JOIN Jogos_Possuem_Jogadas jp ON jp.ID_Jogos = j.ID_Jogos
GROUP BY j.ID_Jogos
""")
result = connection.execute(query)

# Extract the data
game_ids = []
num_moves = []
for row in result:
    game_ids.append(row[0])
    num_moves.append(row[1])

# Close the database connection
connection.close()

# Create the GUI window
layout = [
    [sg.Text('Number of Moves per Game')],
    [sg.Table(values=list(zip(game_ids, num_moves)),
              headings=['Game ID', 'Number of Moves'],
              justification='center',
              auto_size_columns=False,
              col_widths=[10, 15])],
    [sg.Button('Close')]
]

window = sg.Window('Game Statistics', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Close':
        break

# Close the GUI window
window.close()
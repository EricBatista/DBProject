import PySimpleGUI as sg
import sqlalchemy
from sqlalchemy import create_engine, text

# Connect to the database
engine = create_engine('postgresql://postgres:admin@localhost/postgres')
connection = engine.connect()

# Function to perform the search query based on the selected search criteria
def perform_search(search_criteria, value):
    if search_criteria == 'Player':
        query = text("""
        SELECT j.ID_Jogos, j.Jornada, h.Nome AS Lugar, h.Endereco
        FROM JOGOS j
        JOIN Jogador_Participa_Jogo jpj ON jpj.ID_Jogos = j.ID_Jogos
        JOIN PESSOA p ON p.NumAssociado = jpj.NumAssociado
        JOIN SALAO s ON s.ID_Salao = j.ID_Salao
        JOIN HOTEL h ON h.ID_Hotel = s.ID_Hotel
        WHERE p.Nome = :value
        """)
        result = connection.execute(query, {"value": value})
    elif search_criteria == 'Hotel':
        query = text("""
        SELECT j.ID_Jogos, j.Jornada, h.Nome AS Lugar, h.Endereco
        FROM JOGOS j
        JOIN SALAO s ON s.ID_Salao = j.ID_Salao
        JOIN HOTEL h ON h.ID_Hotel = s.ID_Hotel
        WHERE h.Nome = :value
        """)
        result = connection.execute(query, {"value": value})
    elif search_criteria == 'Referee':
        query = text("""
        SELECT j.ID_Jogos, j.Jornada, h.Nome AS Lugar, h.Endereco
        FROM JOGOS j
        JOIN PESSOA p ON p.NumAssociado = j.NumAssociado
        JOIN SALAO s ON s.ID_Salao = j.ID_Salao
        JOIN HOTEL h ON h.ID_Hotel = s.ID_Hotel
        WHERE p.Nome = :value
        """)
        result = connection.execute(query, {"value": value})
    else:
        return []

    games = []
    for row in result:
        formatted_row = [str(row[0]), str(row[1]), row[2], row[3]]
        games.append(formatted_row)

    return games

# Define the search criteria options
search_criteria_options = ['Player', 'Hotel', 'Referee']

# Create the GUI window
layout = [
    [sg.Text('Search Criteria:'), sg.Combo(search_criteria_options, key='-CRITERIA-', enable_events=True)],
    [sg.Text('Search Value:'), sg.InputText(key='-VALUE-')],
    [sg.Button('Search'), sg.Button('Close')],
    [sg.Table(values=[], headings=['Game ID', 'Journey', 'Location', 'Address'],
              justification='center',
              auto_size_columns=False,
              col_widths=[10, 10, 20, 20],
              key='-TABLE-')]
]

window = sg.Window('Game Search', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Close':
        break
    elif event == 'Search':
        search_criteria = values['-CRITERIA-']
        search_value = values['-VALUE-']
        games = perform_search(search_criteria, search_value)
        window['-TABLE-'].update(values=games)

# Close the database connection
connection.close()

# Close the GUI window
window.close()
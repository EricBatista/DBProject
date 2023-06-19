from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
import PySimpleGUIQt as sg

# Set up the database connection
engine = create_engine('postgresql://postgres:admin@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()

# Execute the query
query = text('''
    SELECT j.Jornada, h.Nome AS Lugar, h.Endereco,
       array_to_string(array_agg(DISTINCT p1.Nome), ', ') AS Jogadores,
       array_to_string(array_agg(DISTINCT p2.Nome), ', ') AS Arbitros
FROM JOGOS j
JOIN Jogador_Participa_Jogo jpj ON jpj.ID_Jogos = j.ID_Jogos
JOIN PESSOA p1 ON p1.NumAssociado = jpj.NumAssociado
JOIN PARTICIPA_CAMPEONATO pc ON pc.NumAssociado = p1.NumAssociado
JOIN PESSOA p2 ON p2.NumAssociado = j.NumAssociado
JOIN SALAO s ON s.ID_Salao = j.ID_Salao
JOIN HOTEL h ON h.ID_Hotel = s.ID_Hotel
GROUP BY j.ID_Jogos, j.Jornada, s.ID_Salao, h.Nome, h.Endereco;
''')

results = session.execute(query)

# Convert the results to a list of lists for PySimpleGUI
table_data = []
for row in results:
    table_row = list(row)
    # Format the player names
    jogadores = ' '.join(table_row[3].split()).replace("       ", " ")
    arbitros = ' '.join(table_row[4].split()).replace("       ", " ")
    table_row[3] = jogadores
    table_row[4] = arbitros
    # Convert the date object to a formatted string
    table_row[0] = table_row[0].strftime("%Y-%m-%d")
    table_data.append(table_row)

# Close the session
session.close()

# Define the GUI layout
layout = [
    [sg.Table(values=table_data, headings=list(results.keys()), num_rows=10, justification='left', auto_size_columns=True)],
    [sg.Button('Exit')]
]

# Create the window
window = sg.Window('Query Results', layout)

# Event loop to process events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

# Close the window
window.close()
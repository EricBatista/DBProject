import psycopg2

import pandas as pds
import PySimpleGUIQt as sg

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

url = URL.create(
    drivername="postgresql",
    username="postgres",
    host="localhost",
    database="postgres",
    password="admin"
)

alchemyEngine = create_engine(url)

# Connect to PostgreSQL server

dbConnection = alchemyEngine.connect();

# Read data from PostgreSQL database table and load into a DataFrame instance

dataFrame = pds.read_sql("SELECT  j.Jornada, h.Nome AS Lugar, h.Endereco, array_agg(DISTINCT p1.Nome) AS Jogadores, array_agg(DISTINCT p2.Nome) AS Arbitros FROM JOGOS j JOIN Jogador_Participa_Jogo jpj ON jpj.ID_Jogos = j.ID_Jogos JOIN PESSOA p1 ON p1.NumAssociado = jpj.NumAssociado JOIN PARTICIPA_CAMPEONATO pc ON pc.NumAssociado = p1.NumAssociado JOIN PESSOA p2 ON p2.NumAssociado = j.NumAssociado JOIN SALAO s ON s.ID_Salao = j.ID_Salao JOIN HOTEL h ON h.ID_Hotel = s.ID_Hotel GROUP BY j.ID_Jogos, j.Jornada, s.ID_Salao, h.Nome, h.Endereco;", dbConnection);

pds.set_option('display.expand_frame_repr', False);

# Print the DataFrame


dataframeValues = dataFrame.values

print(dataframeValues)

headings = dataFrame.head()

layout = [[sg.Table(values=dataframeValues, headings=headings,
                    auto_size_columns=True
                    )]]

window = sg.Window('Sample excel file', layout)
event, value = window.read()

# Close the database connection

dbConnection.close();

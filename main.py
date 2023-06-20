import PySimpleGUI as sg
import subprocess

# Define the list of available Python programs
programs = [
    {'name': 'Programação Jogos'},
    {'name': 'Num de Movimentos Por Jogo'},
    {'name': 'Jogador Por País'},
    {'name': 'Pesquisar Partida'}
    # Add more programs as needed
]

programsDict = {
    'Programação Jogos': 'program1.py',
    'Num de Movimentos Por Jogo': 'program2.py',
    'Jogador Por País': 'program3.py',
    'Pesquisar Partida': 'program4.py'
}

# Define the layout for the GUI
layout = [
    [sg.Text('Select a program to run:')],
    [sg.Listbox(values=[program['name'] for program in programs], size=(30, len(programs)), key='-PROGRAMS-')],
    [sg.Button('Run'), sg.Button('Close')]
]

window = sg.Window('Program Selector', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Close':
        break
    elif event == 'Run':
        selected_index = values['-PROGRAMS-'][0]
        selected_program = programsDict[selected_index]
        try:
            subprocess.run(['python', selected_program], check=True)
        except subprocess.CalledProcessError as e:
            sg.popup_error(f"Error running program: {str(e)}")


window.close()

import PySimpleGUI as sg

# Define the layout with dynamic buttons
values = ['Value 1', 'Value 2', 'Value 3']
buttons = [[sg.Button(value, key=f'button_{value}')] for value in values]
layout = [[sg.Text('Select a value:')],
          [sg.Column(buttons, size=(200, 100), scrollable=True)]]

# Create the window
window = sg.Window('Dynamic Button Events', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    # Generate an event based on the dynamic button value
    if event.startswith('button_'):
        selected_value = event.split('_')[1]
        sg.popup(f'Selected value: {selected_value}')

# Close the window
window.close()

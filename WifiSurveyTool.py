#!/usr/bin/env python
import PySimpleGUI as sg
import Functions as f
import matplotlib.pyplot as plt
from mpl_point_clicker import clicker
import cv2
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import numpy as np


# Table field names
fields = ['SSID', 'BSSID', 'RSSI', 'CHANNEL', 'HT', 'CC', 'SECURITY']

# Image file types
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

# ------ Make the Table Data ------
data = []
headings = fields


legend = " "

# List of values to use for radio buttons
values = f.get_all_max_bssid('Data/newdata.csv')

# Create a list of radio buttons with a variable assigned to each one
radio_buttons = [sg.Radio(
    value, 'Group 1', k=f'-R{i}', font=15) for i, value in enumerate(values)]

# Create the window and set its size to the screen resolution
screen_resolution = sg.Window.get_screen_size()


access_point_lists = [[sg.Text("Select accesspoint", font=15)],
                      [sg.Column([[button] for button in radio_buttons],
                                 element_justification='l')]
                      ]


# ------ Window Layout c------
tab1_layout = [[sg.Table(values=data, headings=headings, max_col_width=50,
                         auto_size_columns=False,
                         def_col_width=20,
                         display_row_numbers=False,
                         justification='left',
                         num_rows=35,
                         key='-TABLE-',
                         font='Courier 18',
                         selected_row_colors='black on lightgray',
                         enable_events=True,
                         text_color='white',
                         expand_x=True,
                         expand_y=False,
                         vertical_scroll_only=False,
                         select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                         # Comment out to not enable header and other clicks
                         enable_click_events=True,
                         )],
               [sg.Button('Scan'),
                sg.Button('Delete'), sg.Button('CSV'), sg.Button('Exit')]
               ]

Second_layout = [
    # [sg.T('Import new Project', justification='center')],
    [sg.Input(
        size=(1, 1), key="-FILE-", visible=False), sg.FileBrowse(file_types=file_types), sg.B('Import'), sg.B('HeatMap'), sg.Canvas(key='controls_cv',)],
    [sg.T('Figure:', visible=False)],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(600 * 2, 900)
                       )]
        ],
        pad=(0, 0)
    )]
]


tab2_layout = [
    [sg.Column(Second_layout, expand_x=True, element_justification='center'),
     #  sg.VSeperator(),
     sg.Column(access_point_lists)]
]


# main layout
layout = [[sg.TabGroup([[sg.Tab('Discover', tab1_layout, key='-mykey-'),
                        sg.Tab('Survey', tab2_layout)]], key='-group1-', tab_location='top', selected_title_color='white')]]


window = sg.Window('Indoor Wifi Survey Tool', layout,
                   size=screen_resolution, resizable=False, finalize=True)


while True:
    event, values = window.read()

    fig = None
    ax = None

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    elif event == 'Scan':
        new_data = f.get_data()
        window['-TABLE-'].update(values=new_data)

    elif event == 'CSV':
        f.make_csv(new_data)

    elif event == 'Delete':
        if values['-TABLE-'] == []:
            sg.popup('No Row selected')
        else:
            del new_data[values['-TABLE-'][0]]
            window['-TABLE-'].update(values=new_data)

    elif event == 'Import':
        pic = plt.imread(values["-FILE-"])
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        fig = plt.figure(frameon=False)
        ax = fig.add_subplot()
        ax.imshow(pic)
        ax.tick_params(labelsize="xx-small")
        ax.axis('off')
        klicker = clicker(ax, [legend], markers=['o'], colors="red")
        DPI = fig.get_dpi()
        fig.set_size_inches(500 * 2 / float(DPI), 800 / float(DPI))
        klicker.on_class_changed(f.class_changed_cb)
        klicker.on_point_added(f.point_added_cb)
        klicker.on_point_removed(f.point_removed_cb)
        f.draw_figure_w_toolbar(
            window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)

        # Get the size of the imported image and store it in a variable called 'import_size'
        import_size = pic.shape[:2]

    elif event == 'HeatMap':
        all_max_bssid_value, max_bssid_value, xcoordinates, ycoordinates, rssi = f.process_data(
            'Data/newdata.csv')
        xco = xcoordinates
        yco = ycoordinates
        rv = rssi

        # Call plot_porosity_estimate and get the heat map data, pass 'import_size' instead of 'image_size'
        zstar = f.plot_porosity_estimate(xco, yco, rv, import_size)

        red = mcolors.colorConverter.to_rgb('#FF0000')
        green = mcolors.colorConverter.to_rgb('#00FF00')
        cmap = mcolors.LinearSegmentedColormap.from_list(
            'mycmap', [red, green], N=10)

        # Overlay the heat map on top of the imported image, set the extent of the overlay image to match the extent of the imported image
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.imshow(pic)
        vmin, vmax = -90, -50
        heatmap = ax.imshow(zstar, alpha=0.8, cmap=cmap, interpolation='lanczos',
                            extent=[0, import_size[1], import_size[0], 0])

        ax.axis('off')  # remove axis border
        DPI = fig.get_dpi()
        fig.set_size_inches(500 * 2 / float(DPI), 800 / float(DPI))

        cbar = plt.colorbar(heatmap, orientation='vertical',
                            shrink=0.5, pad=0.05, aspect=10)
        cbar.ax.tick_params(labelsize="xx-small")
        cbar.ax.set_ylabel('RSSI', rotation=270, labelpad=15, fontsize='small')
        ax.set_xlabel('')
        ax.set_ylabel('')
        f.draw_figure_w_toolbar(
            window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)


window.close()

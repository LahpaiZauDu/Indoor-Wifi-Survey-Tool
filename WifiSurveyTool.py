#!/usr/bin/env python
import PySimpleGUI as sg
import Functions as f
import matplotlib.pyplot as plt
from mpl_point_clicker import clicker

# Table field names
fields = ['SSID', 'BSSID', 'RSSI', 'CHANNEL', 'HT', 'CC', 'SECURITY']

# Image file types
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

# ------ Make the Table Data ------
data = []
headings = fields


legend = " "

access_point_lists = [
    [sg.Text("Select accesspoint")],
    [sg.Radio('e4:26:86:e0:fc:37', 'Group 1', k='-R1', font=15)],
    [sg.Radio('e4:26:86:e0:40:a7', 'Group 1', k='-R2', font=15)],


]

# ------ Window Layout c------
tab1_layout = [[sg.Table(values=data, headings=headings, max_col_width=50,
                         auto_size_columns=False,
                         def_col_width=15,
                         display_row_numbers=False,
                         justification='left',
                         num_rows=20,
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
    [sg.T('Import new Project')],
    [sg.Input(
        size=(1, 1), key="-FILE-", visible=False), sg.FileBrowse(file_types=file_types), sg.B('Import'), sg.Canvas(key='controls_cv',)],
    [sg.T('Figure:', visible=False)],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(500 * 2, 400)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )]

]


# tab2_layout = [[sg.Frame('', Second_layout)]]


tab2_layout = [
    [sg.Column(Second_layout),
     sg.VSeperator(),
     sg.Column(access_point_lists)]
]


# main layout
layout = [[sg.TabGroup([[sg.Tab('Discover', tab1_layout, key='-mykey-'),
                        sg.Tab('Survey', tab2_layout)]], key='-group1-', tab_location='top', selected_title_color='white')]]


window = sg.Window('Indoor Wifi Survey Tool', layout,
                   size=(1214, 468), finalize=True)


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    # print selected row value from ['-Table-']
    # elif event == '-TABLE-':
    #     data_selected_row = [data[row] for row in values[event]]
    #     print(data_selected_row[0])
    #     f.make_csv()

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
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.imshow(pic)
        ax.tick_params(labelsize="xx-small")
        klicker = clicker(ax, [legend],
                          markers=['o'], colors="red")
        fig = plt.gcf()
        DPI = fig.get_dpi()
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        klicker.on_class_changed(f.class_changed_cb)
        klicker.on_point_added(f.point_added_cb)
        klicker.on_point_removed(f.point_removed_cb)

        f.draw_figure_w_toolbar(
            window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)


window.close()

import subprocess
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


# returns data as array list
def get_data():
    scan_cmd = subprocess.Popen(
        ['sudo', 'airport', '-s'],    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scan_out, scan_err = scan_cmd.communicate()
    scan_out_data = []
    scan_out_lines = str(scan_out).split("\\n")[1:-1]
    for each_line in scan_out_lines:
        split_line = [e for e in each_line.split(" ") if e != ""]
        while len(split_line) > 7:
            new_value = split_line[0] + split_line[1]
            del split_line[0]
            split_line[0] = new_value
        scan_out_data.append(split_line)
    return scan_out_data


# make csv
def make_csv(datas):
    # field names
    fields = ['SSID', 'BSSID', 'RSSI', 'CHANNEL', 'HT', 'CC', 'SECURITY']
    rows = datas
    with open('./Data/Home_Access_points.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


def draw_figure_w_toolbar_2(canvas, fig):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


def class_changed_cb(new_class: str):
    print(f'The newly selected class is {new_class}')


def point_added_cb(position: Tuple[float, float], klass: str):
    x, y = position
    mylist = [x, y]
    scan_cmd = subprocess.Popen(
        ['sudo', 'airport', '-s'],    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    scan_out, scan_err = scan_cmd.communicate()
    scan_out_data = []
    scan_out_lines = str(scan_out).split("\\n")[1:-1]
    for each_line in scan_out_lines:
        split_line = [e for e in each_line.split(" ") if e != ""]
        while len(split_line) > 7:
            new_value = split_line[0] + split_line[1]
            del split_line[0]
            split_line[0] = new_value
        scan_out_data.append(split_line + mylist)

    fields = ['SSID', 'BSSID', 'RSSI', 'CHANNEL',
              'HT', 'CC', 'SECURITY', 'Xcoordinate', 'Ycoordinate']
    rows = scan_out_data
    with open('./Data/20_floor5.csv', 'a') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)


def point_removed_cb(position: Tuple[float, float], klass: str, idx):
    x, y = position

    suffix = {'1': 'st', '2': 'nd', '3': 'rd'}.get(str(idx)[-1], 'th')
    print(
        f"The {idx}{suffix} point of class {klass} with position {x=:.2f}, {y=:.2f}  was removed"
    )


def plot_porosity_estimate(xco, yco, rss, image_size):

    x = xco
    y = yco
    phi = rss
    OK = OrdinaryKriging(
        x,
        y,
        phi,
        verbose=True,
        enable_plotting=False,
        nlags=3,
        variogram_model="spherical",
    )

    OK.variogram_model_parameters

    # Calculate grid points based on image size
    x_min, y_min, x_max, y_max = 0, 0, image_size[1], image_size[1]
    x_range = x_max - x_min
    y_range = y_max - y_min
    gridx = np.arange(x_min, x_max, x_range/40)
    gridy = np.arange(y_min, y_max, y_range/40)

    zstar, ss = OK.execute("grid", gridx, gridy)
    return zstar


def process_data(csv_file):
    df = pd.read_csv(csv_file)
    channel_values = ['1', '11', '36']
    df_sv = df[df.CHANNEL.isin(channel_values)]
    five_column = df_sv[['SSID', 'BSSID', 'RSSI',
                         'CHANNEL', 'Xcoordinate', 'Ycoordinate']]
    df = five_column

    # sort RSSI value in original dataframe
    df = df.sort_values(['RSSI'], ascending=True)

    # To list the count of BSSID values in the pivot table from minimum to maximum
    df_pivot = df.pivot_table(index=['BSSID'], aggfunc='size')
    df_pivot_sorted = df_pivot.sort_values(
        ascending=True).reset_index(drop=True)

    # To check how many BSSID values have the maximum count in the pivot table and select their BSSID values
    max_count = df_pivot.max()
    all_max_bssid = df_pivot[df_pivot == max_count].index.tolist()
    max_bssid = df_pivot[df_pivot == max_count].index[0]

    # To drop rows from the original DataFrame df if the count of BSSID values in the pivot table is not the maximum count
    # df2 = df[df['BSSID'].isin(max_bssid)]
    df2 = df[df['BSSID'] == max_bssid]

    xcoordinates = df2['Xcoordinate'].to_numpy()
    ycoordinates = df2['Ycoordinate'].to_numpy()
    rssi = df2['RSSI'].to_numpy()

    return all_max_bssid, max_bssid, xcoordinates, ycoordinates, rssi


def get_all_max_bssid(csv_file):
    all_max_bssid, _, _, _, _ = process_data(csv_file)
    return all_max_bssid


def new_average(csv_file):

    # Load data from CSV
    df = pd.read_csv(csv_file)

    # remove rows with missing values
    df_remove = df.dropna()

    # Filter the dataframe to only include rows where RSSI contains '-'
    df_Filter = df_remove[df_remove['RSSI'].str.contains('-')]

    # Group data by X and Y coordinates, and apply the 'list' function to the RSSI column
    df_grouped = df_Filter.groupby(['Xcoordinate', 'Ycoordinate', 'BSSID'])[
        'RSSI'].apply(list).reset_index()

    # Calculate the average RSSI for each row
    df_grouped['RSSI_Max'] = df_grouped['RSSI'].apply(
        lambda x: np.max([int(i) for i in x]))

    # Create a new column for the access point MAC address by removing the last 3 octets of the BSSID
    df_grouped['BSSID_Sumarize'] = df_grouped['BSSID'].apply(
        lambda x: ':'.join(x.split(':')[:3]))

    # Group by unique combination of ['Xcoordinate', 'Ycoordinate', 'BSSID_Sumarize'] and list the RSSI_mean values
    df_grouped_all_max = df_grouped.groupby(['Xcoordinate', 'Ycoordinate', 'BSSID_Sumarize'])[
        'RSSI_Max'].apply(list).reset_index()

    # Create a new column for the overall mean RSSI for each unique combination of ['Xcoordinate', 'Ycoordinate', 'BSSID_Sumarize']
    df_grouped_all_max['Max_lists'] = df_grouped_all_max['RSSI_Max'].apply(
        lambda x: np.max(x))

    # Group by unique combination of ['Xcoordinate', 'Ycoordinate'] and list the unique RSSI_all_mean values
    df_grouped_coord_max = df_grouped_all_max.groupby(
        ['Xcoordinate', 'Ycoordinate', 'BSSID_Sumarize'])['Max_lists'].unique().reset_index()

    # Get count duplicates single column using dataframe.pivot_table()
    df2 = df_grouped_coord_max.pivot_table(
        index=['BSSID_Sumarize'], aggfunc='size')

    max_count = df2.max()
    max_bssid = df2[df2 == max_count].index.tolist()

    df4 = df_grouped_coord_max[df_grouped_coord_max['BSSID_Sumarize'].isin(
        max_bssid)]
    # df4 = df_grouped_coord_max.sort_values(['BSSID_Sumarize'],ascending=True)

    df5 = df4.loc[df4['BSSID_Sumarize'] == '00:b6:70']

    df5.loc[:, 'Max_lists'] = df5['Max_lists'].astype(int)

    df5.to_csv('Data/New_MAX.csv', index=False)

    # Load the updated data from the CSV file
    newdata = pd.read_csv('Data/New_MAX.csv')

    xcoordinates = np.array(newdata['Xcoordinate'])
    ycoordinates = np.array(newdata['Ycoordinate'])
    rssi = np.array(newdata['Max_lists'])

    print(rssi)

    return xcoordinates, ycoordinates, rssi


def Validation(xco, yco, rss, xcoords, ycoords):
    x = xco
    y = yco
    phi = rss

    print('Original')
    print(phi)
    OK = OrdinaryKriging(
        x,
        y,
        phi,
        verbose=True,
        enable_plotting=False,
        nlags=100,
        variogram_model="spherical",
    )

    # Call execute with the ground truth coordinates to get the estimated porosity values at those locations
    zsstar, ss = OK.execute("points", xcoords, ycoords)

    return zsstar


def Validation_points(csv_file):

    # Load data from CSV
    df = pd.read_csv(csv_file)
    xcoordinates = np.array(df['Xcoordinate'])
    ycoordinates = np.array(df['Ycoordinate'])
    rssi = np.array(df['Max_lists'])

    return xcoordinates, ycoordinates, rssi


def Random_Validation_points(csv_file):

    # Load data from CSV
    df = pd.read_csv(csv_file)
    # drop any duplicate rows
    df = df.drop_duplicates()
    # randomly select 5 rows
    result = df.sample(n=9, random_state=np.random.randint(100))
    xcoordinates = np.array(result['Xcoordinate'])
    ycoordinates = np.array(result['Ycoordinate'])
    rssi = np.array(result['Max_lists'])

    return xcoordinates, ycoordinates, rssi

import subprocess
import csv
import cv2
from PIL import ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from typing import Tuple


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
def make_csv():
    # field names
    fields = ['SSID', 'BSSID', 'RSSI', 'CHANNEL', 'HT', 'CC', 'SECURITY']
    rows = get_data()
    with open('./data/home.csv', 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)


def Capture_Event(event, x, y, flags, params):
    # If the left mouse button is pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        # Print the coordinate of the
        # clicked point
        print(f"({x}, {y})")


def FilePath(filepath):
    tostring = str(filepath)
    img = cv2.imread(tostring, 1)
    # Show the Image
    cv2.imshow('image', img)
    # Set the Mouse Callback function, and call
    # the Capture_Event function.
    cv2.setMouseCallback('image', Capture_Event)
    # Press any key to exit
    cv2.waitKey(0)
    # Destroy all the windows
    cv2.destroyAllWindows()


def add_line(im, color):
    draw = ImageDraw.Draw(im)
    draw.line((0, 0) + im.size, fill=color, width=10)
    draw.line((0, im.size[1], im.size[0], 0), fill=color, width=10)
    return im


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


def class_changed_cb(new_class: str):
    print(f'The newly selected class is {new_class}')


def point_added_cb(position: Tuple[float, float], klass: str):
    x, y = position
    print(f"New point of class {klass} added at {x=}, {y=}")


def point_removed_cb(position: Tuple[float, float], klass: str, idx):
    x, y = position

    suffix = {'1': 'st', '2': 'nd', '3': 'rd'}.get(str(idx)[-1], 'th')
    print(
        f"The {idx}{suffix} point of class {klass} with position {x=:.2f}, {y=:.2f}  was removed"
    )

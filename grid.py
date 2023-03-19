import PySimpleGUI as sg
import cv2

# Define the layout of the window
layout = [
    [sg.Text("Select an image file:")],
    [sg.Canvas(key='-IMAGE-',
               # it's important that you set this size
               size=(600 * 2, 900)
               )],
    [sg.Input(key="-FILE-", enable_events=True), sg.FileBrowse()],
    [sg.Text("Enter the number of rows and columns for the grid:")],
    [sg.Text("Rows:"), sg.Input(key="-ROWS-", size=(5, 1)),
     sg.Text("Columns:"), sg.Input(key="-COLS-", size=(5, 1))],
    [sg.Button("Create Grid"), sg.Exit()]
]

# Create the window
window = sg.Window("Image Grid Creator", layout)

while True:
    event, values = window.read()

    # Close the window if the user clicks the Exit button
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    # If the user selects an image file, display the image in the window
    if event == "-FILE-":
        filename = values["-FILE-"]
        image = cv2.imread(filename)
        height, width, _ = image.shape
        window["-IMAGE-"].update(data=cv2.imencode(".png", image)[1].tobytes())

    # If the user clicks the Create Grid button, overlay a grid on top of the image
    if event == "Create Grid":
        rows = int(values["-ROWS-"])
        cols = int(values["-COLS-"])
        if filename:
            image_with_grid = image.copy()
            row_height = height // rows
            col_width = width // cols
            # Draw horizontal lines
            for i in range(1, rows):
                cv2.line(image_with_grid, (0, i*row_height),
                         (width, i*row_height), (255, 0, 0), 2)
            # Draw vertical lines
            for j in range(1, cols):
                cv2.line(image_with_grid, (j*col_width, 0),
                         (j*col_width, height), (255, 0, 0), 2)
            # Display the image with grid overlayed
            window["-IMAGE-"].update(data=cv2.imencode(".png",
                                     image_with_grid)[1].tobytes())

# Close the window when the loop exits
window.close()

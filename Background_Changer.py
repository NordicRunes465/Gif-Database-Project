# Frontend Developer: Colin A. Lewis
# Backend Developer: Isaiah Runkles
# Project Manager: Tyler Pressens

# Company: JRTI Software Development
# Date: Wednesday, September 14th, 2022
import Variables as V
import background_shuffler
import PySimpleGUI as sg
import datetime as dt
import requests


# This code is going to be the main GUI for the background changer program.

# This program is an attempt at addressing the issue of complicated or overpriced desktop background services.

# Colin plans to add the Weather API here, once that has been added to the mainframe.
# The API will display the time, date, and weather on top of the currently playing gif

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.12
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "c189de86d43ce000e3861d001042d9e4"
CITY = "Harpers Ferry"

hasCity = True
sg.theme("DarkTeal9")

# Main Window Layout (will include empty keys & variables until the main source code is finished)
# Everyone's work will be threaded through to the main gui I have created once each portion is finished,  each persons name will be above that which was threaded / created by them.
# Good news, the weatherAPI Tyler made has been threaded through to the mainframe successfully, one more milestone knocked out. Now to see about those bug issues.
# Colin's part of the mainframe

layout = [[sg.Text('Gif Background Changer', justification='center', relief='flat', size=(40, 10))],
          [sg.Text('Run the Program in the background by clicking the button: ', justification='center')],
          [sg.Button('Run the Program in Background', enable_events=True, key='rn')],
          [sg.Button('Save', key='sve', enable_events=True, size=(10, 1))]
          ]

# Isaiah's part of the Mainframe (threaded / put into it's own tab.)

layout2 = [[sg.Text("Select a Gif preset here: ", size=(10, -5))],
           [sg.Button('Summer', key='Summer', size=(10, 1)),
            sg.Button('Campfire', key='Campfire', size=(10, 1))], [sg.Button('Fall', key='Fall', size=(10, 1))],
           [sg.Button('nighttime', key='Night', size=(10, 1))],
           [sg.Button('Winter', key='Winter', size=(10, 1))],
           [sg.Button('Confirm', key='Confirm', size=(10, 1))]]

network3 = [[sg.Text('Network gifs', size=(10, -5))],
            [sg.Button('Access Gif Database', key='acss')],
            [sg.Listbox()],
            ]

layout3 = [[sg.Text("Weather Extractor", size=(60, 1), justification="center")],
           [sg.Text("Written By: Tyler Pressens", size=(60, 1), justification='center')],
           [sg.Image(filename="images/bg.png", key="-IMAGE")],
           [sg.Text("City Selection", justification="center")],
           [sg.InputText(key="citySelection", size=(30, 1), disabled=False)],
           [sg.Button("Search City", key="OK")],
           [sg.Multiline(key="-CANVAS-", size=(60, 10))]]

# My tab grouping of the tabs
tablayout = [[sg.TabGroup([[sg.Tab('Presets', layout2, key='presetTab'),
                            sg.Tab('Run in BG', layout, key='Gifprst'),
                            sg.Tab('Weather', layout3, key='weather')
                            ]], enable_events=True, key="tab")]]

fLayout = sg.Window('Gif Background Changer', location=(0, 0),
                    finalize=True, resizable=True,
                    element_justification="center",
                    font="Helvetica 18", layout=tablayout)

# While running loop


running = True

while running:
    event, values = fLayout.read(timeout=1000, timeout_key='__TIMEOUT__', close=False)

    # Closes the fLayout once the X button is clicked.

    if event == sg.WINDOW_CLOSED:
        break

    # When the button is pressed, this elif statement allows the fLayout to run in the background once the button is pressed
    # Program crashes after confirm is hit, looking for solutions with Isaiah to fix this.
    # Somewhere around this area is where the bug could be, no solutions just yet.
    elif event == 'rn':
        fLayout.AlphaChannel = 0

    # empty for now until a variable and function is created so it can be called everytime the Save button is pressed.

    elif event == 'Summer':
        V.number = 1

    elif event == 'Campfire':
        V.number = 2

    elif event == 'nighttime':
        V.number = 3

    # Colin will be adding more Gif presets.
    elif event == 'Winter':
        V.number = 4

    elif event == 'Fall':
        V.number = 5

    elif event == 'Confirm':
        background_shuffler.shuffle(.13)
        sg.Window.alpha_channel = 1

    # Tyler's Weather API / other portion I threaded in.
    if event == "OK" or event == sg.WIN_CLOSED:
        CITY = values["citySelection"]
        url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
        response = requests.get(url).json()
        print(response)

        if 'Nothing to geocode' in dict.values(response) or 'city not found' in dict.values(response):
            fLayout["-CANVAS-"].update("Invalid City", text_color='red', justification='center')
            CITY = "New York"
            print(CITY)
            hasCity = False

        else:
            hasCity = True

        if hasCity:
            fLayout["-CANVAS-"].update(text_color='black', justification='center')
            temp_kelvin = response['main']['temp']
            temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
            feels_like_kelvin = response['main']['feels_like']
            feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
            humidity = response['main']['humidity']
            wind_speed = response['wind']['speed']
            description = response['weather'][0]['description']
            sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
            sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

            fLayout["-CANVAS-"].update(f"City: {CITY}\nTemperature: {temp_fahrenheit}F / {temp_celsius}C\n"
                                       f"Feels Like: {feels_like_fahrenheit}F / {feels_like_celsius}C\n"
                                       f"Humidity: {humidity}\n"
                                       f"Wind Speed: {wind_speed}\nSun Rises at: {sunrise_time} local time.\n"
                                       f"Sun Sets at {sunset_time} local time.\nWeather Report: {description}")

        else:
            fLayout["-CANVAS-"].update("Invalid City")

fLayout.close()

# I plan to add the variables / function calls once the Database is done.

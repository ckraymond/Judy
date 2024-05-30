import openai
import PySimpleGUI as sg
import sounddeice

from data_file_io import dataFile

def getpromptparams(filename):
    params = dataFile(filename)
    params.readfile()
    return params

def api_call(query):
# Call to the OpenAI API
# Only parameter is the query
    api_call_params = getpromptparams('system_content_role.dat')
    client = openai.OpenAI()

    completion = client.chat.completions.create(
        model = api_call_params.data['model'],
        temperature = float(api_call_params.data['temperature']),
        messages=[
            {"role": "system", "content": api_call_params.data['content']},
            {"role": "user", "content": query}
        ]
    )

    return completion.choices[0].message.content

def open_dialog(api_response='Hello!'):
    sg.theme('DarkBlue')
    sg.set_options(font=('Arial', 14))
    query_input = sg.Input(key = '-IN-', expand_x = True, expand_y = True)
    query_output = sg.Multiline(api_response, key='output_box', size=(700, 15))
    layout = [[sg.Text('Welcome to Judy. Just submit your question and I will respond back.')],
              [sg.Push(), query_input, sg.Push()],
              [sg.Push(), query_output, sg.Push()],
              [sg.Push(), sg.Button('Submit', bind_return_key=True), sg.Button('Quit'), sg.Push()]]

    window = sg.Window('Judy v0.01', layout, size = (900, 400), resizable = False)

    while True:
        event, values = window.read()

        if event in('Quit', None, sg.WIN_CLOSED):
            break
        elif event == 'Submit':
            query_output = api_call(values['-IN-'])
            window['-IN-'].update('')
            window['output_box'].update(values['-IN-'] + "\n" + query_output)

open_dialog()
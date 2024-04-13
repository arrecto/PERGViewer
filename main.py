from gui import *
import numpy as np
import os


patient_index = 0
csv_files = []

def read_perg(file, patient_index, window):
    global fig_agg1, fig_agg2, fig_agg3
    
    #if plot exists in the canvas
    if fig_agg1 is not None:
        delete_fig_agg(fig_agg1, ax1)
    if fig_agg2 is not None:
        delete_fig_agg(fig_agg2, ax2)
    if fig_agg3 is not None:
        delete_fig_agg(fig_agg3, ax3)
    
    # Read the CSV file
    df = pd.read_csv(file)

    # Get the number of columns in the DataFrame
    num_columns = len(df.columns) // 3
    update_listbox(num_columns, window)
    #print patient_details in the side
    #patient_details(csv_files[patient_index], window, patient_index, num_columns)
    patient_details(file, window, patient_index, num_columns)
    #plot_csv_file(csv_files[patient_index], patient_index,0, 'RE_1', 'LE_1', fig1, ax1)
    plot_csv_file(file, patient_index,0, 'RE_1', 'LE_1', fig1, ax1)
    fig_agg1 = draw_figure(window['-CANVAS1-'].TKCanvas, plt.gcf())
    window['-CANVAS1-'].update(visible=True)
    if num_columns == 1:
        window['-CANVAS2-'].update(visible=False)
        window['-CANVAS3-'].update(visible=False)
    if num_columns >= 2:
        plot_csv_file(file, patient_index, 3, 'RE_2', 'LE_2', fig2, ax2)
        fig_agg2 = draw_figure(window['-CANVAS2-'].TKCanvas, plt.gcf())

        window['-CANVAS2-'].update(visible=True)
        window['-CANVAS3-'].update(visible=False)

    if num_columns >= 3:
        plot_csv_file(file, patient_index, 6, 'RE_3', 'LE_3', fig3, ax3)
        fig_agg3 = draw_figure(window['-CANVAS3-'].TKCanvas, plt.gcf())

        window['-CANVAS3-'].update(visible=True)
    window.Refresh()

def get_csv_files_in_folder(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    return csv_files

#create figure
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

layout_patient_info = [[sg.Text('ID Record:', key='-ID_RECORD-')],
                       [sg.Text('Date: ', key='-DATE-')],
                       [sg.Text('Age: ', key='-AGE-')],
                       [sg.Text('Sex: ', key='-SEX-')],
                       [sg.Text('Samples: ', key='-SAMPLE-')],
                       [sg.Text('Unilateral: ', key='-UNILATERAL-')],
                       [sg.Text('Remarks: ', key='-REMARK-')]]

layout1 = [[sg.Input(key="-PATIENTINDEX-", size=(5,1)), sg.Button("Search")],
           [sg.Frame('Patient Information', layout_patient_info)],
           [sg.VPush()],
           [sg.Button("Back"),sg.Button("Next")],
           [sg.Listbox([], size=(8, 5), key='-LIST-')],
           [sg.Text("Level Decomp"), sg.Input(key="-LEVELDECOMP-",size=(5,1))],
           [sg.Button('Denoise')],
           [sg.Button('Add'), sg.Button('Remove')]]
layout2 = [
    [sg.Text("Select Folder"), sg.Input(key="-FOLDER-"), sg.FolderBrowse(), sg.Button('Plot'), sg.Button("Exit")],
    [sg.Column([[sg.Text('PERG plot will be shown here')]],size=(800,500), key='-PLOTCOLUMN-', visible=True), 
     sg.TabGroup([[sg.Tab("TE_1", [[sg.Canvas(size=(1000, 500), key='-CANVAS1-')]]), sg.Tab("TE_2", [[sg.Canvas(size=(1000, 500), key='-CANVAS2-', visible=False)]]), sg.Tab("TE_3", [[sg.Canvas(size=(1000, 500), key='-CANVAS3-', visible=False)]])]],size=(800,500), visible=False, key='-TAB-')]
]

layout =[[sg.Column(layout1), sg.Column(layout2), sg.Column([[sg.Text('Denoised signal')],[sg.Canvas(size=(300,300), key='-CANVASDENOISE-')]], visible=True)]]

window = sg.Window("PERG Viewer", layout, return_keyboard_events =True, resizable=True, element_justification='center')


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Plot":
        window['-PLOTCOLUMN-'].update(visible=False)
        window['-TAB-'].update(visible=True)
        folder_path = values["-FOLDER-"]

        if folder_path:
            csv_files = get_csv_files_in_folder(folder_path)
            file = folder_path+"/"+csv_files[patient_index]
            if patient_index >= len(csv_files):
                break

            read_perg(file, patient_index, window)
    elif event == 'Search':
        patient_index_input = values["-PATIENTINDEX-"]
        patient_index_input = patient_index_input.zfill(4) + ".csv" 
        if patient_index_input in csv_files:
           patient_index = csv_files.index(patient_index_input)
           file = folder_path+"/"+csv_files[patient_index]
           read_perg(file, patient_index, window) 
        else:
            sg.popup_no_titlebar("The file does not exist!")         
    elif event=='Next':
        if patient_index < len(csv_files)-2:
            patient_index += 1
            file = folder_path+"/"+csv_files[patient_index]
            read_perg(file, patient_index, window)
        else:
            sg.popup_no_titlebar("End of the file.") 
    elif event=='Back':
        if patient_index !=0:
            patient_index -= 1
        else:
            sg.popup_no_titlebar("Cannot move further")
        file = folder_path+"/"+csv_files[patient_index]
        read_perg(file, patient_index, window)
    elif event=='Add':
        eye_side = values['-LIST-']
        if eye_side:  # Check if any option is selected
            eye_side = eye_side[0]  # Get the first selected option

            details = patient_info(file)
            #id eye side
            id_eye = str(details["id_record"][patient_index])+eye_side

            #diagnosis
            diagnosis = details['diagnosis1'][patient_index]

            df = pd.read_csv(file)
            coeff = wt(df, eye_side)
        else: 
            sg.popup_no_titlebar("Please select eye side.")
        data_dict = read_perg_csv('data.csv', columns=['id_eye', 'diagnosis', 'coeff'])
        if id_eye in data_dict['id_eye'].to_numpy() and eye_side:
            sg.popup_no_titlebar("Already added!")
        else:
            perg_details = {'id_eye': id_eye, 'diagnosis': diagnosis, 'coeff': [coeff]}
            append_to_csv('data.csv', perg_details)
    elif event == 'Remove':
        eye_side = values['-LIST-']
        if eye_side:  # Check if any option is selected
            eye_side = eye_side[0]  # Get the first selected option

            details = patient_info(file)
            #id eye side
            id_eye = str(details["id_record"][patient_index])+eye_side
            data_dict = read_perg_csv('data.csv', columns=['id_eye', 'diagnosis', 'coeff'])
            print(id_eye)
            data_dict = data_dict.drop(data_dict[data_dict['id_eye'] == id_eye].index)
            data_dict.to_csv('data.csv', index=False)
        else:
            sg.popup_no_titlebar("Please select eye side.")
    elif event == 'Denoise':
        #global fig_denoise
        window['-CANVASDENOISE-'].update(visible=True)
        eye_side = values['-LIST-']
        if eye_side:  # Check if any option is selected
            eye_side = eye_side[0]  # Get the first selected option
            print('canvas denoise should be visible')
            if fig_denoise is not None:
                delete_fig_agg(fig_denoise, ax4)
        
            # Read the CSV file
            level_decomp_input = values['-LEVELDECOMP-']
            if level_decomp_input.isdigit():
                level_decomp = int(level_decomp_input)
            else:
                level_decomp = 3
            df = pd.read_csv(file)

            time_label = pd.to_datetime(df.loc[:, 'TIME_'+eye_side[-1]], format='mixed')

            df = normalize(df, eye_side)
            
            coeff = pywt.wavedec(df['norm'], 'db4', level=level_decomp, mode='per')
            for i in range(level_decomp-1):
                idx = (i+1)*(-1)
                coeff[idx] = None
            perg_denoise = pywt.waverec(coeff, 'db4', mode='per')
            perg_denoise = pd.DataFrame(perg_denoise)

            fig4, ax4 = plt.subplots(1,1,figsize=(5, 5))
            perg_denoise.plot(legend=False, color='orange')

            ax4.set_xticklabels(time_label.dt.microsecond//1000)
            plt.suptitle("Normalized and Denoised " + eye_side)
            fig_denoise = draw_figure(window['-CANVASDENOISE-'].TKCanvas, plt.gcf())
            print(fig_denoise)
            window.Refresh()
        else:
            sg.popup_no_titlebar("Please select eye side.")
window.close()
import PySimpleGUI as sg
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import pywt
import numpy as np

fig_agg1 = None
fig_agg2 = None
fig_agg3 = None
fig_denoise = None

participants_info = pd.read_csv('participants_info.csv')

#read patient info
def patient_info(file_name):
    file_name = file_name[:-4]
    details = participants_info[participants_info['id_record']==int(file_name)]
    return details

#clear existing canvas
def delete_fig_agg(fig_agg, ax):
    fig_agg.get_tk_widget().forget()
    ax.cla()

#Function for drawing
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def patient_details(file_path, window, patient_index, samples):
    #read patient_info
    details = patient_info(file_path)

    #update patient information
    window['-ID_RECORD-'].update('ID Record: ' + str(details["id_record"][patient_index]))
    window['-DATE-'].update('Date: ' + str(details['date'][patient_index]))
    window['-AGE-'].update('Age: ' +str(details['age_years'][patient_index]))
    window['-SEX-'].update('Sex: '+ str(details['sex'][patient_index]))
    window['-SAMPLE-'].update('Samples: '+ str(samples))
    window['-UNILATERAL-'].update('Samples: '+ str(details['unilateral'][patient_index]))
    
def plot_perg(df, ax, eye_side, time_column, color):
    idx = 0
    if 'LE' in eye_side:
        idx=1
    time_label = pd.to_datetime(df.iloc[:, time_column], format='mixed')
    ax[0][idx].plot(time_label.dt.microsecond//1000, df[eye_side], label=eye_side, color=color)
    ax[0][idx].set_title(eye_side)
    ax[0][idx].set_xlabel("{} in milliseconds".format(df.columns[time_column]))

def update_listbox(columns, window):
    eye_values = []
    for i in range(columns):
        eye_values.append('RE_'+str(i+1))
        eye_values.append('LE_'+str(i+1))
    window['-LIST-'].update(values=eye_values)
    
def plot_csv_file(file_path, patient_index, time_column, right_eye, left_eye, fig, ax):
     
    details = patient_info(file_path)
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Get the number of columns in the DataFrame
    num_columns = len(df.columns) // 3
    fig, ax = plt.subplots(1, 2, figsize=(30, 5))
    ax = [ax]
    time_label = pd.to_datetime(df.iloc[:, time_column], format='mixed')
    plot_perg(df, ax, right_eye, time_column, 'blue')
    plot_perg(df, ax, left_eye, time_column, 'green')
    #plt.tight_layout()
    plt.suptitle(str(details['diagnosis1'][patient_index]))
    return plt.gcf()

def read_perg_csv(filename, columns=None):
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
        return df
    else:
        return pd.read_csv(filename)

def append_to_csv(filename, data):
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', index=False, header=False)

def normalize(perg, eye_side):
  max = perg.max()[eye_side]
  min = perg.min()[eye_side]
  #perg['norm'] = 2*(perg[eye_side]-0.5*(max+min))/(0.5*(max-min))
  perg['norm']=((perg[eye_side]-min)/(max-min))*(2-(-2))+(-2)
  perg = perg.drop(columns=[eye_side])
  return perg

level_decomp = 3
def wt(perg, eye_side):
  perg = normalize(perg, eye_side)
  coeffs = pywt.wavedec(perg['norm'], 'db4', level=level_decomp, mode='per')
  for i in range(level_decomp-1):
    idx = (i+1)*(-1)
    coeffs[idx] = None
  coeffs_flat = np.hstack(coeffs).flatten()
  coeffs_flat = coeffs_flat[coeffs_flat!=np.array(None)]
  return coeffs_flat
        
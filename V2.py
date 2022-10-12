import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import io
import base64
from jinja2 import Environment, FileSystemLoader
import pdfkit




st.title('Generación Informe de Fuerzas')
st.write('---')
st.subheader('Procesamiento y Visualización de Datos')

st.write('Primero, **sube tus archivos CSV**.')
data_csv = st.file_uploader(label = 'Sube los CSV aquí.', type = 'csv', accept_multiple_files=True)

if data_csv:
    st.success('Archivos subidos! Ahora puedes verlos y comenzar a editar la plantilla del informe!')

csv_base = pd.DataFrame()

min_floor = 5
percentile = 99.8

f_max = {
    "f_iqt_der" : 0,
    "f_cc_der" : 0,
    "f_iqt_izq": 0,
    "f_cc_izq": 0,
    "f_gm_der": 0,
    "f_gm_izq" : 0
}

f_mean = {
    "f_iqt_der" : 0,
    "f_cc_der" : 0,
    "f_iqt_izq": 0,
    "f_cc_izq": 0,
    "f_gm_der": 0,
    "f_gm_izq" : 0
}



datos_diagnostico = {
    "hallazgos" : None,
    "recomendaciones" : None
}

graficos = {
    "grafico_iqt_izq" : None,
    "grafico_iqt_der" : None,
    "grafico_cc_izq" : None,
    "grafico_cc_der" : None,
    "grafico_gm_izq" : None,
    "grafico_gm_der" : None
}

frel_der = 0
frel_izq = 0

if data_csv is not None:
    
    col1, col2 = st.columns(2, gap='medium')

    for csv in data_csv:
        name = csv.name
        df = pd.read_csv(csv)
        df.index +=1
        csv.seek(0)
        df.columns = ['ID', 'Fuerza']
        fuerza = df["Fuerza"]
        fuerza_nz = []
        
        for value in fuerza:
            if abs(value) >= min_floor:
                fuerza_nz.append(value)
    
        data_max = np.round(np.max(np.percentile(fuerza, percentile)), 1)
        data_mean = np.round(np.mean(fuerza_nz), 1)

        with col1:
            if 'CC_IZQ' in name:
                with st.expander('Datos Cuadricipital Izquierdo'):
                    f_max["f_cc_izq"] = data_max
                    f_mean["f_cc_izq"] = data_mean                                
                    fig = io.BytesIO()

                    grafico = plt.figure(figsize=(10, 4))
                    
                    graficos['grafico_cc_izq'] = plt.scatter(df['ID'], df['Fuerza'], color = '#F36F59')
                    plt.title('Fuerza Obtenida Cuadricipital Izquierdo [N]')
                    plt.xlabel('Puntos de Medición')
                    plt.ylabel('Fuerza Obtenida')
                    plt.savefig(fig, bbox_inches='tight', format = 'png')
                    st.pyplot(grafico)

                    fig.seek(0)

                    fig_64 = base64.b64encode(fig.getvalue()).decode('utf-8')
                    graficos['grafico_cc_izq'] = f"<img src='data:image/png;base64,{fig_64}' width='300' height='180'/>" 
                    
                    st.write(f"Fuerza Máxima: **{f_max['f_cc_izq']} N**")
                    st.write(f"Promedio Estimado: **{f_mean['f_cc_izq']} N**")  

            if 'IQT_IZQ' in name:
                with st.expander('Datos Isquiotibial Izquierdo'):
                    f_max["f_iqt_izq"] = data_max
                    f_mean["f_iqt_izq"] = data_mean
                    

                    fig = io.BytesIO()

                    grafico = plt.figure(figsize=(10, 4))
                    
                    plt.scatter(df['ID'], df['Fuerza'], color = '#F36F59')
                    plt.title('Fuerza Obtenida Isquiotibial Izquierdo [N]')
                    plt.xlabel('Puntos de Medición')
                    plt.ylabel('Fuerza Obtenida')
                    plt.savefig(fig, bbox_inches = 'tight', format = 'png')
                    st.pyplot(grafico)    

                    fig.seek(0)             

                    fig_64 = base64.b64encode(fig.getvalue()).decode('utf-8') 
                    graficos['grafico_iqt_izq'] = f"<img src='data:image/png;base64,{fig_64}' width='300' height='180'/>"

                    
                    st.write(f"Fuerza Máxima: **{f_max['f_iqt_izq']} N**")
                    st.write(f"Promedio Estimado: **{f_mean['f_iqt_izq']} N**")

            if 'GLUT_MEDIO_IZQ' in name:
                with st.expander('Datos Glúteo Medio Izquierdo'):
                    f_max["f_gm_izq"] = data_max
                    f_mean["f_gm_izq"] = data_mean                                
                    fig = io.BytesIO()

                    grafico = plt.figure(figsize=(10, 4))
                    
                    graficos['grafico_gm_izq'] = plt.scatter(df['ID'], df['Fuerza'], color = '#F36F59')
                    plt.title('Fuerza Obtenida Glúteo Medio Izquierdo [N]')
                    plt.xlabel('Puntos de Medición')
                    plt.ylabel('Fuerza Obtenida')
                    plt.savefig(fig, bbox_inches='tight', format = 'png')
                    st.pyplot(grafico)

                    fig.seek(0)

                    fig_64 = base64.b64encode(fig.getvalue()).decode('utf-8')
                    graficos['grafico_gm_izq'] = f"<img src='data:image/png;base64,{fig_64}' width='300' height='180'/>"
                    
                    st.write(f"Fuerza Máxima: **{f_max['f_gm_izq']} N**")
                    st.write(f"Promedio Estimado: **{f_mean['f_gm_izq']} N**")
        
        with col2:                    
            if 'IQT_DER' in name:
                with st.expander('Datos Isquiotibial Derecho'):
                    f_max["f_iqt_der"] = data_max
                    f_mean["f_iqt_der"] = data_mean
                    
                    
                    fig = io.BytesIO()

                    grafico = plt.figure(figsize=(10, 4))
                    
                    graficos['grafico_iqt_der'] = plt.scatter(df['ID'], df['Fuerza'], color = '#F36F59')
                    plt.title('Fuerza Obtenida Isquiotibial Derecho [N]')
                    plt.xlabel('Puntos de Medición')
                    plt.ylabel('Fuerza Obtenida')
                    plt.savefig(fig, bbox_inches='tight', format = 'png')
                    st.pyplot(grafico)

                    fig.seek(0)
                    fig_64 = base64.b64encode(fig.getvalue()).decode('utf-8')
                    graficos['grafico_iqt_der'] = f"<img src='data:image/png;base64,{fig_64}' width='300' height='180'/>"
                    
                    st.write(f"Fuerza Máxima: **{f_max['f_iqt_der']} N**")
                    st.write(f"Promedio Estimado: **{f_mean['f_iqt_der']} N**")

            if 'CC_DER' in name:
                with st.expander('Datos Cuadricipital Derecho'):
                    f_max["f_cc_der"] = data_max
                    f_mean["f_cc_der"] = data_mean                                
                    fig = io.BytesIO()

                    grafico = plt.figure(figsize=(10, 4))
                    
                    graficos['grafico_cc_der'] = plt.scatter(df['ID'], df['Fuerza'], color = '#F36F59')
                    plt.title('Fuerza Obtenida Cuadricipital Derecho [N]')
                    plt.xlabel('Puntos de Medición')
                    plt.ylabel('Fuerza Obtenida')
                    plt.savefig(fig, bbox_inches='tight', format = 'png')
                    st.pyplot(grafico)

                    fig.seek(0)
                    
                    fig_64 = base64.b64encode(fig.getvalue()).decode('utf-8')
                    graficos['grafico_cc_der']= f"<img src='data:image/png;base64,{fig_64}' width='300' height='180'/>" 
                    
                    st.write(f"Fuerza Máxima: **{f_max['f_cc_der']} N**")
                    st.write(f"Promedio Estimado: **{f_mean['f_cc_der']} N**")

            if 'GLUT_MEDIO_DER' in name:
                with st.expander('Datos Glúteo Medio Derecho'):
                    f_max["f_gm_der"] = data_max
                    f_mean["f_gm_der"] = data_mean                                
                    fig = io.BytesIO()

                    grafico = plt.figure(figsize=(10, 4))
                    
                    graficos['grafico_gm_der'] = plt.scatter(df['ID'], df['Fuerza'], color = '#F36F59')
                    plt.title('Fuerza Obtenida Glúteo Medio Derecho [N]')
                    plt.xlabel('Puntos de Medición')
                    plt.ylabel('Fuerza Obtenida')
                    plt.savefig(fig, bbox_inches='tight', format = 'png')
                    st.pyplot(grafico)
                    
                    fig_64 = base64.b64encode(fig.getvalue()).decode('utf-8')
                    fig.seek(0)          
                    graficos['grafico_gm_der'] = f"<img src='data:image/png;base64,{fig_64}' width='300' height='180'/>"     
                    
                    st.write(f"Fuerza Máxima: **{f_max['f_gm_der']} N**")
                    st.write(f"Promedio Estimado: **{f_mean['f_gm_der']} N**")                 
                
try:
    frel_der = round(f_mean['f_iqt_der']/f_mean['f_cc_der'], 2)
    
    frel_izq = round(f_mean['f_iqt_izq']/f_mean['f_cc_izq'], 2)    
        
except:
    pass
      

        # BARRA LATERAL

with st.sidebar:
    st.title('Evaluación del Paciente')
    st.write('---')
    st.subheader('Datos del Paciente')
    with st.expander('Ver datos del paciente'):
        npaciente = st.text_input('Nombre del Paciente')
        epaciente = st.text_input('Edad del Paciente')
        mpaciente = st.text_input('Mail del Paciente')
        fpaciente = st.date_input('Fecha de Evaluación del Paciente')
    st.write('---')
    st.subheader('Diagnóstico del Paciente')
    hallazgos = st.text_area('Hallazgos')
    recomendaciones = st.text_area('Recomendaciones al Paciente')
    st.write('---')



    datos_paciente = {
        "nombre_paciente" : npaciente,
        "edad_paciente" : epaciente,
        "fecha_paciente" : fpaciente.strftime("%d/%m/%Y"),
        "mail_paciente": mpaciente,
        "iqt_der" : f_mean['f_iqt_der'],
        "cc_der" : f_mean['f_cc_der'],
        "iqt_izq" : f_mean['f_iqt_izq'],
        "cc_izq" : f_mean['f_cc_izq'],
        "frel_der" : frel_der,
        "frel_izq" : frel_izq,
        "glut_medio_der" : f_mean['f_gm_der'],
        "glut_medio_izq" : f_mean['f_gm_izq'],
        "grafico_iqt_izq" : graficos['grafico_iqt_izq'],
        "grafico_iqt_der" : graficos['grafico_iqt_der'],
        "grafico_cc_izq" : graficos['grafico_cc_izq'],
        "grafico_cc_der" : graficos['grafico_cc_der'],
        "grafico_gm_izq" : graficos['grafico_gm_izq'],
        "grafico_gm_der" : graficos['grafico_gm_der'],
        "hallazgos" : hallazgos,
        "recomendaciones" : recomendaciones
        
    }
st.write('---')
st.subheader('Creación del Informe')
st.write('La plantilla se irá editando a medida que llenes los datos en la sección de la izquierda! Por ahora, los datos de la sección anterior ya están ingresados.')

env = Environment(loader = FileSystemLoader('./'))
template = env.get_template('template.html.jinja')
html_data = template.render(datos_paciente)
view = components.html(html_data,height=500, width=810, scrolling=True)

option = {
    'enable-local-file-access': '',
    'page-size': 'Letter',
    'encoding' : "UTF-8",
    'margin-top': '0.35in',
    'margin-left': '0.75in',
    'margin-bottom': '0.75in',
    'margin-right': '0.75in'
}

config = pdfkit.configuration(wkhtmltopdf="wkhtmltopdf.exe")

with open(f'informe_base.html', 'r+') as res_html:
    res_html.write(html_data)
    pdf = pdfkit.from_file('informe_base.html', output_path=False, options=option, configuration=config)

# pdf = pdfkit.from_string(html_data, output_path=False, configuration=config, options=option)


st.subheader('Si está todo listo, puedes descargar el informe a continuación.')
st.write('Apreta el botón para realizar tu descarga!')


di = st.download_button('Descargar Informe',
    data = pdf,
    file_name= f'Informe {npaciente}.pdf')









                






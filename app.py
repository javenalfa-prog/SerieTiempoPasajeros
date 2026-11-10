import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datos import cargar_datos
from modelos import MODELOS

# Paleta de colores de la app
AZUL_MARINO = "#13284B"
BLANCO_HUESO = "#F8F4E9"
ORO = "#B08D57"

# Configuración de la página
st.set_page_config(
    page_title="Pronóstico de Pasajeros de Avión",
    page_icon="✈️",
    layout="wide"
)

# Estilos personalizados (fondo blanco hueso, texto azul marino y dorado)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BLANCO_HUESO};
    }}
    html, body, p, label, span {{
        color: {AZUL_MARINO};
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {AZUL_MARINO} !important;
    }}
    [data-testid="stMetric"] {{
        background-color: rgba(176, 141, 87, 0.15);
        border: 1.5px solid {ORO};
        border-radius: 10px;
        padding: 14px;
    }}
    [data-testid="stMetricValue"] {{
        color: {AZUL_MARINO} !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {AZUL_MARINO} !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {AZUL_MARINO};
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        color: {ORO} !important;
        border-bottom-color: {ORO} !important;
    }}
    [data-testid="stAlert"] {{
        background-color: rgba(176, 141, 87, 0.15);
        color: {AZUL_MARINO};
        border: 1.5px solid {ORO};
        border-radius: 10px;
    }}
    [data-testid="stAlert"] p {{
        color: {AZUL_MARINO} !important;
    }}
    [data-testid="stPlotlyChart"] {{
        border: 2px solid {ORO};
        border-radius: 12px;
        background-color: #FFFFFF;
        padding: 8px;
    }}
    [data-testid="stDataFrame"] {{
        border: 1.5px solid {ORO};
        border-radius: 8px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


def estilo_grafico(fig, alto=430):
    """Aplica el fondo blanco hueso, la tipografía azul marino y la rejilla."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=AZUL_MARINO),
        title=dict(font=dict(color=AZUL_MARINO, size=18)),
        legend=dict(
            font=dict(color=AZUL_MARINO),
            bgcolor="rgba(248, 244, 233, 0.85)",
            bordercolor=ORO,
            borderwidth=1
        ),
        margin=dict(l=40, r=20, t=60, b=40),
        height=alto
    )
    fig.update_xaxes(color=AZUL_MARINO, gridcolor="rgba(19, 40, 75, 0.12)")
    fig.update_yaxes(color=AZUL_MARINO, gridcolor="rgba(19, 40, 75, 0.12)")
    return fig


# Cargar datos
df = cargar_datos()
df['Month'] = pd.to_datetime(df['Month'])
df = df.sort_values('Month')

# Título principal
st.title("¿Cuántos pasajeros tendremos el próximo año?")

# Indicadores superiores
df['Ano'] = df['Month'].dt.year
passengers_1949 = int(df[df['Ano'] == 1949]['Passengers'].sum())
passengers_1960 = int(df[df['Ano'] == 1960]['Passengers'].sum())
crecimiento = round(passengers_1960 / passengers_1949, 1)

col1, col2, col3 = st.columns(3)
col1.metric("Pasajeros en 1949 (Total)", f"{passengers_1949:,}")
col2.metric("Pasajeros en 1960 (Total)", f"{passengers_1960:,}")
col3.metric("Veces que creció", f"{crecimiento}x")

# Pestañas
pestana_historia, pestana_temporada, pestana_examen, pestana_pronostico = st.tabs([
    "1. La historia",
    "2. La temporada",
    "3. El examen",
    "4. El pronóstico"
])

# --- PESTAÑA 1: LA HISTORIA ---
with pestana_historia:
    st.subheader("Evolución mensual de pasajeros")
    fig_historia = px.line(
        df, x='Month', y='Passengers',
        labels={'Month': 'Mes', 'Passengers': 'Número de pasajeros'},
        title="Pasajeros de aerolínea a lo largo del tiempo",
        color_discrete_sequence=[ORO]
    )
    fig_historia.update_traces(line=dict(width=3))
    estilo_grafico(fig_historia)
    st.plotly_chart(fig_historia, width="stretch")

    st.info(
        "Este gráfico muestra cómo ha crecido la cantidad de pasajeros mes a mes desde 1949 hasta 1960. "
        "Se observa una tendencia clara al alza constante y un comportamiento repetitivo cada año. "
        "Para el negocio, esto significa que la demanda de vuelos aumenta año con año, requiriendo mayor capacidad de flota y personal."
    )

# --- PESTAÑA 2: LA TEMPORADA ---
with pestana_temporada:
    st.subheader("Comportamiento estacional por mes")

    meses_es = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
        7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    df['Mes_Num'] = df['Month'].dt.month

    promedio_por_mes = df.groupby('Mes_Num')['Passengers'].mean().reset_index()
    promedio_por_mes['Mes'] = promedio_por_mes['Mes_Num'].map(meses_es)
    promedio_por_mes = promedio_por_mes.sort_values('Mes_Num')

    media_general = promedio_por_mes['Passengers'].mean()

    fig_temporada = px.bar(
        promedio_por_mes, x='Mes', y='Passengers',
        text_auto='.0f',
        labels={'Mes': 'Mes del año', 'Passengers': 'Promedio de pasajeros'},
        title="Promedio de pasajeros por mes (Temporada alta y baja)",
        color_discrete_sequence=[ORO]
    )
    fig_temporada.add_hline(
        y=media_general, line_dash="dash", line_color=AZUL_MARINO,
        annotation_text="Promedio normal", annotation_position="bottom right"
    )
    estilo_grafico(fig_temporada)
    st.plotly_chart(fig_temporada, width="stretch")

    st.info(
        "Aquí se compara el promedio de pasajeros de cada mes frente al promedio general del año. "
        "Los meses de verano (como julio y agosto) superan ampliamente la línea media, marcando la temporada alta. "
        "Para el negocio, esto indica cuándo se deben planear campañas de marketing agresivas y tarifas especiales, así como prepararse para picos de operación."
    )

# --- PESTAÑA 3: EL EXAMEN ---
with pestana_examen:
    st.subheader("Evaluación de modelos con los últimos 24 meses")

    train = df.iloc[:-24].copy()
    test = df.iloc[-24:].copy()

    serie_train = pd.Series(
        train["Passengers"].values,
        index=pd.DatetimeIndex(train["Month"])
    ).asfreq("MS")

    with st.spinner("Calculando todos los modelos... esto puede tardar unos segundos."):
        predicciones = {}
        for nombre, funcion in MODELOS.items():
            try:
                pron = funcion(serie_train, 24)
                predicciones[nombre] = np.asarray(pron.values, dtype=float)
            except Exception as error:
                st.warning(f"El modelo {nombre} no pudo calcularse: {error}")

    # Tonos de dorado para distinguir cada modelo manteniendo el contraste
    tonos_oro = {
        "Copiar el año pasado": "#6E5330",
        "Suavizamiento exponencial": "#7D5F32",
        "Modelo de temporada (Holt-Winters)": "#8C6D3F",
        "SARIMA": "#A07C46",
        "Regresión lineal": "#C9A876",
        "Prophet": "#9C7A45",
    }

    fig_examen = go.Figure()
    fig_examen.add_trace(go.Scatter(
        x=train["Month"], y=train["Passengers"], name="Entrenamiento",
        line=dict(color="#C9A876", width=1.5)
    ))
    fig_examen.add_trace(go.Scatter(
        x=test["Month"], y=test["Passengers"], name="Real (Prueba)",
        line=dict(color=AZUL_MARINO, width=3)
    ))
    for nombre, valores in predicciones.items():
        fig_examen.add_trace(go.Scatter(
            x=test["Month"], y=valores, name=nombre,
            line=dict(color=tonos_oro.get(nombre, ORO), dash="dash", width=2)
        ))

    estilo_grafico(fig_examen, alto=470)
    fig_examen.update_layout(title="Comparativa de pronósticos vs Realidad (Últimos 24 meses)")
    st.plotly_chart(fig_examen, width="stretch")

    real = test["Passengers"].values
    errores = []
    for nombre, valores in predicciones.items():
        mape = np.mean(np.abs((real - valores) / real)) * 100
        errores.append({"Método": nombre, "Error promedio (%)": round(mape, 2)})

    df_errores = pd.DataFrame(errores).sort_values("Error promedio (%)").reset_index(drop=True)
    st.dataframe(df_errores, width="stretch", hide_index=True)

    ganador = df_errores.iloc[0]["Método"]
    error_ganador = df_errores.iloc[0]["Error promedio (%)"]

    st.success(f"El modelo ganador fue **{ganador}**, con un error promedio de {error_ganador}%.")

    st.info(
        f"En este examen simulamos pronosticar los últimos dos años sin haberlos visto antes y probamos varios métodos. "
        f"El que tuvo el error más bajo fue **{ganador}**, lo que indica que es el más confiable para este negocio. "
        "Menos error significa presupuestos más precisos y menos sorpresas en la operación."
    )

# --- PESTAÑA 4: EL PRONÓSTICO ---
with pestana_pronostico:
    st.subheader("Pronóstico para los 12 meses de 1961")

    modelo_elegido = st.selectbox(
        "Elige el modelo para pronosticar:",
        list(MODELOS.keys()),
        index=list(MODELOS.keys()).index("Modelo de temporada (Holt-Winters)")
    )

    serie_completa = pd.Series(
        df["Passengers"].values,
        index=pd.DatetimeIndex(df["Month"])
    ).asfreq("MS")

    with st.spinner(f"Entrenando {modelo_elegido} con todos los datos..."):
        pred_1961 = MODELOS[modelo_elegido](serie_completa, 12)

    fechas_1961 = pd.date_range(start="1961-01-01", periods=12, freq="MS")

    df_pronostico = pd.DataFrame({
        "Month": fechas_1961,
        "Passengers_Pred": np.asarray(pred_1961.values, dtype=float)
    })

    fig_pronostico = go.Figure()
    fig_pronostico.add_trace(go.Scatter(
        x=df["Month"], y=df["Passengers"], name="Histórico",
        line=dict(color="#8C6D3F", width=2.5)
    ))
    fig_pronostico.add_trace(go.Scatter(
        x=df_pronostico["Month"], y=df_pronostico["Passengers_Pred"],
        name=f"Pronóstico 1961 ({modelo_elegido})",
        line=dict(color=ORO, width=3, dash="dash")
    ))
    estilo_grafico(fig_pronostico, alto=470)
    fig_pronostico.update_layout(title="Histórico y Pronóstico de pasajeros para 1961")
    st.plotly_chart(fig_pronostico, width="stretch")

    df_tabla_pronostico = pd.DataFrame({
        "Mes": [meses_es[m] + " 1961" for m in range(1, 13)],
        "Pasajeros Esperados": [round(p) for p in df_pronostico["Passengers_Pred"]]
    })

    st.dataframe(df_tabla_pronostico, width="stretch", hide_index=True)

    st.info(
        f"Este gráfico y tabla presentan el pronóstico oficial para cada mes de 1961 usando el modelo **{modelo_elegido}** entrenado con toda la historia disponible. "
        "Se proyecta una continuación del crecimiento histórico manteniendo las altas y bajas estacionales. "
        "Para el negocio, esta información es vital para presupuestar ingresos, contratar personal de apoyo en temporada alta y negociar contratos con proveedores con anticipación."
    )

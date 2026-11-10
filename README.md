# ¿Cuántos pasajeros tendremos el próximo año?

App sencilla en **Streamlit** para pronosticar pasajeros mensuales de avión.

## Estructura

- `app.py`: aplicación principal (pestañas, gráficos e indicadores).
- `datos.py`: carga los datos desde internet y, si falla, desde `datos/airline-passengers.csv`.
- `modelos.py`: modelos de pronóstico (Copiar el año pasado, Suavizamiento exponencial, Holt-Winters, SARIMA, Regresión lineal y Prophet).
- `datos/airline-passengers.csv`: respaldo local de los datos.
- `.streamlit/config.toml`: tema de colores de la app.
- `requirements.txt`: librerías necesarias.

## Ejecutar en local

```bash
uv venv
uv pip install -r requirements.txt
uv run streamlit run app.py
```

En Windows también puedes hacer doble clic en `iniciar_app.bat`.

## Desplegar en Streamlit Community Cloud

1. Sube el proyecto a un repositorio de GitHub (incluye `datos/airline-passengers.csv`).
2. Entra a https://share.streamlit.io y conecta tu cuenta de GitHub.
3. Pulsa **New app** y elige:
   - Repositorio: el que acabas de subir.
   - Branch: `main`.
   - Main file path: `app.py`.
4. Pulsa **Deploy**. La primera vez puede tardar varios minutos porque instala Prophet.

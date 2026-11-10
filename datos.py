from pathlib import Path

import pandas as pd

URL_DATOS = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
RUTA_LOCAL = Path(__file__).parent / "datos" / "airline-passengers.csv"


def cargar_datos():
    try:
        df = pd.read_csv(URL_DATOS)
    except Exception:
        df = pd.read_csv(RUTA_LOCAL)

    df.columns = [c.strip() for c in df.columns]
    return df

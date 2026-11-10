import logging
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")
logging.getLogger("prophet").setLevel(logging.ERROR)
logging.getLogger("cmdstanpy").setLevel(logging.ERROR)


def _fechas_futuras(serie, pasos):
    return pd.date_range(start=serie.index[-1], periods=pasos + 1, freq="MS")[1:]


def predecir_copiar_ano(serie, pasos):
    valores = serie.values
    prediccion = [valores[len(serie) - 12 + (i % 12)] for i in range(pasos)]
    return pd.Series(prediccion, index=_fechas_futuras(serie, pasos))


def predecir_holt_winters(serie, pasos):
    modelo = ExponentialSmoothing(
        serie, trend="add", seasonal="mul", seasonal_periods=12
    ).fit()
    return pd.Series(modelo.forecast(pasos).values, index=_fechas_futuras(serie, pasos))


def predecir_suavizamiento(serie, pasos):
    modelo = ExponentialSmoothing(serie).fit()
    return pd.Series(modelo.forecast(pasos).values, index=_fechas_futuras(serie, pasos))


def predecir_sarima(serie, pasos):
    modelo = SARIMAX(
        serie,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False)
    pron = modelo.get_forecast(steps=pasos).predicted_mean
    return pd.Series(np.asarray(pron), index=_fechas_futuras(serie, pasos))


def predecir_regresion(serie, pasos):
    n = len(serie)
    t = np.arange(1, n + 1)
    meses = serie.index.month
    dummies = pd.get_dummies(meses, prefix="mes", drop_first=True).astype(float)
    X = np.column_stack([t, dummies.values])
    X = sm.add_constant(X)
    modelo = sm.OLS(serie.values, X).fit()

    t_fut = np.arange(n + 1, n + pasos + 1)
    fechas = _fechas_futuras(serie, pasos)
    dummies_fut = pd.get_dummies(fechas.month, prefix="mes", drop_first=True).astype(float)
    dummies_fut = dummies_fut.reindex(columns=dummies.columns, fill_value=0.0)
    X_fut = np.column_stack([t_fut, dummies_fut.values])
    X_fut = sm.add_constant(X_fut)
    prediccion = modelo.predict(X_fut)
    return pd.Series(prediccion, index=fechas)


def predecir_prophet(serie, pasos):
    from prophet import Prophet

    datos = pd.DataFrame({"ds": serie.index, "y": serie.values})
    modelo = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
    )
    modelo.fit(datos)
    futuro = modelo.make_future_dataframe(periods=pasos, freq="MS")
    pron = modelo.predict(futuro)
    pron = pron.iloc[-pasos:]
    return pd.Series(pron["yhat"].values, index=_fechas_futuras(serie, pasos))


MODELOS = {
    "Copiar el año pasado": predecir_copiar_ano,
    "Suavizamiento exponencial": predecir_suavizamiento,
    "Modelo de temporada (Holt-Winters)": predecir_holt_winters,
    "SARIMA": predecir_sarima,
    "Regresión lineal": predecir_regresion,
    "Prophet": predecir_prophet,
}

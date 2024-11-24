import pandas as pd
from utils.handleError import handle_error


def proces_data(data, label_encoders, scaler):

    df = pd.DataFrame([data])

    # Convertir variables categóricas a valores numéricos usando los LabelEncoders
    for column, le in label_encoders.items():
        if column in df:
            try:
                df[column] = le.transform(df[column])
            except ValueError as e:
                 raise handle_error(
                        status=400,
                        title=f"Error transformando la columna '{column}'",
                        detail=str(e),
                        instance="/predict"
                    )

    # Escalar los datos numéricos
    try:
        df_scaled = scaler.transform(df)
    except Exception as e:
        handle_error(
            status=500,
            title="Error en el escalado de datos",
            detail=str(e),
            instance="/predict"
        )

    return df_scaled
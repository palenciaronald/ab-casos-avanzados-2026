"""CreditSight — app de apoyo al analista de riesgo.

Carga `ejemplo/models/model.joblib` desde el repositorio (no consulta Databricks: no se ponen
credenciales en la nube). Ejecutar:  streamlit run ejemplo/app/streamlit_app.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# Permite importar `creditsight` sin instalarlo (el código vive en ejemplo/src)
EXAMPLE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE_DIR / "src"))

from creditsight.config import CLASSES, COST_MATRIX  # noqa: E402
from creditsight.inference.predict import InputValidationError, load_model, predict, required_columns  # noqa: E402

MODEL_PATH = EXAMPLE_DIR / "models" / "model.joblib"
SCHEMA_PATH = EXAMPLE_DIR / "models" / "input_schema.json"

st.set_page_config(page_title="CreditSight", page_icon="💳", layout="wide")

LABELS = {
    "Age": "Edad (años)",
    "Occupation": "Ocupación",
    "Annual_Income": "Ingreso anual",
    "Monthly_Inhand_Salary": "Sueldo mensual neto",
    "Num_Bank_Accounts": "Cuentas bancarias",
    "Num_Credit_Card": "Tarjetas de crédito",
    "Num_of_Loan": "Número de préstamos",
    "Interest_Rate": "Tasa de interés (%)",
    "Credit_Mix": "Mezcla de crédito (Bad / Standard / Good)",
    "Credit_History_Months": "Antigüedad crediticia (meses)",
    "Delay_from_due_date": "Días de retraso promedio en pagos",
    "Num_of_Delayed_Payment": "Pagos atrasados",
    "Payment_of_Min_Amount": "¿Paga solo el mínimo?",
    "Payment_Behaviour": "Comportamiento de pago",
    "Changed_Credit_Limit": "Cambio en el límite de crédito (%)",
    "Num_Credit_Inquiries": "Consultas de crédito",
    "Outstanding_Debt": "Deuda pendiente",
    "Credit_Utilization_Ratio": "Utilización del crédito (%)",
    "Total_EMI_per_month": "Cuotas mensuales (EMI)",
    "Amount_invested_monthly": "Monto invertido al mes",
    "Monthly_Balance": "Saldo mensual",
}
SECTIONS = {
    "Perfil": ["Age", "Occupation", "Annual_Income", "Monthly_Inhand_Salary"],
    "Productos de crédito": ["Num_Bank_Accounts", "Num_Credit_Card", "Num_of_Loan", "Interest_Rate", "Credit_Mix", "Credit_History_Months"],
    "Comportamiento de pago": ["Delay_from_due_date", "Num_of_Delayed_Payment", "Payment_of_Min_Amount", "Payment_Behaviour", "Changed_Credit_Limit", "Num_Credit_Inquiries"],
    "Deuda y flujo de caja": ["Outstanding_Debt", "Credit_Utilization_Ratio", "Total_EMI_per_month", "Amount_invested_monthly", "Monthly_Balance"],
}
UNKNOWN = "(no sé)"
INTEGER_FIELDS = {"Age", "Num_Bank_Accounts", "Num_Credit_Card", "Num_of_Loan", "Num_of_Delayed_Payment",
                  "Num_Credit_Inquiries", "Credit_History_Months", "Delay_from_due_date", "Interest_Rate"}


@st.cache_resource
def get_model():
    return load_model(MODEL_PATH)


@st.cache_data
def get_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def collect_inputs(schema: dict, defaults: dict) -> dict:
    """Dibuja el formulario y devuelve una fila de entrada (NaN donde el usuario marcó 'no sé')."""
    numeric, categorical = required_columns()
    row = {}
    for title, fields in SECTIONS.items():
        st.subheader(title)
        cols = st.columns(3)
        for i, field in enumerate(fields):
            with cols[i % 3]:
                label = LABELS.get(field, field)
                if field in categorical:
                    options = schema["categories"][field] + [UNKNOWN]
                    default = defaults.get(field, options[0])
                    choice = st.selectbox(label, options, index=options.index(default) if default in options else 0, key=field)
                    row[field] = np.nan if choice == UNKNOWN else choice
                    continue
                low, high = schema["observed_range"][field]
                default = float(defaults.get(field, schema["median"][field]))
                unknown = st.checkbox(f"No sé: {label}", key=f"unk_{field}", value=False)
                if unknown:
                    row[field] = np.nan
                    continue
                if field in INTEGER_FIELDS:
                    row[field] = st.number_input(label, min_value=int(low), max_value=int(high), value=int(round(default)), step=1, key=field)
                else:
                    row[field] = st.number_input(label, min_value=float(low), max_value=float(high), value=float(round(default, 2)), key=field)
    return row


def main():
    st.title("💳 CreditSight")
    st.caption("Apoyo a la decisión de límite de crédito. **No decide por sí solo: prioriza la revisión del analista de riesgo.**")

    if not MODEL_PATH.exists() or not SCHEMA_PATH.exists():
        st.error("Falta el modelo (`ejemplo/models/model.joblib`). Ejecuta el notebook `09_inferencia.ipynb` para generarlo.")
        st.stop()
    model, schema = get_model(), get_schema()

    examples = schema.get("examples", {})
    choice = st.radio("Empezar desde un perfil de ejemplo", ["(en blanco: valores típicos)"] + list(examples), horizontal=True)
    defaults = examples.get(choice, {}) if choice in examples else {}

    with st.form("cliente"):
        row = collect_inputs(schema, defaults)
        submitted = st.form_submit_button("Evaluar cliente", type="primary")

    if not submitted:
        st.info("Completa los datos del cliente y pulsa **Evaluar cliente**. Marca *No sé* en lo que no conozcas.")
        return

    try:
        output = predict(pd.DataFrame([row]), model=model, schema=schema)
        result, warnings = output.iloc[0], output.attrs.get("warnings", [])
    except InputValidationError as error:
        st.error(f"Revisa los datos: {error}")
        return

    colors = {"Good": "🟢", "Standard": "🟡", "Poor": "🔴"}
    left, right = st.columns([1, 1])
    with left:
        st.metric("Decisión sugerida", f"{colors[result['decision']]} {result['decision']}")
        st.caption(f"Clase más probable: **{result['most_likely']}** · costo esperado de esta decisión: **{result['expected_cost']:.2f}**")
        if result["needs_review"]:
            st.warning("**Revisión recomendada:** el modelo duda, o la decisión de menor costo difiere de la clase más probable.")
        else:
            st.success("El modelo está seguro: revisión estándar.")
        for message in warnings:
            st.warning(message)
    with right:
        st.write("**Probabilidad por clase**")
        st.bar_chart(pd.DataFrame({"probabilidad": [result[f"proba_{c}"] for c in CLASSES]}, index=CLASSES))

    with st.expander("¿Cómo se toma la decisión?"):
        st.markdown(
            "El modelo calcula la probabilidad de cada clase y luego elige la decisión de **menor costo esperado**, "
            "no la más probable: aprobar a un cliente `Poor` cuesta mucho más que rechazar a uno `Good`."
        )
        st.dataframe(pd.DataFrame(COST_MATRIX, index=[f"real {c}" for c in CLASSES], columns=[f"decide {c}" for c in CLASSES]))
    with st.expander("Uso responsable"):
        st.markdown(
            "- Esta herramienta **apoya** al analista; la decisión final es humana.\n"
            "- Entrenada con datos **sintéticos** de ejemplo: no usar con clientes reales sin una validación propia.\n"
            "- `Credit_Mix` se usa asumiendo que se conoce al momento de decidir.\n"
            "- Revisar con el equipo legal el uso de atributos como la edad antes de usarlo en producción."
        )


main()

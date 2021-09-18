import streamlit as st
import joblib
from helper import prepare_data, display_data


# Load model
@st.cache(allow_output_mutation=True)
def load_model():
    my_model = joblib.load('model.joblib')
    return my_model


model = load_model()

st.markdown("<h1 style='text-align: center; color: black;'>New York Taxi Fleet Allocations</h1>", unsafe_allow_html=True)

st.sidebar.header('Allocation Date')
dt = st.sidebar.date_input('Date')

st.sidebar.write("""### Click to allocate""")
alloc = st.sidebar.button('Allocate')

df, data = prepare_data(dt)

if alloc:
    pred = model.predict(data)
    orig, frac = display_data(df.copy(), pred)
    frac.index.name = None

    # st.markdown(f"<h3 style='text-align: center; color: black;'>Data Predictions for {dt}</h3>", unsafe_allow_html=True)
    # st.dataframe(orig, 2000, 200)

    st.markdown(f"<h3 style='text-align: center; color: black;'>Bar Chart Allocations for {dt}</h3>", unsafe_allow_html=True)
    st.bar_chart(frac)

    st.markdown(f"<h3 style='text-align: center; color: black;'>Data Allocations for {dt}</h3>", unsafe_allow_html=True)

    st.table(frac.style.highlight_min(axis=1))

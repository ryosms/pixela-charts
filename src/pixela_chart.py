from datetime import date, timedelta, datetime

import pandas as pd
import streamlit as st

import session_state
from pixela import Pixela

state = session_state.get_state()
st.sidebar.title("Pixela Chart")
username = st.sidebar.text_input("username")
token = st.sidebar.text_input("token", type="password")
auth_error = st.sidebar.empty()
if st.sidebar.button("Load graphs"):
    state.client = None
    state.graphs = None
    if not username or not token:
        auth_error.error("username or token is empty")
    else:
        state.client = Pixela(username, token)
        state.graphs = state.client.load_graph_definitions()
        if not state.graphs:
            auth_error.error(state.client.last_error())

if state.graphs:
    id_list = list(state.graphs.keys())
    id_list.insert(0, "")
    selected_graph_id = st.sidebar.selectbox('select graph', id_list)
    if selected_graph_id:
        selected = state.graphs[selected_graph_id]
        st.title(f"{selected['name']}")
        id_text, unit_text, _ = st.beta_columns((1, 1, 2))
        id_text.write(f"id: {selected['id']}")
        unit_text.write(f"unit: {selected['unit']}")

        from_input, to_input = st.beta_columns(2)
        from_date = from_input.date_input("From", date.today() - timedelta(days=7))
        to_date = to_input.date_input("To")

        state.pixels = state.client.load_pixels(selected_graph_id, from_date, to_date)
        if state.pixels:
            index = []
            chart_data = {'quantity': []}
            for p in state.pixels:
                index.append(datetime.strptime(p['date'], '%Y%m%d'))
                chart_data['quantity'].append(float(p['quantity']))
            df = pd.DataFrame(chart_data, index=index)
            st.line_chart(df)
        else:
            st.error("No data")

        if state.selected_graph_id != selected_graph_id:
            state.selected_graph_id = selected_graph_id

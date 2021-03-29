import json
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
        ret = state.client.load_graph_definitions()
        state.graphs = ret[0]
        if not state.graphs:
            auth_error.error(ret[1])

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

        ret = state.client.load_pixels(selected_graph_id, from_date, to_date)
        state.pixels = ret[0]
        if not state.pixels:
            st.error(ret[1] if ret[1] else "No Data")
        else:
            query_area, chart_area = st.beta_columns((1, 3))
            pixel: dict = state.pixels[-1]
            optionalDataHeaders = []
            selectedOptionalData = {}
            if "optionalData" in pixel.keys():
                optionalData = json.loads(pixel["optionalData"])
                optionalDataHeaders = list(optionalData.keys())

            chart_data = {'quantity': []}
            show_quantity = query_area.checkbox("quantity", True)
            query_area.write("optionalData:")
            for k in optionalDataHeaders:
                selectedOptionalData[k] = query_area.checkbox(k, False)
                chart_data[k] = []

            index = []
            for p in state.pixels:
                index.append(datetime.strptime(p['date'], '%Y%m%d'))
                chart_data['quantity'].append(float(p['quantity']))
                if "optionalData" in p.keys():
                    optionalData = json.loads(p["optionalData"])
                    for k in optionalDataHeaders:
                        if k in optionalData.keys():
                            chart_data[k].append(float(optionalData[k]))

            df = pd.DataFrame(chart_data, index=index)
            if not show_quantity:
                df = df.drop("quantity", axis=1)
            for k, v in selectedOptionalData.items():
                if not v:
                    df = df.drop(k, axis=1)

            if len(df.columns) > 0:
                chart_area.line_chart(df)

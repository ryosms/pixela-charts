from datetime import date, timedelta

import streamlit as st

import session_state
from pixela import Pixela

state = session_state.get_state()
st.sidebar.title("Pixela Chart")
username = st.sidebar.text_input("username")
token = st.sidebar.text_input("token", type="password")

if st.sidebar.button("Load graphs"):
    if not username or not token:
        st.sidebar.error("username or token is empty")
    else:
        state.client = Pixela(username, token)
        state.graphs = state.client.load_graph_definitions()
        if not state.graphs:
            st.sidebar.error(state.client.last_error())

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
        # st.write(selected)

        from_input, to_input = st.beta_columns(2)
        from_date = from_input.date_input("From", date.today() - timedelta(days=7))
        to_date = to_input.date_input("To")

        if state.selected_graph_id != selected_graph_id:
            state.selected_graph_id = selected_graph_id

import json
from datetime import date, timedelta, datetime
from typing import Optional, Tuple

import pandas as pd
import streamlit as st

import session_state
from pixela import Pixela

st.set_page_config(page_title='Pixela Chart', layout='wide')

state = session_state.get_state()
st.sidebar.title("Pixela Chart")
username = st.sidebar.text_input("username")
token = st.sidebar.text_input("token", type="password")
auth_error = st.sidebar.empty()


@st.cache
def load_graph_list(u: str, t: str) -> Tuple[Optional[Pixela], Optional[dict], Optional[str]]:
    if not u or not t:
        return None, None, "username or token is empty"
    client = Pixela(u, t)
    return (client,) + client.load_graph_definitions()


if st.sidebar.button("Load graphs"):
    state.client, state.graphs, err_msg = load_graph_list(username, token)
    if err_msg:
        auth_error.error(err_msg)

if not state.graphs:
    st.stop()


@st.cache
def create_graph_id_list(graphs: dict) -> list:
    id_list = list(graphs.keys())
    id_list.insert(0, "")
    return id_list


ids = create_graph_id_list(state.graphs)
selected_id = st.sidebar.selectbox("Select Graph", ids)
if not selected_id:
    st.stop()

selected_graph = state.graphs[selected_id]
st.title(f"{selected_graph['name']}")

id_label, unit_label, _ = st.beta_columns((1, 1, 2))
id_label.write(f"id: {selected_graph['id']}")
unit_label.write(f"unit: {selected_graph['unit']}")

from_date_input, to_date_input = st.beta_columns(2)
from_date = from_date_input.date_input("From", date.today() - timedelta(days=7))
to_date = to_date_input.date_input("To", date.today())


@st.cache
def load_pixels(client: Pixela, graph_id: str, from_: date, to: date) -> Tuple[list, str]:
    return client.load_pixels(graph_id, from_, to)


state.pixels, err_msg = load_pixels(state.client, selected_id, from_date, to_date)
if not state.pixels:
    st.error(err_msg if err_msg else "No Data")
    st.stop()


@st.cache
def make_optional_dat_headers(pixel: dict) -> list:
    if "optionalData" in pixel.keys():
        od = json.loads(pixel["optionalData"])
        return list(od.keys())
    return []


optional_headers = make_optional_dat_headers(state.pixels[-1])
selected_optional_data = {}

query_area, chart_area = st.beta_columns((1, 3))

show_quantity = query_area.checkbox("quantity", True)
query_area.write("optionalData:")
for k in optional_headers:
    selected_optional_data[k] = query_area.checkbox(k, False)


def parse_data(q: str) -> Optional[float]:
    try:
        return float(q)
    except ValueError:
        return None


@st.cache
def make_chart_data(pixels: list, headers: list) -> pd.DataFrame:
    index = []
    data = {"quantity": []}
    for h in headers:
        data[h] = []
    for p in pixels:
        index.append(datetime.strptime(p["date"], "%Y%m%d"))
        data["quantity"].append(parse_data(p["quantity"]))
        if "optionalData" in p.keys():
            od = json.loads(p["optionalData"])
            for key in headers:
                if key in od.keys():
                    data[key].append(parse_data(od[key]))
        else:
            for key in headers:
                data[key].append(None)
    return pd.DataFrame(data, index=index)


df = make_chart_data(state.pixels, optional_headers)
if not show_quantity:
    df = df.drop("quantity", axis=1)
for k, selected in selected_optional_data.items():
    if not selected:
        df = df.drop(k, axis=1)

if len(df.columns) > 0:
    chart_area.line_chart(df)

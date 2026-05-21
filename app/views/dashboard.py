import numpy as np
import pandas as pd
import streamlit as st

from app.auth.authenticator import require_login
from app.components.chat import render_chat_panel
from app.components.footer import render_sidebar_footer
from app.components.layout import inject_app_css
from app.components.sidebar_filters import render_filters


def render() -> None:
    inject_app_css()

    # Auth guard
    name, username = require_login()

    # Sidebar
    render_filters()
    render_sidebar_footer()

    # Main area
    st.title("Dashboard")

    # KPI Tiles
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Users", "1,024", "12%")
    col2.metric("Active Projects", "42", "-5%")
    col3.metric("Revenue", "$12,400", "8%")

    st.divider()

    # Chart and Chat
    main_col, chat_col = st.columns([2, 1])

    with main_col:
        st.subheader("Activity")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        st.line_chart(chart_data)

    with chat_col:
        with st.container(border=True):
            render_chat_panel()


render()

import streamlit as st

from app.services.agent_service import stream_agent_response


def render_chat_panel() -> None:
    st.markdown("### Agent Chat")

    # Initialize history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Render history
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask the agent..."):
        # Append user message
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call agent service and stream response
        with st.chat_message("assistant"):
            response_generator = stream_agent_response(
                prompt, st.session_state["chat_history"]
            )
            full_response = st.write_stream(response_generator)

        st.session_state["chat_history"].append(
            {"role": "assistant", "content": full_response}
        )

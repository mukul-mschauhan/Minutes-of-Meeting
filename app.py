import streamlit as st
from generator import MoMGenerator
from datetime import datetime
import pandas as pd

def main():
    st.title("📝 Minutes of Meeting Generator")
    with st.sidebar:
        api_key = st.text_input("Gemini API Key", type="password")
        if not api_key:
            st.warning("Please enter your Gemini API key to proceed")
            st.stop()

    mom_gen = MoMGenerator(api_key)
    uploaded_files = st.file_uploader("Upload meeting files", type=['txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)

    if uploaded_files and st.button("🔄 Generate MoM"):
        combined_text = ""
        for file in uploaded_files:
            combined_text += f"\n\n--- {file.name} ---\n" + mom_gen.extract_text_from_file(file)
        mom_data = mom_gen.process_text_with_gemini(combined_text)
        st.json(mom_data)
        excel_buffer = mom_gen.create_excel_file(mom_data)
        st.download_button("📥 Download Excel", excel_buffer.getvalue(), file_name=f"MoM_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")

if __name__ == "__main__":
    main()
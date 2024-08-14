import streamlit as st
import fitz  # PyMuPDF
import re
import time

def extract_answer(pdf_path, query, time_limit=3):
    start_time = time.time()
    
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Iterate through the pages and extract text
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")
        
        # Use regex to find the answer to the query
        pattern = re.compile(rf"\b{re.escape(query)}\b.*", re.IGNORECASE)
        match = pattern.search(text)
        
        if match:
            # Stop the search and return the result if found within the time limit
            if time.time() - start_time > time_limit:
                return "Time limit exceeded"
            return match.group(0)
    
    return "Answer not found within the document"

# Streamlit Chatbot Interface
def main():
    st.title("PDF Knowledge Miner Chatbot")
    
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    query = st.text_input("Enter your query:")
    time_limit = st.slider("Set time limit (seconds)", 1, 10, 3)
    
    if st.button("Get Answer"):
        if uploaded_file and query:
            with open("temp_pdf.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            answer = extract_answer("temp_pdf.pdf", query, time_limit)
            st.write(f"Answer: {answer}")
        else:
            st.write("Please upload a PDF file and enter a query.")

if __name__ == "__main__":
    main()

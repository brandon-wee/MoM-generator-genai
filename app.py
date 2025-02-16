import streamlit as st
from models import MeetingOfMinutesLLM, SpamDetectorLLM
from outputs import MarkdownOutput, DOCXOutput, PDFOutput
from datetime import datetime
import json
import os

llm = MeetingOfMinutesLLM()
markdown_output = MarkdownOutput()
docx_output = DOCXOutput()
pdf_output = PDFOutput()
spam_detector = SpamDetectorLLM()

output_folder = "./output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

md_output_folder = "./output/md"
if not os.path.exists(md_output_folder):
    os.makedirs(md_output_folder)

docx_output_folder = "./output/docx"
if not os.path.exists(docx_output_folder):
    os.makedirs(docx_output_folder)

pdf_output_folder = "./output/pdf"
if not os.path.exists(pdf_output_folder):
    os.makedirs(pdf_output_folder)


st.set_page_config(
    page_title="Meeting of Minutes Generator",  
    page_icon="📝"  
)

st.title("Meeting of Minutes Generator")
output_format = st.selectbox("Select your output", ["Markdown", "DOCX", "PDF"])
transcript = st.text_area("Insert your transcript")


if st.button("Submit"):
    if transcript.strip() == "":
        st.warning("Please enter a transcript!")
    elif json.loads(spam_detector.detect_spam(transcript))["spam"]:
        st.warning("The transcript is invalid! Please enter a valid transcript.")
    else:
        try:
            template = open("./templates/sample_template.md", "r").read()
            minutes_content = json.loads(llm.generate_minutes(transcript))
            print(type(minutes_content))
            file_name = f"meeting_minutes_{hash(datetime.now().time()) % 10000007}"
            # Process the transcript and prepare file for download
            if output_format == "Markdown":
                # Generate Markdown content
                file_name = f"{md_output_folder}/{file_name}.md"
                markdown_output.generate_markdown_output(template, minutes_content, file_name)
                data = open(file_name, "r").read()
                mime = "text/markdown"

            elif output_format == "DOCX":
                # Generate DOCX file using python-docx
                file_name = f"{docx_output_folder}/{file_name}.docx"
                docx_output.generate_docx_output(template, minutes_content, file_name)
                data = open(file_name, "rb").read()
                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

            elif output_format == "PDF":
                # Generate PDF file using fpdf
                docx_file_name = f"{docx_output_folder}/{file_name}.docx"
                file_name = f"{pdf_output_folder}/{file_name}.pdf"
                pdf_output.generate_pdf_output(template, minutes_content, file_name, docx_file_name)
                data = open(file_name, "rb").read()
                mime = "application/pdf"

            # 5. File download button
            st.download_button(
                label="Download File",
                data=data,
                file_name=file_name,
                mime=mime,
            )
        except:
            st.warning("An error occurred while processing the transcript. Please try again. If the problem persists, contact the administrator.")
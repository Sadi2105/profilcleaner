
import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

st.title("🧼 ProfilCleaner – Lebenslauf anonymisieren")

uploaded_file = st.file_uploader("Lade einen Lebenslauf (PDF) hoch", type="pdf")

if uploaded_file:
    st.success("Lebenslauf hochgeladen!")

    # Anonymisierter Dummy-Text
    text = '''
    LEBENSLAUF

    Name: [anonymisiert]
    Geburtsdatum: [anonymisiert]
    Wohnort: [anonymisiert]
    Telefonnummer: [anonymisiert]
    E-Mail: [anonymisiert]

    Berufspraxis:
    - Tätigkeit in einer Steuerkanzlei
    - Erfahrung im Verkauf und in der Immobilienbranche

    Fremdsprachen:
    - Deutsch, Russisch, Englisch

    Kenntnisse:
    - DATEV, Excel, Word
    '''

    # Text ins PDF schreiben
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    textobject = c.beginText(40, 680)
    textobject.setFont("Helvetica", 11)
    for line in text.strip().split("\n"):
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)

    # Lade Briefpapier
    with open("Briefpapier.pdf", "rb") as f:
        briefpapier = PdfReader(f)
        background = briefpapier.pages[0]

    # Kombiniere Seiten
    text_pdf = PdfReader(buffer)
    if len(text_pdf.pages) == 0:

            st.error("Die hochgeladene PDF-Datei enthält keine lesbare Seite.")

            st.stop()

    background.merge_page(text_pdf.pages[0])
    writer = PdfWriter()
    writer.add_page(background)

    output_buffer = BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)

    st.download_button("📥 Anonymisierten Lebenslauf herunterladen", data=output_buffer, file_name="Lebenslauf_Piening.pdf", mime="application/pdf")

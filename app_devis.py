import streamlit as st
from fpdf import FPDF

# Fonction pour générer le PDF
def generer_pdf(nom_entreprise, nom_client, prestation, quantite, prix_unitaire, remise_pourcent, total_ht, tva, total_ttc):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # En-tête / Titre
    pdf.set_font("Helvetica", 'B', 18)
    pdf.cell(0, 10, f"DEVIS - {nom_entreprise}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    
    # Informations Client
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"Client : {nom_client}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Prestation : {prestation}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # En-tête du Tableau
    pdf.set_font("Helvetica", 'B', 10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(80, 8, "Description", border=1, fill=True)
    pdf.cell(25, 8, "Quantité", border=1, align='C', fill=True)
    pdf.cell(40, 8, "Prix Unitaire HT", border=1, align='R', fill=True)
    pdf.cell(35, 8, "Total HT", border=1, align='R', fill=True, new_x="LMARGIN", new_y="NEXT")
    
    # Ligne du Tableau
    pdf.set_font("Helvetica", size=10)
    total_brut = quantite * prix_unitaire
    pdf.cell(80, 8, prestation[:35], border=1)
    pdf.cell(25, 8, str(quantite), border=1, align='C')
    pdf.cell(40, 8, f"{prix_unitaire:.2f} EUR", border=1, align='R')
    pdf.cell(35, 8, f"{total_brut:.2f} EUR", border=1, align='R', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Récapitulatif
    pdf.cell(110)
    pdf.cell(35, 7, "Remise :", border=0)
    pdf.cell(35, 7, f"-{remise_pourcent:.1f} %", border=0, align='R', new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(110)
    pdf.cell(35, 7, "Total HT :", border=0)
    pdf.cell(35, 7, f"{total_ht:.2f} EUR", border=0, align='R', new_x="LMARGIN", new_y="NEXT")
    
    pdf.cell(110)
    pdf.cell(35, 7, "TVA (20%) :", border=0)
    pdf.cell(35, 7, f"{tva:.2f} EUR", border=0, align='R', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Helvetica", 'B', 11)
    pdf.cell(110)
    pdf.cell(35, 8, "TOTAL TTC :", border=0)
    pdf.cell(35, 8, f"{total_ttc:.2f} EUR", border=0, align='R', new_x="LMARGIN", new_y="NEXT")
    
    return bytes(pdf.output())

# --- Interface Web Streamlit ---
st.title("⚡ Générateur de Devis Express")
st.subheader("Solution d'automatisation pour PME / Artisans")

with st.form("form_devis"):
    nom_entreprise = st.text_input("Nom de votre entreprise", "Menuiserie Dupond & Fils")
    nom_client = st.text_input("Nom du client", "Mme. Laurent")
    prestation = st.text_input("Prestation réalisée", "Remplacement de 4 fenêtres")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        quantite = st.number_input("Quantité", min_value=1, value=4)
    with col2:
        prix_unitaire = st.number_input("Prix unitaire HT (€)", min_value=0.0, value=350.0)
    with col3:
        remise_pourcent = st.number_input("Remise (%)", min_value=0.0, max_value=100.0, value=5.0)

    bouton_valider = st.form_submit_button("Générer le devis")

if bouton_valider:
    total_brut_ht = prix_unitaire * quantite
    montant_remise = total_brut_ht * (remise_pourcent / 100)
    total_ht = total_brut_ht - montant_remise
    tva = total_ht * 0.20
    total_ttc = total_ht + tva

    st.success("✅ Devis calculé avec succès !")
    st.metric(label="TOTAL TTC À PAYER", value=f"{total_ttc:.2f} €")
    
    # Génération du PDF
    pdf_data = generer_pdf(nom_entreprise, nom_client, prestation, quantite, prix_unitaire, remise_pourcent, total_ht, tva, total_ttc)
    
    # Bouton de téléchargement
    st.download_button(
        label="📄 Télécharger le Devis en PDF",
        data=pdf_data,
        file_name=f"Devis_{nom_client.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
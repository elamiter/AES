import streamlit as st
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import openai
from PIL import Image
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---------------- SETUP ----------------
st.set_page_config(page_title="KI-Einführung Simulation", layout="wide")

# ---------------- LOGO ----------------
logo = Image.open("logo.png")
st.image(logo, use_container_width=True)

st.title("🚀 Strategische KI-Einführung – Simulation")

# ---------------- ENV ----------------
print("Lade .env ...")
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
print(f"EMAIL_PASSWORD geladen: {'JA' if EMAIL_PASSWORD else 'NEIN'}")

openai.api_key = OPENAI_API_KEY
EMAIL_ADDRESS = "8da511002@smtp-brevo.com"

# ---------------- MAIL ----------------
def send_mail(subject, body, to_address):
    print(f"Versende an: {to_address}")
    print(f"Benutze Login: {EMAIL_ADDRESS}")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = "arjang.farashzadeh@digitalnewx.com"
    msg["To"] = to_address
    html_part = MIMEText(body.replace("\n", "<br>"), "html")
    msg.attach(html_part)

    with smtplib.SMTP("smtp-relay.brevo.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("✅ SMTP-Login erfolgreich")
        smtp.send_message(msg)
        print("✅ Mail erfolgreich gesendet")

# ---------------- ANMELDUNG ----------------
st.header("1. Anmeldung")
with st.form("user_form"):
    first_name = st.text_input("Vorname")
    last_name = st.text_input("Nachname")
    email = st.text_input("E-Mail-Adresse")
    role = st.text_input("Rolle im Unternehmen (z. B. CEO, CTO, HR, etc.)")
    submitted = st.form_submit_button("Absenden")

if submitted:
    st.session_state.angemeldet = True
    st.success("Anmeldung gespeichert. Viel Erfolg!")
    try:
        mail_text = f"""
Neue Anmeldung für die KI-Simulation:

Vorname: {first_name}
Nachname: {last_name}
E-Mail: {email}
Rolle: {role}
"""
        send_mail("Neue KI-Simulationsanmeldung", mail_text, EMAIL_ADDRESS)
        send_mail("Ihre Anmeldung zur KI-Simulation", f"Vielen Dank für Ihre Anmeldung, {first_name}!\n\nWir haben Ihre Daten erhalten.", "arjang.farashzadeh@digitalnewx.com")
    except Exception as e:
        st.warning(f"Anmeldung gespeichert, aber Mailversand fehlgeschlagen: {e}")

# ---------------- TESTS ----------------
class TestMailFunction(unittest.TestCase):
    def test_mail_format(self):
        subject = "Testbetreff"
        body = "Dies ist\nein Test mit Zeilenumbruch."
        to_address = "test@domain.de"

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = "arjang.farashzadeh@digitalnewx.com"
        msg["To"] = to_address
        html_part = MIMEText(body.replace("\n", "<br>"), "html")
        msg.attach(html_part)

        self.assertEqual(msg["Subject"], subject)
        self.assertEqual(msg["From"], "arjang.farashzadeh@digitalnewx.com")
        self.assertEqual(msg["To"], to_address)
        self.assertIn("<br>", html_part.get_payload())

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

# ---------------- AUFGABE ----------------

st.header("2. Aufgabe")
aufgabenstellung = """
**Aufgabe des Kandidaten:**
1. PoC-Aufsetzung: Definieren Sie, wie Sie den ersten KI-Anwendungsfall auswählen und technisch realisieren, sodass binnen weniger Wochen ein erster Prototyp entsteht.
2. Quick Wins sichtbar machen: Welche Maßnahmen sind vorgesehen, damit der PoC intern kommuniziert und als Erfolg wahrgenommen wird?
3. Vorbereitung auf Skalierung: Welche Hebel müssen Sie bereits in dieser kurzen „Turbo“-Phase ansetzen, um sich auf Roll-out und tiefere Prozessintegration vorzubereiten?

Ziel: Zeigen Sie, wie kurzfristige Erfolgserlebnisse und eine langfristige KI-Basis geschaffen werden.
"""
st.markdown(aufgabenstellung)

st.header("3. Ihre Antwort")
antwort = st.text_area("Tragen Sie hier Ihre Antwort ein:", height=300)

# Session Flag, ob die Anmeldung erfolgt ist
if 'angemeldet' not in st.session_state:
    st.session_state.angemeldet = False

if st.button("Antwort einreichen & analysieren"):
    if not st.session_state.angemeldet:
        st.warning("Bitte melden Sie sich zuerst an und klicken Sie auf 'Absenden', bevor Sie fortfahren.")
    elif not antwort:
        st.info("Bitte geben Sie zuerst Ihre Maßnahmen ein.")
    else:
    with st.spinner("Analysiere Antwort mit GPT-4..."):
        prompt_bewertung = f"""
Du bist ein Evaluator für KI-Strategie-Simulationen in Unternehmen. Vergleiche die folgende Antwort mit dem Erwartungshorizont in drei Dimensionen:

**Antwort des Kandidaten:**
{antwort}

**Erwartungshorizont:**
Dimension 1 – Werte: Nutzenargumentation, Umgang mit Unsicherheit
Dimension 2 – Wissen: Reifegrad, Know-how
Dimension 3 – Kultur: Haltung, Offenheit

Bewerte jede Dimension mit kurzer Begründung. Gib am Ende eine Gesamteinschätzung (kurz) für den strategischen Reifegrad.
"""
        response1 = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Du bist ein strenger, aber fairer Evaluator für strategische Entscheidungsprozesse."},
                {"role": "user", "content": prompt_bewertung}
            ],
            temperature=0.7
        )
        beurteilung = response1.choices[0].message.content
        st.subheader("🧠 GPT-Bewertung:")
        st.markdown(beurteilung)

        # Zweiter GPT-Call: Auswirkungen auf XANDU
        prompt_xandu = f"""
Nutze folgende Beschreibung von Maßnahmen und Strategien:

{antwort}

Wende diese auf die Firma XANDU an. Erstelle eine kurze tabellarische Übersicht zu den erwarteten Auswirkungen innerhalb der ersten vier Wochen.

**Eckdaten von XANDU:**
- Jahresumsatz: 20 Mio €
- EBIT-Marge: ca. 10%
- Liefertermintreue: < 95%
- Ausschussquote: > 2%
- Personalfluktuation: < 8%
- Kundenzufriedenheit: NPS > +40
- 120 Mitarbeitende, Produktionsbetrieb in Deutschland
- Kernbereiche: GF, Produktion, Einkauf, Vertrieb, F&E, HR, Controlling, IT
- Größte Herausforderung: Veraltete IT-Systeme, Systemwildwuchs, steigender Wettbewerbsdruck durch KI
"""
        response2 = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Du bist ein Business-Analyst für KI-Transformationen in mittelständischen Unternehmen."},
                {"role": "user", "content": prompt_xandu}
            ],
            temperature=0.7
        )
        auswirkungen = response2.choices[0].message.content
        st.markdown("**Ihre Maßnahmen und Strategien hätten auf die XANDU GmbH folgende Auswirkungen:**")
        st.subheader("🏭 Auswirkungen auf XANDU GmbH (erste 4 Wochen):")
        st.markdown(auswirkungen)
st.subheader("🏭 Auswirkungen auf XANDU GmbH (erste 4 Wochen):")
        st.markdown(auswirkungen)


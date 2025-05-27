import streamlit as st
import smtplib
from email.mime.text import MIMEText
import os
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

st.title("🚀 DigitalNewX | Transformation-Sandbox")

# ---------------- ENV ----------------

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
EMAIL_ADDRESS = st.secrets["EMAIL_ADDRESS"]

openai.api_key = OPENAI_API_KEY


# ---------------- MAIL ----------------
def send_mail(subject, body, to_address):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = "arjang.farashzadeh@digitalnewx.com"
    msg["To"] = to_address
    html_part = MIMEText(body.replace("\n", "<br>"), "html")
    msg.attach(html_part)

    with smtplib.SMTP("smtp-relay.brevo.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        

# ---------------- ANMELDUNG ----------------
st.header("Anmeldung")
with st.form("user_form"):
    first_name = st.text_input("Vorname")
    last_name = st.text_input("Nachname")
    email = st.text_input("E-Mail-Adresse")
    role = st.text_input("Rolle im Unternehmen (z.B. CEO, CTO, HR, etc.)")
    submitted = st.form_submit_button("Absenden")

if submitted:
    st.success("Anmeldung gespeichert. Viel Erfolg!")
    try:
        mail_text = f"""
Neue Anmeldung für die KI-Simulation:

Vorname: {first_name}
Nachname: {last_name}
E-Mail: {email}
Rolle: {role}
"""
        send_mail("Neue KI-Simulationsanmeldung", mail_text, 'pascal.rudolf@digitalnewx.com')
    except Exception as e:
        st.warning(f"Anmeldung gespeichert, aber Mailversand fehlgeschlagen: {e}")


# ---------------- AUFGABE ----------------

st.header("Aufgabe")
aufgabenstellung = """
**Aufgabe des Kandidaten:**
1. PoC-Aufsetzung: Definieren Sie, wie Sie den ersten KI-Anwendungsfall auswählen und technisch realisieren, sodass binnen weniger Wochen ein erster Prototyp entsteht.
2. Quick Wins sichtbar machen: Welche Maßnahmen sind vorgesehen, damit der PoC intern kommuniziert und als Erfolg wahrgenommen wird?
3. Vorbereitung auf Skalierung: Welche Hebel müssen Sie bereits in dieser kurzen „Turbo“-Phase ansetzen, um sich auf Roll-out und tiefere Prozessintegration vorzubereiten?

Ziel: Zeigen Sie, wie kurzfristige Erfolgserlebnisse und eine langfristige KI-Basis geschaffen werden.
"""
st.markdown(aufgabenstellung)

st.header("Ihre Antwort")
antwort = st.text_area("Tragen Sie hier Ihre Antwort ein:", height=300)

if st.button("Antwort einreichen & analysieren") and antwort:
    with st.spinner("Analysiere Antwort ..."):
        prompt_bewertung = f"""
Du bist ein Evaluator für KI-Strategie-Simulationen in Unternehmen. Vergleiche die folgende Antwort mit dem Erwartungshorizont in drei Dimensionen:

**Antwort des Kandidaten:**
{antwort}

**Erwartungshorizont:**
Dimension: Werte (Wirtschaftlichkeit & Umsetzung)
Erwartung: Die Teilnehmenden erkennen, dass in dieser frühen Phase häufig keine klaren Business-Cases vorliegen und es Skepsis bei Budgetfreigaben gibt.
Was eine gute Lösung zeigt:
Ein methodisches Vorgehen, wie erste Argumente für Nutzen und ROI geliefert werden können (z.B. Quick-Win-Ansätze, erste grobe Wirtschaftlichkeitsbetrachtungen).
Überlegungen dazu, wie Unsicherheit und Widerstand gegen erste KI-Investitionen reduziert werden können (z.B. Pilot-Budget, Kommunikationsplan zum Kosten-Nutzen-Verhältnis).

Dimension: Wissen (Reifegrad & Know-how)
Erwartung: Die Teilnehmenden berücksichtigen, dass das Unternehmen geringes Verständnis für KI haben könnte und dass Daten (bzw. deren Qualität und Struktur) am Anfang oft unzureichend sind.
Was eine gute Lösung zeigt:
Erste Ideen, wie das Unternehmen trotz mangelnder Erfahrung einen PoC oder ein KI-Konzept anstoßen kann (z.B. externe Beratung, interne Taskforce, Weiterbildung).
Ansätze, wie man den Data-Reifegrad Schritt für Schritt steigert (z.B. erste Bestandsaufnahme der vorhandenen Datenquellen).

Dimension: Kultur (Haltung & Kultur)
Erwartung: In der „Inspirieren“-Phase herrscht oft eine vorsichtige Grundhaltung gegenüber Neuerungen, es gibt keine etablierten KI-Befürworter und Skepsis kann hoch sein.
Was eine gute Lösung zeigt:
Maßnahmen, wie erste KI-Euphorie oder zumindest Offenheit geschaffen wird (z.B. gemeinsamer Kick-off, Stakeholder-Workshops).
Überlegungen, wie man den Kulturwandel unterstützt (z.B. Vorbilder im Management identifizieren, die hinter dem KI-Thema stehen) und den typischen Ängsten begegnet.

Bewerte (Überhauptnicht erfüllt, Teilweise erfüllt, Erweitert erfüllt, ganz Erfüllt) jede Dimension mit kurzer Begründung. Gib am Ende eine Gesamteinschätzung (kurz) für den strategischen Reifegrad.


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
        st.subheader("🧠 Bewertung:")
        st.markdown(beurteilung)

        # Zweiter GPT-Call: Auswirkungen auf XANDU
        prompt_xandu = f"""
Nutze folgende Beschreibung von Maßnahmen und Strategien:

{antwort}

Wende diese auf die Firma XANDU an. Erstelle eine kurze  Übersicht  zu den erwarteten simulierten Auswirkungen auf die drei 
Bewertungsdimensionen (Werte, Wissen, Kultur) innerhalb der ersten vier Wochen. lasse in der Antwort "<br>" weg!

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
        
        st.markdown("**Ihre Maßnahmen und Strategien hätten auf die XANDU GmbH folgende Auswirkungen:**")
        response2 = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "Du bist ein Business-Analyst für KI-Transformationen in mittelständischen Unternehmen."},
                {"role": "user", "content": prompt_xandu}
            ],
            temperature=0.7
        )
        auswirkungen = response2.choices[0].message.content
        st.header("🏭 Auswirkungen auf XANDU GmbH (erste 4 Wochen):")
        st.markdown(auswirkungen)
else:
    st.info("Bitte geben Sie zuerst Ihre Maßnahmen ein.")

st.header('Lassen Sie uns über Ihre Simulation sprechen!')
st.subheader('pascal.rudolf@digitalnewx.com')

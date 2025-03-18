# meeting_summary_prompts.py

# System prompt for the meeting summarizer
system_prompt = """You are a professional multilingual meeting summarizer. Your task is to generate concise, actionable summaries of meeting transcripts while preserving their substantive content. Eliminate small talk, redundant discussions, and irrelevant details. 

Key requirements:
- Summarize only meaningful and substantive points, including decisions, action items, key discussions, and insights.
- Ensure clarity and coherence while maintaining the original intent.
- Return the summary in the language requested by the user. If no language is specified, use the transcript's original language.
- Only and directly return the summary, without additional comments or explanations.

Your summaries should be structured, easy to read, and useful for stakeholders who need key takeaways without reviewing the entire transcript."""

# User prompt templates for different languages
prompt_templates = {
    "english": """Please summarize the following meeting transcript into three clear sections: 1) Overview (2-3 sentences covering meeting purpose, key participants, and overall outcome), 2) Key Discussion Points (bullet points with topic names and 1-2 sentence summaries for each major topic), and 3) Action Items (listing all specific tasks with responsible persons and due dates if mentioned). Maintain the original language used in the meeting.

Summary ratio: {ratio}

{transcript}""",

    "french": """Veuillez résumer la transcription de réunion suivante en trois sections claires : 1) Aperçu (2-3 phrases couvrant l'objectif de la réunion, les participants clés et le résultat global), 2) Points de discussion clés (points avec noms de sujets et résumés de 1-2 phrases pour chaque sujet majeur), et 3) Points d'action (listant toutes les tâches spécifiques avec les personnes responsables et les dates d'échéance si mentionnées). Maintenez la langue originale utilisée dans la réunion.

Ratio de résumé : {ratio}

{transcript}""",

    "german": """Bitte fassen Sie das folgende Besprechungsprotokoll in drei klare Abschnitte zusammen: 1) Überblick (2-3 Sätze zum Zweck der Besprechung, den wichtigsten Teilnehmern und dem Gesamtergebnis), 2) Wichtige Diskussionspunkte (Aufzählungspunkte mit Themennamen und 1-2 Satz-Zusammenfassungen für jedes Hauptthema) und 3) Aktionspunkte (Auflistung aller spezifischen Aufgaben mit verantwortlichen Personen und Fälligkeitsdaten, falls erwähnt). Behalten Sie die in der Besprechung verwendete Originalsprache bei.

Zusammenfassungsverhältnis: {ratio}

{transcript}""",

    "spanish": """Por favor, resume la siguiente transcripción de la reunión en tres secciones claras: 1) Visión general (2-3 oraciones que cubren el propósito de la reunión, los participantes clave y el resultado general), 2) Puntos clave de discusión (puntos con nombres de temas y resúmenes de 1-2 oraciones para cada tema principal), y 3) Elementos de acción (listando todas las tareas específicas con las personas responsables y las fechas de vencimiento si se mencionan). Mantén el idioma original utilizado en la reunión.

Ratio de resumen: {ratio}

{transcript}""",

    "portuguese": """Por favor, resuma a seguinte transcrição da reunião em três seções claras: 1) Visão geral (2-3 frases abrangendo o propósito da reunião, os participantes-chave e o resultado geral), 2) Pontos-chave de discussão (tópicos com nomes e resumos de 1-2 frases para cada tema principal), e 3) Itens de ação (listando todas as tarefas específicas com as pessoas responsáveis e datas de vencimento, se mencionadas). Mantenha a linguagem original usada na reunião.

Proporção do resumo: {ratio}

{transcript}""",

    "italian": """Si prega di riassumere la seguente trascrizione della riunione in tre sezioni chiare: 1) Panoramica (2-3 frasi che coprono lo scopo della riunione, i partecipanti chiave e il risultato complessivo), 2) Punti chiave di discussione (punti elenco con nomi degli argomenti e riassunti di 1-2 frasi per ogni argomento principale), e 3) Elementi d'azione (elenco di tutti i compiti specifici con le persone responsabili e le date di scadenza se menzionate). Mantenere il linguaggio originale utilizzato nella riunione.

Rapporto di sintesi: {ratio}

{transcript}"""
}

# Function to create the full user prompt with the transcript and language
def create_user_prompt(transcript, language="english", ratio=0.2):
    if language.lower() not in prompt_templates:
        language = "english"  # Default to English if language not supported
    
    return prompt_templates[language.lower()].format(transcript=transcript, ratio=ratio)
# LawAssist India - Multilingual Legal Information Assistant

Hackathon brief AIML-05: answer questions using Indian laws, summarize legal text in simple language,
and help users find the relevant Acts and procedures - without giving professional legal advice.

## Run
```
pip install -r requirements.txt
streamlit run app.py
```
Works offline (internet is only used for Google Fonts). No API key needed.

## What it does
- **Ask** - tap a common problem or type a question in English / हिंदी / मराठी. Get the relevant Acts, plain-language
  explanation, step-by-step actions, the office to approach and documents to carry.
- **Documents** - upload a PDF/TXT or paste text: summary, key amounts and dates, clauses to check (with severity),
  legal words explained, risk level, downloadable report. Then ask questions about your own document.
- **Letters & Tools** (new)
  - Draft letters: RTI application (en/hi/mr), security-deposit demand (en/hi/mr), consumer complaint notice,
    cheque-bounce notice (s.138), unpaid-salary demand, complaint to SP when FIR is refused. Download as Word or text.
  - Deadline checker: cheque bounce, consumer complaint, RTI and appeals, POSH complaint.
  - Consumer-court fee finder: which commission to approach and the filing fee.
- **Your Rights** (12 topics) · **Tax & Compliance** (ITR, GST, Udyam, FSSAI, Trademark)
- **Lawyers** (sample data, with filters) · **Emergency** helplines (tap to call)
- Text-size switch (A / A+ / A++) and full language switch (the whole page changes)

## Structure
- app.py - interface
- src/knowledge_base.py - laws and guides in 3 languages (add topics here)
- src/letters.py - letter templates
- src/tools.py - deadline and fee calculators
- src/retrieval.py - TF-IDF matching (word + character n-grams; works for Devanagari)
- src/analyzer.py - key facts, risky-clause rules, legal-word glossary, extractive summary
- data/ - lawyers.json (sample), sample_rent_agreement.txt

## 3-minute demo script
1. Switch the language English -> मराठी, then back. Raise the text size with A+.
2. Tap "Rent & deposit": show the law, steps, where to go.
3. Documents -> "Use sample agreement": show risk level, clauses to check, legal words.
4. Ask: "how much notice is needed to terminate" - the answer highlights the clause in the document.
5. Letters & Tools -> RTI letter in Marathi -> download Word file. Then Deadline checker (cheque bounce).
6. Emergency tab, then close with the disclaimer: information, not legal advice.

## Honest limits
Laws change - verify on official portals. Summaries are extractive (sentences from the document).
Scanned image PDFs need OCR (next step: Tesseract). The lawyer list is sample data.
Letters are drafts; court notices should be reviewed by an advocate.

"""Fill-in-the-blanks drafts of common letters. These are starting drafts, not legal advice."""
from datetime import date

# field kinds: "text", "area", "num", "date"
LETTERS = {
    "rti": {
        "title": {"en": "RTI application", "hi": "RTI आवेदन", "mr": "RTI अर्ज"},
        "about": {"en": "Ask a government office for information. Attach the ₹10 fee (central bodies).",
                  "hi": "सरकारी कार्यालय से जानकारी माँगें। ₹10 शुल्क संलग्न करें (केंद्रीय निकाय)।",
                  "mr": "सरकारी कार्यालयाकडून माहिती मागा. ₹10 शुल्क जोडा (केंद्रीय संस्था)."},
        "langs": ["en", "hi", "mr"],
        "fields": [
            ("name", {"en": "Your full name", "hi": "आपका पूरा नाम", "mr": "तुमचे पूर्ण नाव"}, "text"),
            ("address", {"en": "Your address", "hi": "आपका पता", "mr": "तुमचा पत्ता"}, "area"),
            ("office", {"en": "Office / department (to whom it goes)", "hi": "कार्यालय / विभाग", "mr": "कार्यालय / विभाग"}, "text"),
            ("info", {"en": "What information do you want? (one point per line)", "hi": "कौन सी जानकारी चाहिए? (हर बिंदु नई पंक्ति में)", "mr": "कोणती माहिती हवी? (प्रत्येक मुद्दा नवीन ओळीत)"}, "area"),
        ],
        "body": {
            "en": """To,
The Public Information Officer,
{office}

Date: {today}

Subject: Application under Section 6(1) of the Right to Information Act, 2005

Sir/Madam,

I, {name}, a citizen of India, request the following information under the Right to Information Act, 2005:

{info}

I am enclosing the application fee of Rs. 10/- (by Indian Postal Order / online payment / cash receipt). If any part of this information is held by another public authority, please transfer this request under Section 6(3) and inform me.

Please send the information to the address below.

Yours faithfully,
{name}
{address}
""",
            "hi": """सेवा में,
जन सूचना अधिकारी,
{office}

दिनांक: {today}

विषय: सूचना का अधिकार अधिनियम, 2005 की धारा 6(1) के अंतर्गत आवेदन

महोदय/महोदया,

मैं, {name}, भारत का नागरिक, सूचना का अधिकार अधिनियम, 2005 के अंतर्गत निम्नलिखित जानकारी चाहता/चाहती हूँ:

{info}

मैं आवेदन शुल्क रु. 10/- (भारतीय पोस्टल ऑर्डर / ऑनलाइन भुगतान / नकद रसीद द्वारा) संलग्न कर रहा/रही हूँ। यदि इस जानकारी का कोई भाग किसी अन्य लोक प्राधिकरण के पास है, तो कृपया धारा 6(3) के अंतर्गत यह आवेदन अंतरित कर मुझे सूचित करें।

कृपया जानकारी नीचे दिए पते पर भेजें।

भवदीय,
{name}
{address}
""",
            "mr": """प्रति,
जनमाहिती अधिकारी,
{office}

दिनांक: {today}

विषय: माहितीचा अधिकार अधिनियम, 2005 च्या कलम 6(1) अन्वये अर्ज

महोदय/महोदया,

मी, {name}, भारताचा नागरिक, माहितीचा अधिकार अधिनियम, 2005 अन्वये खालील माहिती मागत आहे:

{info}

मी अर्ज शुल्क रु. 10/- (भारतीय पोस्टल ऑर्डर / ऑनलाइन पेमेंट / रोख पावतीद्वारे) जोडत आहे. या माहितीचा कोणताही भाग दुसऱ्या सार्वजनिक प्राधिकरणाकडे असल्यास कृपया कलम 6(3) अन्वये हा अर्ज वर्ग करून मला कळवावे.

कृपया माहिती खालील पत्त्यावर पाठवावी.

आपला विश्वासू,
{name}
{address}
""",
        },
    },
    "deposit": {
        "title": {"en": "Security deposit demand (tenant to landlord)", "hi": "जमानत राशि वापसी माँग (किरायेदार से मकान मालिक)", "mr": "अनामत रक्कम परतावा मागणी (भाडेकरू ते घरमालक)"},
        "about": {"en": "A written demand is the first step before approaching the Rent Controller or court.",
                  "hi": "रेंट कंट्रोलर या अदालत जाने से पहले लिखित माँग पहला कदम है।",
                  "mr": "रेंट कंट्रोलर किंवा न्यायालयात जाण्यापूर्वी लेखी मागणी हे पहिले पाऊल आहे."},
        "langs": ["en", "hi", "mr"],
        "fields": [
            ("name", {"en": "Your name (tenant)", "hi": "आपका नाम (किरायेदार)", "mr": "तुमचे नाव (भाडेकरू)"}, "text"),
            ("address", {"en": "Your current address", "hi": "आपका वर्तमान पता", "mr": "तुमचा सध्याचा पत्ता"}, "area"),
            ("landlord", {"en": "Landlord's name", "hi": "मकान मालिक का नाम", "mr": "घरमालकाचे नाव"}, "text"),
            ("property", {"en": "Rented property address", "hi": "किराये की संपत्ति का पता", "mr": "भाड्याच्या मालमत्तेचा पत्ता"}, "area"),
            ("amount", {"en": "Deposit paid (₹)", "hi": "जमा की गई राशि (₹)", "mr": "भरलेली रक्कम (₹)"}, "num"),
            ("vacated", {"en": "Date you vacated / handed over the keys", "hi": "घर खाली करने / चाबी सौंपने की तारीख", "mr": "घर रिकामे केल्याची / चावी दिल्याची तारीख"}, "date"),
        ],
        "body": {
            "en": """To,
{landlord}

Date: {today}

Subject: Demand for refund of security deposit of Rs. {amount}/-

Dear Sir/Madam,

I was your tenant at {property}. I paid a refundable security deposit of Rs. {amount}/- and handed over vacant possession of the premises on {vacated}.

Despite this, the deposit has not been returned. I request you to refund the full amount (or give a written, itemised statement of any lawful deductions) within 15 days of receiving this letter, by transfer to my bank account.

If I do not receive the amount within 15 days, I will be forced to take legal steps, including approaching the Rent Controller / competent civil court, at your risk as to costs.

Yours faithfully,
{name}
{address}
""",
            "hi": """सेवा में,
{landlord}

दिनांक: {today}

विषय: जमानत राशि रु. {amount}/- की वापसी की माँग

महोदय/महोदया,

मैं {property} पर आपका किरायेदार था/थी। मैंने रु. {amount}/- की वापसी योग्य जमानत राशि जमा की थी और दिनांक {vacated} को परिसर खाली करके कब्ज़ा सौंप दिया।

इसके बावजूद राशि वापस नहीं की गई है। कृपया इस पत्र के मिलने के 15 दिनों के भीतर पूरी राशि मेरे बैंक खाते में लौटाएँ (या वैध कटौतियों का लिखित, विस्तृत विवरण दें)।

15 दिनों में राशि न मिलने पर मुझे रेंट कंट्रोलर / सक्षम दीवानी अदालत सहित कानूनी कदम उठाने पड़ेंगे, जिसका खर्च आपके जोखिम पर होगा।

भवदीय,
{name}
{address}
""",
            "mr": """प्रति,
{landlord}

दिनांक: {today}

विषय: अनामत रक्कम रु. {amount}/- परत मिळण्याबाबत मागणी

महोदय/महोदया,

मी {property} येथे तुमचा भाडेकरू होतो/होते. मी रु. {amount}/- ची परतावा योग्य अनामत रक्कम भरली होती आणि दिनांक {vacated} रोजी जागा रिकामी करून ताबा दिला.

तरीही रक्कम परत केलेली नाही. कृपया हे पत्र मिळाल्यापासून 15 दिवसांत संपूर्ण रक्कम माझ्या बँक खात्यात परत करावी (किंवा कायदेशीर कपातींचे लेखी, तपशीलवार विवरण द्यावे).

15 दिवसांत रक्कम न मिळाल्यास मला रेंट कंट्रोलर / सक्षम दिवाणी न्यायालयासह कायदेशीर पावले उचलावी लागतील, त्याचा खर्च तुमच्या जबाबदारीवर राहील.

आपला विश्वासू,
{name}
{address}
""",
        },
    },
    "consumer": {
        "title": {"en": "Consumer complaint notice to seller", "hi": "विक्रेता को उपभोक्ता शिकायत नोटिस", "mr": "विक्रेत्याला ग्राहक तक्रार नोटीस"},
        "about": {"en": "Send this before filing on e-Daakhil; it shows you gave the seller a chance to fix the problem.",
                  "hi": "e-Daakhil पर शिकायत से पहले भेजें; इससे दिखता है कि आपने विक्रेता को सुधारने का मौका दिया।",
                  "mr": "e-Daakhil वर तक्रारीपूर्वी पाठवा; यावरून विक्रेत्याला सुधारण्याची संधी दिल्याचे दिसते."},
        "langs": ["en"],
        "fields": [
            ("name", {"en": "Your name", "hi": "आपका नाम", "mr": "तुमचे नाव"}, "text"),
            ("address", {"en": "Your address", "hi": "आपका पता", "mr": "तुमचा पत्ता"}, "area"),
            ("seller", {"en": "Seller / company name", "hi": "विक्रेता / कंपनी", "mr": "विक्रेता / कंपनी"}, "text"),
            ("seller_addr", {"en": "Seller's address / email", "hi": "विक्रेता का पता / ईमेल", "mr": "विक्रेत्याचा पत्ता / ईमेल"}, "area"),
            ("product", {"en": "Product or service", "hi": "वस्तु या सेवा", "mr": "वस्तू किंवा सेवा"}, "text"),
            ("order_date", {"en": "Date of purchase", "hi": "खरीद की तारीख", "mr": "खरेदीची तारीख"}, "date"),
            ("amount", {"en": "Amount paid (₹)", "hi": "भुगतान की गई राशि (₹)", "mr": "भरलेली रक्कम (₹)"}, "num"),
            ("problem", {"en": "What went wrong?", "hi": "क्या समस्या हुई?", "mr": "काय अडचण झाली?"}, "area"),
        ],
        "body": {"en": """To,
{seller}
{seller_addr}

Date: {today}

Subject: Complaint regarding {product} - request for refund / replacement

Dear Sir/Madam,

I purchased {product} from you on {order_date} for Rs. {amount}/-.

Problem: {problem}

This amounts to a defect in goods / deficiency in service under the Consumer Protection Act, 2019. I request you to refund Rs. {amount}/- (or replace / repair the product free of cost) within 15 days of receiving this letter.

If the matter is not resolved within 15 days, I will file a complaint before the Consumer Commission without further notice, and claim compensation and costs.

Yours faithfully,
{name}
{address}
"""},
    },
    "cheque": {
        "title": {"en": "Cheque bounce legal notice (Section 138)", "hi": "चेक बाउंस कानूनी नोटिस (धारा 138)", "mr": "चेक बाउन्स कायदेशीर नोटीस (कलम 138)"},
        "about": {"en": "Must be sent within 30 days of the bank memo. Have an advocate check it before sending.",
                  "hi": "बैंक मेमो के 30 दिनों के भीतर भेजना ज़रूरी है। भेजने से पहले वकील से जँचवाएँ।",
                  "mr": "बँक मेमोपासून 30 दिवसांत पाठवणे आवश्यक. पाठवण्यापूर्वी वकिलाकडून तपासून घ्या."},
        "langs": ["en"],
        "fields": [
            ("name", {"en": "Your name (payee)", "hi": "आपका नाम (प्राप्तकर्ता)", "mr": "तुमचे नाव (प्राप्तकर्ता)"}, "text"),
            ("address", {"en": "Your address", "hi": "आपका पता", "mr": "तुमचा पत्ता"}, "area"),
            ("drawer", {"en": "Name of the person who gave the cheque", "hi": "चेक देने वाले का नाम", "mr": "चेक देणाऱ्याचे नाव"}, "text"),
            ("drawer_addr", {"en": "Their address", "hi": "उनका पता", "mr": "त्यांचा पत्ता"}, "area"),
            ("cheque_no", {"en": "Cheque number", "hi": "चेक नंबर", "mr": "चेक क्रमांक"}, "text"),
            ("cheque_date", {"en": "Cheque date", "hi": "चेक की तारीख", "mr": "चेकची तारीख"}, "date"),
            ("amount", {"en": "Cheque amount (₹)", "hi": "चेक राशि (₹)", "mr": "चेकची रक्कम (₹)"}, "num"),
            ("bank", {"en": "Bank on which cheque was drawn", "hi": "जिस बैंक पर चेक था", "mr": "ज्या बँकेवर चेक होता"}, "text"),
            ("memo_date", {"en": "Date of bank's return memo", "hi": "बैंक रिटर्न मेमो की तारीख", "mr": "बँक रिटर्न मेमोची तारीख"}, "date"),
            ("reason", {"en": "Reason on memo (e.g. funds insufficient)", "hi": "मेमो में कारण (जैसे अपर्याप्त राशि)", "mr": "मेमोवरील कारण (उदा. अपुरी रक्कम)"}, "text"),
        ],
        "body": {"en": """LEGAL DEMAND NOTICE
(Under Section 138 of the Negotiable Instruments Act, 1881)

Date: {today}

To,
{drawer}
{drawer_addr}

Under instructions from and on behalf of {name}, residing at {address}, I/we serve you with the following notice:

1. You issued cheque no. {cheque_no} dated {cheque_date} for Rs. {amount}/- drawn on {bank} in discharge of a legally enforceable debt / liability owed to my client.

2. On presentation, the cheque was returned unpaid by the bank with memo dated {memo_date} for the reason: "{reason}".

3. You are hereby called upon to pay Rs. {amount}/- within 15 (fifteen) days of receipt of this notice, failing which my client will initiate criminal proceedings against you under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, besides civil remedies, at your risk as to costs and consequences.

{name}
{address}

(Draft for guidance only. Have an advocate review and send it by registered post / speed post with a copy kept for evidence.)
"""},
    },
    "salary": {
        "title": {"en": "Unpaid salary demand letter", "hi": "बकाया वेतन माँग पत्र", "mr": "थकीत पगार मागणी पत्र"},
        "about": {"en": "A formal demand to HR before complaining to the Labour Commissioner.",
                  "hi": "श्रम आयुक्त से शिकायत से पहले HR को औपचारिक माँग।",
                  "mr": "कामगार आयुक्ताकडे तक्रारीपूर्वी HR ला औपचारिक मागणी."},
        "langs": ["en"],
        "fields": [
            ("name", {"en": "Your name", "hi": "आपका नाम", "mr": "तुमचे नाव"}, "text"),
            ("address", {"en": "Your address", "hi": "आपका पता", "mr": "तुमचा पत्ता"}, "area"),
            ("employer", {"en": "Employer / company name", "hi": "नियोक्ता / कंपनी", "mr": "मालक / कंपनी"}, "text"),
            ("designation", {"en": "Your designation", "hi": "आपका पद", "mr": "तुमचे पद"}, "text"),
            ("period", {"en": "Months for which salary is unpaid", "hi": "किन महीनों का वेतन बकाया है", "mr": "कोणत्या महिन्यांचा पगार थकीत आहे"}, "text"),
            ("amount", {"en": "Total amount due (₹)", "hi": "कुल बकाया राशि (₹)", "mr": "एकूण थकीत रक्कम (₹)"}, "num"),
        ],
        "body": {"en": """To,
The HR Manager / Director,
{employer}

Date: {today}

Subject: Demand for payment of unpaid salary

Dear Sir/Madam,

I am working / worked with {employer} as {designation}. My salary for {period} amounting to Rs. {amount}/- has not been paid despite repeated requests.

I request you to clear the entire dues by bank transfer within 7 days of receiving this letter. Delay in payment of wages is a violation of the applicable labour law (Code on Wages, 2019).

If the dues are not cleared in 7 days, I will approach the Labour Commissioner / competent authority for recovery.

Yours faithfully,
{name}
{address}
"""},
    },
    "fir": {
        "title": {"en": "Complaint to Superintendent of Police (FIR refused)", "hi": "पुलिस अधीक्षक को शिकायत (FIR से इनकार)", "mr": "पोलीस अधीक्षकांना तक्रार (FIR नाकारली)"},
        "about": {"en": "If the police station refuses to register your FIR, write to the SP (BNSS s.173(4)).",
                  "hi": "थाना FIR दर्ज न करे तो SP को लिखें (BNSS धारा 173(4))।",
                  "mr": "ठाण्याने FIR नोंदवली नाही तर SP ना लिहा (BNSS कलम 173(4))."},
        "langs": ["en"],
        "fields": [
            ("name", {"en": "Your name", "hi": "आपका नाम", "mr": "तुमचे नाव"}, "text"),
            ("address", {"en": "Your address and phone", "hi": "आपका पता और फ़ोन", "mr": "तुमचा पत्ता व फोन"}, "area"),
            ("station", {"en": "Police station that refused", "hi": "जिस थाने ने मना किया", "mr": "ज्या ठाण्याने नकार दिला"}, "text"),
            ("incident_date", {"en": "Date of the incident", "hi": "घटना की तारीख", "mr": "घटनेची तारीख"}, "date"),
            ("incident", {"en": "What happened?", "hi": "क्या हुआ?", "mr": "काय घडले?"}, "area"),
            ("refused_on", {"en": "Date the station refused", "hi": "थाने ने मना किया उस दिन की तारीख", "mr": "ठाण्याने नकार दिल्याची तारीख"}, "date"),
        ],
        "body": {"en": """To,
The Superintendent of Police,
(District)

Date: {today}

Subject: Complaint under Section 173(4) of the Bharatiya Nagarik Suraksha Sanhita, 2023 - refusal to register FIR

Sir/Madam,

On {incident_date}, the following incident occurred:

{incident}

I approached {station} Police Station on {refused_on} to register an FIR, but the officer in charge refused to register it.

I request you to direct the registration of an FIR on the facts above and to investigate the matter. I am enclosing a copy of my written complaint to the police station.

Yours faithfully,
{name}
{address}
"""},
    },
}


def render_letter(letter_id: str, lang: str, values: dict) -> str:
    tpl = LETTERS[letter_id]["body"]
    body = tpl.get(lang) or tpl["en"]
    vals = {k: (str(v).strip() if str(v).strip() else "________") for k, v in values.items()}
    vals["today"] = date.today().strftime("%d %B %Y")

    class _D(dict):
        def __missing__(self, k):
            return "________"
    return body.format_map(_D(vals))

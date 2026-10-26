"""Small calculators: legal deadlines and consumer-court fee / forum finder."""
import calendar
from datetime import date, timedelta


def add_months(d: date, n: int) -> date:
    m = d.month - 1 + n
    y = d.year + m // 12
    m = m % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


# ------------------------------------------------------------------ consumer fee
# (upper limit in rupees, fee) - Consumer Protection (Consumer Disputes Redressal Commissions) Rules, 2020
FEE_SLABS = [
    (5_00_000, 0), (10_00_000, 200), (20_00_000, 400), (50_00_000, 1000), (1_00_00_000, 2000),
    (2_00_00_000, 2500), (4_00_00_000, 3000), (6_00_00_000, 4000), (8_00_00_000, 5000), (10_00_00_000, 6000),
]
TOP_FEE = 7500


def consumer_fee(value: int):
    """Return (fee, forum) where forum is 'district' | 'state' | 'national'."""
    fee = TOP_FEE
    for limit, f in FEE_SLABS:
        if value <= limit:
            fee = f
            break
    forum = "district" if value <= 50_00_000 else "state" if value <= 2_00_00_000 else "national"
    return fee, forum


FORUM_NAMES = {
    "district": {"en": "District Consumer Commission", "hi": "ज़िला उपभोक्ता आयोग", "mr": "जिल्हा ग्राहक आयोग"},
    "state": {"en": "State Consumer Commission", "hi": "राज्य उपभोक्ता आयोग", "mr": "राज्य ग्राहक आयोग"},
    "national": {"en": "National Consumer Commission", "hi": "राष्ट्रीय उपभोक्ता आयोग", "mr": "राष्ट्रीय ग्राहक आयोग"},
}


# ------------------------------------------------------------------ deadlines
DEADLINE_KINDS = {
    "cheque": {"en": "Cheque bounce (Section 138)", "hi": "चेक बाउंस (धारा 138)", "mr": "चेक बाउन्स (कलम 138)"},
    "consumer": {"en": "Consumer complaint", "hi": "उपभोक्ता शिकायत", "mr": "ग्राहक तक्रार"},
    "rti": {"en": "RTI application and appeals", "hi": "RTI आवेदन और अपील", "mr": "RTI अर्ज आणि अपील"},
    "posh": {"en": "Workplace harassment (POSH) complaint", "hi": "कार्यस्थल उत्पीड़न (POSH) शिकायत", "mr": "कामाच्या ठिकाणचा छळ (POSH) तक्रार"},
}

DATE_LABELS = {
    "cheque": {"en": "Date on the bank's cheque-return memo", "hi": "बैंक के चेक रिटर्न मेमो की तारीख", "mr": "बँकेच्या चेक रिटर्न मेमोची तारीख"},
    "consumer": {"en": "Date the problem happened (purchase / service failure)", "hi": "समस्या की तारीख (खरीद / सेवा में चूक)", "mr": "समस्येची तारीख (खरेदी / सेवेतील त्रुटी)"},
    "rti": {"en": "Date you filed the RTI application", "hi": "RTI आवेदन देने की तारीख", "mr": "RTI अर्ज दाखल केल्याची तारीख"},
    "posh": {"en": "Date of the (last) incident", "hi": "(अंतिम) घटना की तारीख", "mr": "(शेवटच्या) घटनेची तारीख"},
}


def deadlines(kind: str, d: date, notice_sent: date = None):
    """List of dicts: {label:{en,hi,mr}, date, note:{en,hi,mr}}."""
    out = []
    if kind == "cheque":
        n = notice_sent or d
        pay_by = n + timedelta(days=15)
        out = [
            {"label": {"en": "Last day to send the legal demand notice", "hi": "कानूनी माँग नोटिस भेजने की अंतिम तारीख", "mr": "कायदेशीर मागणी नोटीस पाठवण्याची अंतिम तारीख"},
             "date": d + timedelta(days=30),
             "note": {"en": "30 days from the memo date.", "hi": "मेमो की तारीख से 30 दिन।", "mr": "मेमोच्या तारखेपासून 30 दिवस."}},
            {"label": {"en": "Other side's 15 days to pay end on", "hi": "दूसरे पक्ष के भुगतान के 15 दिन समाप्त", "mr": "समोरच्या पक्षाचे पैसे देण्याचे 15 दिवस संपतात"},
             "date": pay_by,
             "note": {"en": "Counted from the day they receive the notice (assumed = the date you sent it).", "hi": "नोटिस मिलने के दिन से गिनती (यहाँ भेजने की तारीख मानी गई)।", "mr": "नोटीस मिळाल्याच्या दिवसापासून मोजणी (येथे पाठवल्याची तारीख गृहीत)."}},
            {"label": {"en": "Last day to file the court complaint", "hi": "अदालत में शिकायत दाखिल करने की अंतिम तारीख", "mr": "न्यायालयात तक्रार दाखल करण्याची अंतिम तारीख"},
             "date": add_months(pay_by, 1),
             "note": {"en": "Within 1 month after the 15 days end.", "hi": "15 दिन खत्म होने के बाद 1 महीने के भीतर।", "mr": "15 दिवस संपल्यानंतर 1 महिन्याच्या आत."}},
        ]
    elif kind == "consumer":
        out = [{"label": {"en": "Last day to file the consumer complaint", "hi": "उपभोक्ता शिकायत दाखिल करने की अंतिम तारीख", "mr": "ग्राहक तक्रार दाखल करण्याची अंतिम तारीख"},
                "date": add_months(d, 24),
                "note": {"en": "2 years from the cause of action. Delay can be excused only with good reasons.", "hi": "शिकायत के कारण से 2 वर्ष। देरी तभी माफ़ होती है जब ठोस कारण हो।", "mr": "तक्रारीचे कारण घडल्यापासून 2 वर्षे. ठोस कारण असेल तरच विलंब माफ होतो."}}]
    elif kind == "rti":
        reply = d + timedelta(days=30)
        out = [
            {"label": {"en": "Reply due from the office", "hi": "कार्यालय से उत्तर मिलने की तारीख", "mr": "कार्यालयाकडून उत्तर अपेक्षित तारीख"},
             "date": reply,
             "note": {"en": "30 days (48 hours if life or liberty is involved).", "hi": "30 दिन (जीवन या स्वतंत्रता का मामला हो तो 48 घंटे)।", "mr": "30 दिवस (जीवित किंवा स्वातंत्र्याचा प्रश्न असल्यास 48 तास)."}},
            {"label": {"en": "Last day for First Appeal if there is no reply", "hi": "उत्तर न मिलने पर प्रथम अपील की अंतिम तारीख", "mr": "उत्तर न मिळाल्यास प्रथम अपीलाची अंतिम तारीख"},
             "date": reply + timedelta(days=30),
             "note": {"en": "30 days after the reply was due. If you got an unsatisfactory reply, count 30 days from receiving it.", "hi": "उत्तर की तारीख के 30 दिन बाद। असंतोषजनक उत्तर मिला हो तो मिलने से 30 दिन।", "mr": "उत्तराच्या देय तारखेनंतर 30 दिवस. असमाधानकारक उत्तर मिळाल्यास ते मिळाल्यापासून 30 दिवस."}},
        ]
    elif kind == "posh":
        out = [
            {"label": {"en": "Last day to complain to the Internal Committee", "hi": "आंतरिक समिति में शिकायत की अंतिम तारीख", "mr": "अंतर्गत समितीकडे तक्रारीची अंतिम तारीख"},
             "date": add_months(d, 3), "note": {"en": "3 months from the incident.", "hi": "घटना से 3 महीने।", "mr": "घटनेपासून 3 महिने."}},
            {"label": {"en": "Extended last day (with reasons)", "hi": "बढ़ी हुई अंतिम तारीख (कारण सहित)", "mr": "वाढीव अंतिम तारीख (कारणासह)"},
             "date": add_months(d, 6), "note": {"en": "The committee may extend by up to 3 more months if there are good reasons.", "hi": "ठोस कारण हों तो समिति 3 महीने और बढ़ा सकती है।", "mr": "ठोस कारण असल्यास समिती आणखी 3 महिने वाढवू शकते."}},
        ]
    return out

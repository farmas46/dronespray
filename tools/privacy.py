import json
EL = {
 "title": "Πολιτική απορρήτου",
 "upd": "Τελευταία ενημέρωση: Νοέμβριος 2026",
 "intro": "Η παρούσα πολιτική εξηγεί ποια προσωπικά δεδομένα συλλέγουμε μέσω της ιστοσελίδας DroneSpray, για ποιο σκοπό, πόσο καιρό τα κρατάμε και ποια δικαιώματα έχετε σύμφωνα με τον Γενικό Κανονισμό Προστασίας Δεδομένων (ΕΕ) 2016/679 (GDPR).",
 "s": [
  ["Υπεύθυνος επεξεργασίας", ["FARMA Κυράτσας Γεωργικά Μηχανήματα Ε.Ε., 3ο χλμ. Λάρισας – Καρδίτσας, 41500 Λάρισα. Τηλέφωνο: 2410 622500 · Email: info@farma.com.gr."]],
  ["Ποια δεδομένα συλλέγουμε", [
    "Φόρμα επικοινωνίας: ονοματεπώνυμο, επιχείρηση, χώρα, τηλέφωνο, email, προϊόν ενδιαφέροντος και το μήνυμά σας.",
    "Αίτηση dealer: τα παραπάνω, καθώς και περιοχή, τύπος επιχείρησης και ιστοσελίδα (προαιρετικά).",
    "Newsletter: η διεύθυνση email σας και η συγκατάθεσή σας.",
    "WhatsApp: αν μας γράψετε μέσω WhatsApp, την επικοινωνία διαχειρίζεται η WhatsApp (Meta) σύμφωνα με τους δικούς της όρους."]],
  ["Για ποιο σκοπό και με ποια νομική βάση", [
    "Για να απαντήσουμε στο αίτημά σας, να σας στείλουμε προσφορά ή να οργανώσουμε επίδειξη (ενέργειες πριν από τη σύναψη σύμβασης, άρθρο 6 παρ. 1 β' GDPR).",
    "Για την αξιολόγηση αιτήσεων συνεργασίας (έννομο συμφέρον, άρθρο 6 παρ. 1 στ').",
    "Για την αποστολή newsletter, μόνο με τη συγκατάθεσή σας (άρθρο 6 παρ. 1 α'), την οποία μπορείτε να ανακαλέσετε οποτεδήποτε.",
    "Για στατιστικά επισκεψιμότητας μέσω Google Analytics, μόνο αν το αποδεχτείτε στο σχετικό μήνυμα (άρθρο 6 παρ. 1 α')."]],
  ["Πόσο καιρό κρατάμε τα δεδομένα", [
    "Τα αιτήματα επικοινωνίας και οι αιτήσεις dealer διατηρούνται έως 24 μήνες από την τελευταία επικοινωνία, εκτός αν προκύψει συνεργασία, οπότε ισχύουν οι νόμιμες υποχρεώσεις τήρησης.",
    "Το email του newsletter διατηρείται μέχρι να διαγραφείτε."]],
  ["Σε ποιους κοινοποιούνται", [
    "Δεν πουλάμε και δεν μεταβιβάζουμε τα δεδομένα σας σε τρίτους για διαφημιστικούς σκοπούς.",
    "Μπορεί να τα επεξεργάζονται για λογαριασμό μας πάροχοι φιλοξενίας, email και newsletter, δεσμευμένοι με σύμβαση επεξεργασίας.",
    "Αν ζητήσετε συνεργάτη στη χώρα σας, θα του διαβιβάσουμε τα στοιχεία επικοινωνίας σας μόνο για να σας εξυπηρετήσει.",
    "Αν αποδεχτείτε τα cookies στατιστικών, δεδομένα χρήσης της σελίδας επεξεργάζεται η Google Ireland Ltd (Google Analytics). Ενδέχεται να διαβιβαστούν στις ΗΠΑ, βάσει του Πλαισίου Προστασίας Δεδομένων ΕΕ–ΗΠΑ."]],
  ["Cookies", [
    "Η ιστοσελίδα δεν χρησιμοποιεί cookies διαφήμισης.",
    "Στη συσκευή σας αποθηκεύονται τοπικά η γλώσσα που επιλέξατε και η απάντησή σας στο μήνυμα για τα cookies.",
    "Μόνο αν πατήσετε «Αποδοχή», φορτώνεται το Google Analytics 4, που καταγράφει ανώνυμα στατιστικά, όπως σελίδες που επισκεφθήκατε, τύπο συσκευής και κατά προσέγγιση χώρα. Χρησιμοποιεί τα cookies _ga και _ga_*, που διατηρούνται έως 2 έτη. Αν πατήσετε «Απόρριψη», δεν φορτώνεται καθόλου.",
    "Μπορείτε να αλλάξετε την επιλογή σας οποτεδήποτε από τον σύνδεσμο «Ρυθμίσεις cookies» στο κάτω μέρος της σελίδας.",
    "Οι γραμματοσειρές φιλοξενούνται μαζί με την ιστοσελίδα· δεν γίνεται σύνδεση με το Google Fonts."]],
  ["Τα δικαιώματά σας", [
    "Έχετε δικαίωμα πρόσβασης, διόρθωσης, διαγραφής, περιορισμού, φορητότητας και εναντίωσης στην επεξεργασία, καθώς και ανάκλησης της συγκατάθεσής σας.",
    "Για να τα ασκήσετε, γράψτε μας στο info@farma.com.gr. Θα απαντήσουμε εντός ενός μηνός.",
    "Έχετε επίσης δικαίωμα να υποβάλετε καταγγελία στην Αρχή Προστασίας Δεδομένων Προσωπικού Χαρακτήρα (www.dpa.gr)."]],
  ["Ασφάλεια", ["Λαμβάνουμε εύλογα τεχνικά και οργανωτικά μέτρα για την προστασία των δεδομένων σας από απώλεια, κατάχρηση ή μη εξουσιοδοτημένη πρόσβαση."]],
  ["Αλλαγές", ["Μπορεί να ενημερώνουμε την πολιτική αυτή. Η ισχύουσα έκδοση είναι πάντα δημοσιευμένη σε αυτή τη σελίδα."]]]}
EN = {
 "title": "Privacy policy",
 "upd": "Last updated: November 2026",
 "intro": "This policy explains what personal data we collect through the DroneSpray website, why, how long we keep it and what rights you have under the General Data Protection Regulation (EU) 2016/679 (GDPR).",
 "s": [
  ["Data controller", ["FARMA Kyratsas Agricultural Machinery L.P., 3rd km Larissa – Karditsa road, 41500 Larissa, Greece. Phone: +30 2410 622500 · Email: info@farma.com.gr."]],
  ["What data we collect", [
    "Contact form: full name, company, country, phone, email, product of interest and your message.",
    "Dealer application: the above, plus region, type of business and website (optional).",
    "Newsletter: your email address and your consent.",
    "WhatsApp: if you message us on WhatsApp, the conversation is handled by WhatsApp (Meta) under its own terms."]],
  ["Purpose and legal basis", [
    "To answer your request, send you a quote or arrange a demonstration (steps prior to a contract, Art. 6(1)(b) GDPR).",
    "To assess partnership applications (legitimate interest, Art. 6(1)(f)).",
    "To send the newsletter, only with your consent (Art. 6(1)(a)), which you can withdraw at any time.",
    "For visitor statistics through Google Analytics, only if you accept it in the cookie notice (Art. 6(1)(a))."]],
  ["How long we keep data", [
    "Contact requests and dealer applications are kept for up to 24 months after the last contact, unless a business relationship follows, in which case statutory retention periods apply.",
    "Your newsletter email is kept until you unsubscribe."]],
  ["Who we share it with", [
    "We do not sell or transfer your data to third parties for advertising.",
    "Hosting, email and newsletter providers may process it on our behalf under a data processing agreement.",
    "If you ask for a partner in your country, we pass your contact details to that partner only so they can serve you.",
    "If you accept statistics cookies, usage data is processed by Google Ireland Ltd (Google Analytics). It may be transferred to the USA under the EU–US Data Privacy Framework."]],
  ["Cookies", [
    "The website does not use advertising cookies.",
    "Your chosen language and your answer to the cookie notice are stored locally on your device.",
    "Only if you click “Accept” is Google Analytics 4 loaded. It records anonymous statistics such as pages visited, device type and approximate country, using the _ga and _ga_* cookies, which last up to 2 years. If you click “Decline”, it is not loaded at all.",
    "You can change your choice at any time with the “Cookie settings” link at the bottom of the page.",
    "Fonts are hosted together with the website; no connection is made to Google Fonts."]],
  ["Your rights", [
    "You have the right of access, rectification, erasure, restriction, portability and objection, and to withdraw your consent.",
    "To exercise them, email info@farma.com.gr. We will reply within one month.",
    "You may also lodge a complaint with the Hellenic Data Protection Authority (www.dpa.gr) or your local supervisory authority."]],
  ["Security", ["We take reasonable technical and organisational measures to protect your data against loss, misuse or unauthorised access."]],
  ["Changes", ["We may update this policy. The current version is always published on this page."]]]}
def js():
    return "const PRIV="+json.dumps({"el":EL,"en":EN},ensure_ascii=False)+";\n"

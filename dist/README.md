# DroneSpray – ιστοσελίδα

Στατική ιστοσελίδα, χωρίς server. Ανεβαίνει ως έχει σε GitHub Pages ή Netlify.

## Ρυθμίσεις (αρχείο `config.js`)

Αλλάζει απευθείας στο GitHub (μολυβάκι ✏️ → Commit changes), χωρίς άλλο βήμα.

- `gaId`: ο κωδικός μέτρησης του Google Analytics 4 (π.χ. `G-AB12CD34EF`). Όταν συμπληρωθεί, εμφανίζεται αυτόματα το μήνυμα συγκατάθεσης για τα cookies.
- `formEndpoint`: η διεύθυνση όπου στέλνονται οι φόρμες (π.χ. Formspree). Αν μείνει κενό, οι φόρμες ανοίγουν το email του επισκέπτη με το μήνυμα έτοιμο.
- `formEmail`: το email που λαμβάνει τα μηνύματα όταν δεν υπάρχει `formEndpoint`.

## Αρχεία

- `index.html`: η σελίδα
- `assets/`: ελαχιστοποιημένα CSS και JavaScript (το όνομα αλλάζει σε κάθε έκδοση, ώστε οι επισκέπτες να βλέπουν πάντα την τελευταία)
- `img/`: εικόνες WebP σε 3 μεγέθη
- `fonts/`: γραμματοσειρές WOFF2 (χωρίς Google Fonts)
- `files/`: ο κατάλογος PDF
- `_headers`: ρυθμίσεις cache για Netlify (το GitHub Pages το αγνοεί)
- `CNAME`: το domain της σελίδας για το GitHub Pages

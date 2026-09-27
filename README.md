# Knjižnica

Web aplikacija za upravljanje knjižnicom.

Projekt je izrađen pomoću Flask backenda, Vue.js frontenda i MySQL baze podataka.

## Funkcionalnosti

Aplikacija omogućuje upravljanje:

- autorima
- knjigama
- članovima knjižnice
- posudbama

Za podatke su omogućene CRUD operacije:

- dodavanje
- pregled
- uređivanje
- brisanje

Aplikacija također sadrži:

- pretragu podataka
- paginaciju
- validaciju unosa
- povezivanje knjiga s autorima
- povezivanje posudbi s knjigama i članovima
- dropdown izbornike za povezane podatke

## Tehnologije

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- PyMySQL
- python-dotenv

### Frontend

- Vue 3
- Vuetify
- Vite
- Material Design Icons

### Baza podataka

- MySQL
- phpMyAdmin

## Struktura projekta

```text
knjiznica-projekt
│
├── knjiznica-backend
│   ├── migrations
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── routes.py
│   └── requirements.txt
│
├── knjiznica-frontend
│   ├── src
│   │   ├── components
│   │   │   ├── Autori.vue
│   │   │   ├── Knjige.vue
│   │   │   ├── Clanovi.vue
│   │   │   └── Posudbe.vue
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
│
├── knjiznica_db.sql
└── README.md
```

## Pokretanje baze podataka

1. Pokrenuti Apache i MySQL u XAMPP-u.
2. Otvoriti phpMyAdmin.
3. Kreirati bazu pod nazivom:

```text
knjiznica_db
```

4. Odabrati bazu `knjiznica_db`.
5. Odabrati opciju Import.
6. Uvesti datoteku:

```text
knjiznica_db.sql
```

## Backend

Otvoriti terminal u direktoriju:

```text
knjiznica-backend
```

Kreirati virtualno okruženje:

```bash
python -m venv .venv
```

Aktivirati ga na Windowsu:

```bash
.venv\Scripts\activate
```

Instalirati potrebne pakete:

```bash
pip install -r requirements.txt
```

Potrebno je postaviti `.env` datoteku s podacima za MySQL bazu.

Primjer:

```env
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=knjiznica_db
```

Pokrenuti Flask backend:

```bash
python -m flask --app app run --debug
```

Backend se pokreće na:

```text
http://127.0.0.1:5000
```

## Frontend

Otvoriti drugi terminal u direktoriju:

```text
knjiznica-frontend
```

Instalirati pakete:

```bash
npm install
```

Pokrenuti frontend:

```bash
npm run dev
```

Frontend se pokreće na adresi koju prikaže Vite, najčešće:

```text
http://localhost:5173
```

## Baza podataka

Projekt koristi sljedeće glavne tablice:

- autori
- knjige
- clanovi
- posudbe

Tablica `knjige` povezana je s tablicom `autori`.

Tablica `posudbe` povezana je s tablicama `knjige` i `clanovi`.
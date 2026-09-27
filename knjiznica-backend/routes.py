from flask import Blueprint, jsonify, request
from extensions import db
from models import Autor, Knjiga, Clan, Posudba


api = Blueprint("api", __name__)


# Dohvati sve autore
@api.route("/api/autori", methods=["GET"])
def get_autori():
    autori = Autor.query.all()

    rezultat = []

    for autor in autori:
        rezultat.append({
            "id": autor.id,
            "ime": autor.ime,
            "prezime": autor.prezime,
            "drzava": autor.drzava
        })

    return jsonify(rezultat)


# Dohvati jednog autora
@api.route("/api/autori/<int:id>", methods=["GET"])
def get_autor(id):
    autor = db.get_or_404(Autor, id)

    return jsonify({
        "id": autor.id,
        "ime": autor.ime,
        "prezime": autor.prezime,
        "drzava": autor.drzava
    })


# Dodaj autora
@api.route("/api/autori", methods=["POST"])
def add_autor():
    data = request.get_json()

    autor = Autor(
        ime=data["ime"],
        prezime=data["prezime"],
        drzava=data.get("drzava")
    )

    db.session.add(autor)
    db.session.commit()

    return jsonify({
        "poruka": "Autor uspjesno dodan"
    }), 201


# Uredi autora
@api.route("/api/autori/<int:id>", methods=["PUT"])
def update_autor(id):
    autor = db.get_or_404(Autor, id)
    data = request.get_json()

    autor.ime = data["ime"]
    autor.prezime = data["prezime"]
    autor.drzava = data.get("drzava")

    db.session.commit()

    return jsonify({
        "poruka": "Autor uspjesno uredjen"
    })


# Obrisi autora
@api.route("/api/autori/<int:id>", methods=["DELETE"])
def delete_autor(id):
    autor = db.get_or_404(Autor, id)

    db.session.delete(autor)
    db.session.commit()

    return jsonify({
        "poruka": "Autor uspjesno obrisan"
    })
# =========================
# KNJIGE
# =========================

# Dohvati sve knjige
@api.route("/api/knjige", methods=["GET"])
def get_knjige():
    knjige = Knjiga.query.all()

    rezultat = []

    for knjiga in knjige:
        rezultat.append({
            "id": knjiga.id,
            "naslov": knjiga.naslov,
            "godina": knjiga.godina,
            "zanr": knjiga.zanr,
            "autor_id": knjiga.autor_id,
            "autor": f"{knjiga.autor.ime} {knjiga.autor.prezime}"
        })

    return jsonify(rezultat)


# Dodaj novu knjigu
@api.route("/api/knjige", methods=["POST"])
def add_knjiga():
    data = request.get_json()

    nova_knjiga = Knjiga(
        naslov=data["naslov"],
        godina=data.get("godina"),
        zanr=data.get("zanr"),
        autor_id=data["autor_id"]
    )

    db.session.add(nova_knjiga)
    db.session.commit()

    return jsonify({
        "poruka": "Knjiga uspjesno dodana"
    }), 201


# Izmijeni knjigu
@api.route("/api/knjige/<int:id>", methods=["PUT"])
def update_knjiga(id):
    knjiga = db.get_or_404(Knjiga, id)

    data = request.get_json()

    knjiga.naslov = data.get("naslov", knjiga.naslov)
    knjiga.godina = data.get("godina", knjiga.godina)
    knjiga.zanr = data.get("zanr", knjiga.zanr)
    knjiga.autor_id = data.get("autor_id", knjiga.autor_id)

    db.session.commit()

    return jsonify({
        "poruka": "Knjiga uspjesno izmijenjena"
    })


# Obrisi knjigu
@api.route("/api/knjige/<int:id>", methods=["DELETE"])
def delete_knjiga(id):
    knjiga = db.get_or_404(Knjiga, id)

    db.session.delete(knjiga)
    db.session.commit()

    return jsonify({
        "poruka": "Knjiga uspjesno obrisana"
    })

# =========================
# CLANOVI
# =========================

# Dohvati sve clanove
@api.route("/api/clanovi", methods=["GET"])
def get_clanovi():
    clanovi = Clan.query.all()

    rezultat = []

    for clan in clanovi:
        rezultat.append({
            "id": clan.id,
            "ime": clan.ime,
            "prezime": clan.prezime,
            "email": clan.email,
            "telefon": clan.telefon
        })

    return jsonify(rezultat)


# Dodaj novog clana
@api.route("/api/clanovi", methods=["POST"])
def add_clan():
    data = request.get_json()

    novi_clan = Clan(
        ime=data["ime"],
        prezime=data["prezime"],
        email=data.get("email"),
        telefon=data.get("telefon")
    )

    db.session.add(novi_clan)
    db.session.commit()

    return jsonify({
        "poruka": "Clan uspjesno dodan"
    }), 201


# Izmijeni clana
@api.route("/api/clanovi/<int:id>", methods=["PUT"])
def update_clan(id):
    clan = db.get_or_404(Clan, id)

    data = request.get_json()

    clan.ime = data.get("ime", clan.ime)
    clan.prezime = data.get("prezime", clan.prezime)
    clan.email = data.get("email", clan.email)
    clan.telefon = data.get("telefon", clan.telefon)

    db.session.commit()

    return jsonify({
        "poruka": "Clan uspjesno izmijenjen"
    })


# Obrisi clana
@api.route("/api/clanovi/<int:id>", methods=["DELETE"])
def delete_clan(id):
    clan = db.get_or_404(Clan, id)

    db.session.delete(clan)
    db.session.commit()

    return jsonify({
        "poruka": "Clan uspjesno obrisan"
    })

# =========================
# POSUDBE
# =========================

# Dohvati sve posudbe
@api.route("/api/posudbe", methods=["GET"])
def get_posudbe():
    posudbe = Posudba.query.all()

    rezultat = []

    for posudba in posudbe:
        rezultat.append({
            "id": posudba.id,
            "datum_posudbe": posudba.datum_posudbe,
            "datum_povrata": posudba.datum_povrata,
            "status": posudba.status,
            "knjiga_id": posudba.knjiga_id,
            "clan_id": posudba.clan_id,
            "knjiga": posudba.knjiga.naslov,
            "clan": f"{posudba.clan.ime} {posudba.clan.prezime}"
        })

    return jsonify(rezultat)


# Dodaj novu posudbu
@api.route("/api/posudbe", methods=["POST"])
def add_posudba():
    data = request.get_json()

    nova_posudba = Posudba(
        datum_posudbe=data["datum_posudbe"],
        datum_povrata=data.get("datum_povrata"),
        status=data.get("status", "aktivna"),
        knjiga_id=data["knjiga_id"],
        clan_id=data["clan_id"]
    )

    db.session.add(nova_posudba)
    db.session.commit()

    return jsonify({
        "poruka": "Posudba uspjesno dodana"
    }), 201


# Izmijeni posudbu
@api.route("/api/posudbe/<int:id>", methods=["PUT"])
def update_posudba(id):
    posudba = db.get_or_404(Posudba, id)

    data = request.get_json()

    posudba.datum_posudbe = data.get(
        "datum_posudbe",
        posudba.datum_posudbe
    )

    posudba.datum_povrata = data.get(
        "datum_povrata",
        posudba.datum_povrata
    )

    posudba.status = data.get(
        "status",
        posudba.status
    )

    posudba.knjiga_id = data.get(
        "knjiga_id",
        posudba.knjiga_id
    )

    posudba.clan_id = data.get(
        "clan_id",
        posudba.clan_id
    )

    db.session.commit()

    return jsonify({
        "poruka": "Posudba uspjesno izmijenjena"
    })


# Obrisi posudbu
@api.route("/api/posudbe/<int:id>", methods=["DELETE"])
def delete_posudba(id):
    posudba = db.get_or_404(Posudba, id)

    db.session.delete(posudba)
    db.session.commit()

    return jsonify({
        "poruka": "Posudba uspjesno obrisana"
    })
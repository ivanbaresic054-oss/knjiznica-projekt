from extensions import db


class Autor(db.Model):
    __tablename__ = "autori"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    drzava = db.Column(db.String(100))

    knjige = db.relationship(
        "Knjiga",
        backref="autor",
        lazy=True
    )


class Knjiga(db.Model):
    __tablename__ = "knjige"

    id = db.Column(db.Integer, primary_key=True)
    naslov = db.Column(db.String(150), nullable=False)
    godina = db.Column(db.Integer)
    zanr = db.Column(db.String(100))

    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("autori.id"),
        nullable=False
    )

    posudbe = db.relationship(
        "Posudba",
        backref="knjiga",
        lazy=True
    )


class Clan(db.Model):
    __tablename__ = "clanovi"

    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100), nullable=False)
    prezime = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    telefon = db.Column(db.String(50))

    posudbe = db.relationship(
        "Posudba",
        backref="clan",
        lazy=True
    )


class Posudba(db.Model):
    __tablename__ = "posudbe"

    id = db.Column(db.Integer, primary_key=True)
    datum_posudbe = db.Column(db.String(20), nullable=False)
    datum_povrata = db.Column(db.String(20))
    status = db.Column(db.String(50), default="aktivna")

    knjiga_id = db.Column(
        db.Integer,
        db.ForeignKey("knjige.id"),
        nullable=False
    )

    clan_id = db.Column(
        db.Integer,
        db.ForeignKey("clanovi.id"),
        nullable=False
    )
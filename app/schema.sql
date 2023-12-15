CREATE TABLE IF NOT EXISTS kategorie (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS kantori(
id INTEGER PRIMARY KEY AUTOINCREMENT,
_title_before TEXT,
_name TEXT NOT NULL,
_middle_name TEXT,
_surname TEXT NOT NULL,
_title_after TEXT,
_location TEXT,
_claim TEXT, 
_bio TEXT,
_email TEXT NOT NULL,
_phone INTEGER NOT NULL
);


SELECT * FROM kantori WHERE lokace IS "Brno";

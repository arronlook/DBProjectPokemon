DROP TABLE IF EXISTS tbl_pokemon_moves;
DROP TABLE IF EXISTS tbl_allmoves;
DROP TABLE IF EXISTS tbl_pokemon;
DROP TABLE IF EXISTS tbl_weakness;
/* List of all moves and their info */
CREATE TABLE tbl_allmoves (
    name                    VARCHAR(31)   PRIMARY KEY,
    type                    VARCHAR(8),
    category                VARCHAR(8),
    effect                  VARCHAR(255),
    power                   SMALLINT default NULL,
    acc                     SMALLINT default NULL,
    pp                      SMALLINT default NULL,
    tm                      CHAR(5) default NULL,
    prob_second_effect      SMALLINT default NULL,
    gen                     SMALLINT
);

/* maps (type1, type2) to a vector of weaknesses for all types */
/* Separated from tbl_pokemon because
   tbl_pokemon.pokedex_number functionally determines (type1, type2),
   and (type1, type2) functionally determines all the against_* attributes*/
CREATE TABLE tbl_weakness (
    against_bug       REAL,
    against_dark      REAL,
    against_dragon    REAL,
    against_electric  REAL,
    against_fairy     REAL,
    against_fight     REAL,
    against_fire      REAL,
    against_flying    REAL,
    against_ghost     REAL,
    against_grass     REAL,
    against_ground    REAL,
    against_ice       REAL,
    against_normal    REAL,
    against_poison    REAL,
    against_psychic   REAL,
    against_rock      REAL,
    against_steel     REAL,
    against_water     REAL,
    type1             VARCHAR(15),
    type2             VARCHAR(15),
    PRIMARY KEY (type1, type2)
);

/* list of all pokemon and some default stats */
CREATE TABLE tbl_pokemon (
    attack            SMALLINT,
    classification    VARCHAR(63),
    defense           SMALLINT,
    experience_growth INTEGER,
    height_m          REAL default 0,
    hp                SMALLINT,
    japanese_name     VARCHAR(63)  COLLATE "ja-JP-x-icu",
    name              VARCHAR(15)  UNIQUE,
    percentage_male   REAL         DEFAULT NULL,
    pokedex_number    SMALLINT     PRIMARY KEY,
    sp_attack         SMALLINT,
    sp_defense        SMALLINT,
    speed             SMALLINT,
    type1             VARCHAR(15),
    type2             VARCHAR(15),
    weight_kg         REAL default NULL,
    generation        SMALLINT,
    is_legendary      BOOLEAN,
    FOREIGN KEY (type1, type2) REFERENCES tbl_weakness (type1, type2)
);

/* maps pokemon id to the moves they can learn */
CREATE TABLE tbl_pokemon_moves (
    pokemon_id SMALLINT    REFERENCES tbl_pokemon (pokedex_number),
    move_name  VARCHAR(31) REFERENCES tbl_allmoves (name)
);

/* INDICES */
CREATE INDEX type ON tbl_pokemon using btree (type1, type2);


-- Notes
/*
tbl_allmoves
---------
- power set '-' to NULL
- acc set '-' to NULL, Γê₧ to 1000
- pp set '-' to NULL
- tm set '' to NULL
- prob set '' and '-' to NULL, and it maps to prob_second_effect

tbl_pokemon
---------
- remove attributes (abilities, base_total)
- height_m set '' to 0 or something. geodude's height is 0?
- weight_kg set '' to NULL
- for pokemon name 'minor', there are 2 values for capture_rate. I suggest we separate them into 2 different pokemon, one for meteorite and one for core, since it's the same pokemon in different forms. Or just remove capture_rate
- NOTE that classfication is misspelled in the csv file. should be classification
*/
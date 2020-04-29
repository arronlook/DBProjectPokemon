DROP SCHEMA IF EXISTS pokemon;
CREATE SCHEMA pokemon AUTHORIZATION ash;

CREATE TABLE tbl_allmoves (
    move_id                 SMALLINT      UNIQUE,
    name                    VARCHAR(29)   PRIMARY KEY,
    type                    VARCHAR(8),
    category                VARCHAR(8),
    effect                  VARCHAR(255),
    power                   SMALLINT,
    acc                     SMALLINT,
    pp                      SMALLINT,
    tm                      CHAR(5),
    prob_second_effect      SMALLINT,
    gen                     SMALLINT
);

CREATE TABLE tbl_pokemon (
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
    attack            SMALLINT,
    base_egg_steps    SMALLINT,
    base_happiness    SMALLINT,
    base_total        SMALLINT,
    capture_rate      SMALLINT,
    classification    VARCHAR(63),
    defense           SMALLINT,
    experience_growth INTEGER,
    height_m          REAL,
    hp                SMALLINT,
    japanese_name     VARCHAR(63)  COLLATE "ja-JP-x-icu",
    name              VARCHAR(15)  UNIQUE,
    percentage_male   REAL,
    pokedex_number    SMALLINT     PRIMARY KEY,
    sp_attack         SMALLINT,
    sp_defense        SMALLINT,
    speed             SMALLINT,
    type1             VARCHAR(15),
    type2             VARCHAR(15),
    weight_kg         REAL,
    generation        SMALLINT,
    is_legendary      BOOLEAN
);

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
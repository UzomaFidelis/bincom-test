DROP TABLE IF EXISTS agentname;
CREATE TABLE IF NOT EXISTS agentname (
  name_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT DEFAULT NULL,
  phone TEXT NOT NULL,
  pollingunit_uniqueid INTEGER NOT NULL
); 


DROP TABLE IF EXISTS announced_pu_results;
CREATE TABLE IF NOT EXISTS announced_pu_results (
  result_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  polling_unit_uniqueid TEXT NOT NULL,
  party_abbreviation TEXT NOT NULL,
  party_score INTEGER NOT NULL,
  entered_by_user TEXT NOT NULL,
  date_entered TEXT NOT NULL,
  user_ip_address TEXT NOT NULL
);


DROP TABLE IF EXISTS announced_state_results;
CREATE TABLE IF NOT EXISTS announced_state_results (
  result_id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  state_name TEXT NOT NULL,
  party_abbreviation TEXT NOT NULL,
  party_score INTEGER NOT NULL,
  entered_by_user TEXT NOT NULL,
  date_entered TEXT NOT NULL,
  user_ip_address TEXT NOT NULL
);


DROP TABLE IF EXISTS announced_ward_results;
CREATE TABLE IF NOT EXISTS announced_ward_results (
  result_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  ward_name TEXT NOT NULL,
  party_abbreviation TEXT NOT NULL,
  party_score INTEGER NOT NULL,
  entered_by_user TEXT NOT NULL,
  date_entered TEXT NOT NULL,
  user_ip_address TEXT NOT NULL
);


DROP TABLE IF EXISTS announced_lga_results;
CREATE TABLE IF NOT EXISTS announced_lga_results (
  result_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  lga_name TEXT NOT NULL,
  party_abbreviation TEXT NOT NULL,
  party_score INTEGER NOT NULL,
  entered_by_user TEXT NOT NULL,
  date_entered TEXT NOT NULL,
  user_ip_address TEXT NOT NULL
); 


DROP TABLE IF EXISTS lga;
CREATE TABLE IF NOT EXISTS lga (
  uniqueid  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  lga_id INTEGER NOT NULL,
  lga_name TEXT NOT NULL,
  state_id INTEGER NOT NULL,
  lga_description TEXT,
  entered_by_user TEXT NOT NULL,
  date_entered TEXT NOT NULL,
  user_ip_address TEXT NOT NULL
); 


DROP TABLE IF EXISTS party;
CREATE TABLE IF NOT EXISTS party (
  id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  partyid TEXT NOT NULL,
  partyname TEXT NOT NULL
); 


DROP TABLE IF EXISTS polling_unit;
CREATE TABLE IF NOT EXISTS polling_unit (
  uniqueid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  polling_unit_id INTEGER NOT NULL,
  ward_id INTEGER NOT NULL,
  lga_id INTEGER NOT NULL,
  uniquewardid INTEGER DEFAULT NULL,
  polling_unit_number TEXT DEFAULT NULL,
  polling_unit_name TEXT DEFAULT NULL,
  polling_unit_description TEXT,
  lat TEXT DEFAULT NULL,
  long TEXT DEFAULT NULL,
  entered_by_user TEXT DEFAULT NULL,
  date_entered TEXT DEFAULT NULL,
  user_ip_address TEXT DEFAULT NULL
);


DROP TABLE IF EXISTS states;
CREATE TABLE IF NOT EXISTS states (
  state_id INTEGER NOT NULL PRIMARY KEY,
  state_name TEXT NOT NULL
);


DROP TABLE IF EXISTS ward;
CREATE TABLE IF NOT EXISTS ward (
  uniqueid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  ward_id INTEGER NOT NULL,
  ward_name TEXT NOT NULL,
  lga_id INTEGER NOT NULL,
  ward_description TEXT,
  entered_by_user TEXT NOT NULL,
  date_entered TEXT NOT NULL,
  user_ip_address TEXT NOT NULL
);

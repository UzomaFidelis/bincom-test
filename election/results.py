from datetime import datetime
from flask import (Blueprint, redirect, render_template, request, url_for)
from election.db import get_db

bp = Blueprint('results', __name__)


@bp.route("/")
def index():
    # db = get_db()
    return render_template("results/index.html")

@bp.route("/pu")
def polling_units():
    db = get_db()

    # Results for polling units from the database
    pu_results = db.execute(
        """
        SELECT 
        pu.polling_unit_name AS polling_unit, 
        ar.party_abbreviation AS party,
        ar.party_score AS score,
        pu.uniqueid as pu_uniqueid
        FROM polling_unit pu
        INNER JOIN announced_pu_results ar
        ON 
        ar.polling_unit_uniqueid = pu.uniqueid 
        ORDER BY 
        polling_unit;
        """
    ).fetchall()
    
    # # Results with rows with missing polling unit name removed
    # clean_pu_results = [result for result in pu_results if result["polling_unit"] != ""]

    pu_ids = set([(result["pu_uniqueid"], result["polling_unit"]) for result in pu_results])
    print("Polling Units Actual", pu_ids)

    
    # dictionary to store the party result for the different polling units with the 
    # polling unit name as the key and the party results as a list of tuples

    grouped_results = {}
    for pu_id in pu_ids:
        party_results = [(result["party"], result["score"]) for result in pu_results if  
                         result["pu_uniqueid"] == pu_id[0]]
        result_key = pu_id[1] + " " + f"({pu_id[0]})"
        grouped_results[result_key] = party_results

    print(grouped_results)

    return render_template("results/polling-unit.html", results=grouped_results)

@bp.route("/lga")
def local_governments():
    db = get_db()
    lga_results = db.execute(
        """
        SELECT lg.lga_name, 
        lg.lga_id, 
        ar.party_abbreviation AS party,
        SUM (ar.party_score) as total_votes
        FROM lga lg
        INNER JOIN polling_unit pu
        ON 
        lg.lga_id = pu.lga_id
        INNER JOIN announced_pu_results ar
        ON 
        ar.polling_unit_uniqueid = pu.uniqueid
        GROUP BY lga_name, party
        ORDER BY lga_name;
        """
    ).fetchall()
    
    lga_names = set([result["lga_name"] for result in lga_results])
   
    grouped_results = {}
    for lga_name in lga_names:
        party_results = [(result["party"], result["total_votes"]) for result in lga_results if  
                         result["lga_name"] == lga_name]
        print("Party results", party_results)

        grouped_results[lga_name] = party_results

    return render_template("results/local-government.html", results=grouped_results)


@bp.route("/add-result", methods=('GET', 'POST'))
def add_result():
    db = get_db()
    parties = db.execute(
        """
        SELECT * FROM party;
        """
    )
    if request.method == "POST":
        # print(request.form)
        pu_name = request.form["polling_unit"] 
        pu_id = request.form["polling_unit_id"]
        ward_id = request.form["ward_id"] 
        lga_id = request.form["lga"]
        print(pu_id, ward_id, lga_id) 
        db.execute(
            """
            INSERT INTO polling_unit (polling_unit_id, ward_id, lga_id, 
            polling_unit_name)
            VALUES (?, ?, ?, ?)
            """, (pu_id, ward_id, lga_id, pu_name)
        )
        db.commit()

        new_pu = db.execute(
            """
            SELECT * FROM polling_unit WHERE polling_unit_name = ?
            """, (pu_name,)
        ).fetchone()

        unique_id = new_pu["uniqueid"]
        user = "Fidelis"
        date = datetime.now()
        user_ip = "192.168.1.109"
        for party in parties:
           score = request.form[party["partyid"]]
           if score == "":
               score = 0
           db.execute(
           """
           INSERT INTO announced_pu_results (polling_unit_uniqueid,
           party_abbreviation, party_score, entered_by_user, 
           date_entered, user_ip_address) VALUES (?,?,?,?,?,?)
           """, (unique_id, party["partyid"], score, user, date, 
                   user_ip,)
           ) 
           db.commit()
        return redirect(url_for("results.index"))

    lgas = db.execute(
        """
        SELECT * FROM lga;           
        """).fetchall()
    parties = db.execute(
        """
        SELECT * FROM party;
        """
    )
    return render_template("results/add-result.html", lgas=lgas, parties=parties)

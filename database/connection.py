import sys
import io
import pymysql as db
import json


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


# parsing database configuration information with config.json
with open('../database/config.json') as config_file:
    info = json.load(config_file)

# initialize steps for create connection to database
try:
    # connection instance
    connection = db.connect(host=info['db']['host'], user=info['db']['user'], password=info['db']['password'],
                            db=info['db']['database'], charset="utf8")
    # Create Cursor instance from connection instance
    cursor = connection.cursor()

except db.InternalError as error:
    code, message = error.args
    print(">>>>>>>>>>", code, message)


def save_medicine_api_data(atc_code, atc_code_name, date, insurance_type, money_of_use_amount, recu_cl_code, sggu_code,
                           sggu_code_name, sido_code_name, total_used_medicine_amount):
    # query string
    query = "INSERT INTO atc_api(atcStep4Cd, atcStepCdNm, diagYm, insupTpCd, msupUseAmt, recuClCd, sgguCd, sgguCdNm, sidoCdNm, totUseQty) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # binding of method parameters in to query parameter placeholders and then, execute query
    cursor.execute(query, (
    atc_code, atc_code_name, date, insurance_type, money_of_use_amount, recu_cl_code, sggu_code, sggu_code_name,
    sido_code_name, total_used_medicine_amount))

def load_all_atc_code():
    query = "SELECT atcCode FROM atc_code"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
    return rows

def load_sgis_code():
    query = "SELECT sidoCd, sgguCd FROM medicineaddress"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
    return rows

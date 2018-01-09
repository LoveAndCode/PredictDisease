import sys
import io
import pymysql as db
import json

""" Setting for printing Korean characters """
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

""" Parsing mysqldb configuration information with config.json """
with open('../config/config.json') as config_file:
    info = json.load(config_file)

""" Initialize steps for create connection to mysqldb """
try:
    """ Connection instance """
    connection = db.connect(host=info['db']['host'], user=info['db']['user'], password=info['db']['password'],
                            db=info['db']['database'], charset="utf8")
    """ Create cursor instance from connection instance """
    cursor = connection.cursor()

except db.InternalError as error:
    code, message = error.args
    print(">>>>>>>>>>", code, message)


def save_medicine_info(item):
    query = "INSERT INTO api_data(atcStep4Cd, atcStepCdNm, diagYm, insupTpCd, msupUseAmt, recuClCd, sgguCd, sgguCdNm, sidoCdNm, totUseQty) VALUES('%s', '%s', %s, %s, %s, %s, %s, '%s', '%s', %s)"
    query = query % (
        item.atcstep4cd.string, item.atcstep4cdnm.string, item.diagym.string, item.insuptpcd.string,
        item.msupuseamt.string, item.recuclcd.string, item.sggucd.string, item.sggucdnm.string,
        item.sidocdnm.string, item.totuseqty.string)
    """ binding of method parameters in to query parameter placeholders and then, execute query """
    try:
        re = cursor.execute(query)
    except db.Error as e:
        print(e)
    connection.commit()


def load_all_atc_code():
    query = "SELECT atcCode FROM atc_code"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])
    return rows


def load_sgis_code():
    query = "SELECT sidoCdNm, sgguCdNm, sidoCd, sgguCd FROM parse_sgis"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print("-" * 50)
        print("[행정구역] %s - %s" % (row[0], row[1]))
        print("[SGIS_CODE] %s - %s" % (row[2], row[3]))
        print("-" * 50)
    return rows


def load_predict_result(diseasecode=None):
    if diseasecode is None:
        query = "SELECT diagYm, city, usedMedicineQty, predictPatients FROM result"
    else:
        query = "SELECT diagYm, city, usedMedicineQty, predictPatients AS patients FROM result WHERE diseaseCode = %d" % diseasecode
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def all_city():
    query = "SELECT DISTINCT city FROM result"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def important_city():
    query = "SELECT DISTINCT city FROM result WHERE city in ('서울특별시', '부산광역시', '인천광역시', '대구광역시', '대전광역시', '광주광역시', '울산광역시', '청주시')"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

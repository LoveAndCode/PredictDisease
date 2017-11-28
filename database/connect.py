import pymysql
import sys
import io
import configparser
import json

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

with open('F:\JJH\DevProject\python\python_DALAB\database\config.json', 'r') as f:
    config = json.load(f)

try:
    connect = pymysql.connect(
        host=config['dbconfig']['host'], port=config['dbconfig']['port'], user=config['dbconfig']['user'], passwd=config['dbconfig']['password'], db=config['dbconfig']['db'], charset='utf8'
    )
    cur = connect.cursor()

except pymysql.InternalError as error :
    code, message = error.args
    print(">>>>>>>>>>", code, message)

## database method for parsing of medicine data
def get_atc_code():
    query="SELECT atcCode FROM atc_code"
    cur.execute(query)
    result = cur.fetchall()
    return result

def get_atc_code_by(atcCodeType):
    query = "SELECT atcCode FROm atc_code WHERE atcCode LIKE '%s%%'" %atcCodeType
    cur.execute(query)
    result = cur.fetchall()
    return result


def get_all_address():
    cur.execute("SELECT * FROM address")
    result = cur.fetchall()
    return result


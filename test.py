from database import connect
from api import medicine
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(),encoding='utf-8')

atc_list = connect.get_atc_code()

for atcCode in atc_list:
    medicine.get_medicine_data("201001","110000","110001",atcCode[0])

from bs4 import BeautifulSoup
import requests
import sys
import io
from mysqldb import database as atcdb

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


class MedicineAPI:
    def __init__(self, api_key, log=None):
        self.api = "http://apis.data.go.kr/B551182/msupUserInfoService/getAtcStp4AreaList?"
        self.key = "ServiceKey=" + api_key
        self.rows = "&numOfRows=100"
        self.page = "&pageNo=1"
        self.insuranceType = "&insupTp=0"
        self.cpmdPrscTp = "&cpmdPrscTp=02"
        self.url = None
        self.logging = log

    def parse(self, atccode, sidoCode, sgguCode, diagYm):
        """ Parameter of parsing condition """
        atc = "&atcStep4Cd=" + atccode
        date = "&diagYm=" + diagYm
        sido = "&sidoCd=" + sidoCode
        sggu = "&sgguCd=" + sgguCode

        url = self.api + self.key + self.rows + self.page + date + atc + self.insuranceType + self.cpmdPrscTp + sido + sggu

        data = requests.get(url)
        soup = BeautifulSoup(data.text, "lxml")
        items = soup.find_all("item")

        try:
            for item in items:
                if self.logging:
                    print("=" * 50)
                    print("date:", item.diagym.string)
                    print("atcCode: ", item.atcstep4cd.string)
                    print("atcCodeName: ", item.atcstep4cdnm.string)
                    print("amountOfMedicine: ", item.totuseqty.string)
                    print("totalMoneyOfMedicine: ", item.msupuseamt.string + "원")
                    print("gu: ", item.sggucdnm.string)
                    print("sido: ", item.sidocdnm.string)
                    print("sidoCode: ", sidoCode)
                    print("guCode: ", item.sggucd.string)
                    print("=" * 50)
                atcdb.save_medicine_info(item)
        except:
            print("ERROR: THIS [", atccode, "] IS NOT MATCHED IN APIES")

    def debug_toggle(self):
        if self.logging:
            self.logging = False
        else:
            self.logging = True

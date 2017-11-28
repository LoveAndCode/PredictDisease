import requests
import sys
import io
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(),encoding='utf-8')


def get_medicine_data(diagYm, sidoCode, sgguCode, atcCode):
    # atc 4step code api url
    url = "http://apis.data.go.kr/B551182/msupUserInfoService/getAtcStp4AreaList?"
    key = "ServiceKey" + "=uKoS2h8nLZtyARxcnTC64ywVHm%2Fh0RG27jMg2mdabNVJyU%2FdnmUVRBMnMCk6stklk9ZBwAKmMtXtRxiyaHRGTg%3D%3D"
    # assignment value to query parameters
    rows = "&numOfRows=100"
    pageNo = "&pageNo=1"
    date = "&diagYm="+diagYm
    atc = "&atcStep4Cd="+atcCode
    insuranceType = "&insupTp=0"
    cpmdPrscTp = "&cpmdPrscTp=02"
    sido = "&sidoCd="+sidoCode
    sggu = "&sgguCd="+sgguCode
    # builde api request url
    api_url = url + key + rows + pageNo + date + atc + insuranceType + cpmdPrscTp + sido + sggu
    # send request to the api server
    data = requests.get(api_url)
    soup = BeautifulSoup(data.text, 'lxml')
    try:
        for item in soup.find_all('item'):
            print("=================================")
            print("date:",item.diagym.string)
            print("atcCode: ",item.atcstep4cd.string)
            print("amountOfMedicine: ", item.totuseqty.string)
            print("totalMoneyOfMedicine: ",item.msupuseamt.string,"원")
            print("gu: ",item.sggucdnm.string)
            print("sido: ",item.sidocdnm.string)
            print("sidoCode: ", sidoCode)
            print("guCode: ", item.sggucd.string)
            print("=================================")
    except:
        print("ERROR: THIS [",atcCode,"] IS NOT MATCHED IN APIES")
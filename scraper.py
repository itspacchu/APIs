from bs4 import BeautifulSoup
import requests
from pprint import pprint
import itertools
import threading
import time
import sys

# Test multithread for loading animation
# def animate(done = False):
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if done:
#             break
#         sys.stdout.write('\rloading ' + c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\rDone!     ')
# t = threading.Thread(target=animate)


class JNTUResult:
    SERVERS = ['http://results.jntuh.ac.in', 'http://202.63.105.184/results']
    RECURSIVE_LIMIT = 5  # Its better to not exceed 10
    EXAM_CODE_TOL = 10  # Better not to excede 20

    def __init__(self, rollNum: str, examCode: int, **kwargs):
        self.user = None
        self.result = None

        self.rollNum = self.isValidRollNumber(rollNum)
        self.examCode = str(examCode)
        self.appox_code = None
        self.degree = kwargs.get('degree', "btech")  # Defaults to btech
        self.eType = kwargs.get('eType', "r17")  # Defaults to R18 results
        # Defaults to Sem results
        self.out_type = kwargs.get('out_type', "intgrade")

        self.url = self.get_url()

    def __call__(self) -> dict:
        if not self.result:
            self.result = self.JNTUResultAPI()
            self.sgpa = self.SGPACalculator(self.result)
        return {
            'user': self.user,
            'result': self.result,
            'sgpa': self.sgpa
        }

    def recursiveGet(self) -> dict:
        limit = 0
        while True:
            res = self.__call__()
            if self.user or limit > self.RECURSIVE_LIMIT:
                break
            limit += limit
            self.url = self.get_url() if limit % 2 == 0 else self.get_url(server=1)
        return res

    def examCodeEstimate(self):
        tolerance = self.EXAM_CODE_TOL
        appoxVal = int(self.examCode)
        self.appox_code = appoxVal
        for i in range(appoxVal-tolerance, appoxVal+tolerance+1):
            self.examCode = str(i)
            self.url = self.get_url()
            try:
                res = self.recursiveGet()
                return i
            except ValueError:
                pass
        self.examCode = self.appox_code
        return -1

    @staticmethod
    def isValidRollNumber(rollNum: str = None) -> str:
        if(len(rollNum) != 10):
            raise ValueError("Roll-Number not 10 digit")
        try:
            int(rollNum[:2])
            int(rollNum[-3:], base=19)  # G and H are in rollno
        except ValueError:
            raise ValueError("Roll-Number not Valid")
        return rollNum

    def get_url(self, server: int = 0) -> str:
        params = [
            f"degree={self.degree}",
            f"&examCode={self.examCode}",
            f"&etype={self.eType}",
            f"&type={self.out_type}",
            f"&htno={self.rollNum}",
            f"&result=null&grad=null"
        ]
        final = f'{self.SERVERS[server]}/resultAction?'+''.join(params)
        # print(final)
        return final

    @staticmethod
    def gradeToPoints(grade: str) -> int:
        if(grade == 'F' or grade == 'Ab'):  # Leo has big brains you know efficiency 100%
            return 0
        elif(grade == 'C'):
            return 5
        elif(grade == 'B'):
            return 6
        elif(grade == 'B+'):
            return 7
        elif(grade == 'A'):
            return 8
        elif(grade == 'A+'):
            return 9
        elif(grade == "O"):
            return 10
        else:
            return 0

    def SGPACalculator(self, result: dict) -> float:
        if not result:
            return
        total_credit = 0
        gpa_accum = 0
        for item in result:
            g2p = self.gradeToPoints(item['GRADE'])
            if(g2p == 0):
                return float(0.0)
            gpa_accum += g2p * float(item['CREDIT'])
            total_credit += float(item['CREDIT'])
        return round(gpa_accum/total_credit, 2)

    def JNTUResultAPI(self):
        resultDict = []
        response = requests.request("POST", self.url, timeout=5)

        if(response.status_code >= 300):
            return

        soup = BeautifulSoup(response.text, "html.parser")
        resultTable = soup.find_all('table')

        if resultTable[0].find_all('tr')[0].text.find("invalid hallticket number") != -1:
            raise ValueError("The given Hallticket number doesn't exist")

        nameRow = resultTable[0].find_all('b')
        self.user = [nameRow[n+1].text for n in range(0, len(nameRow), 2)]
        tableRow = resultTable[1].find_all('tr')

        for i in range(1, len(tableRow)):
            tr = tableRow[i]
            try:
                currentCol = tr.text.split('\n')[1:-1]
                resultDict.append({
                    'SUB_CODE': currentCol[0],
                    'SUB_NAME': currentCol[1],
                    'INTERNAL': currentCol[2],
                    'EXTERNAL': currentCol[3],
                    'TOTAL': currentCol[4],
                    'GRADE': currentCol[5],
                    'CREDIT': currentCol[6]
                })
            except Exception as e:
                print(e)
                break

        return resultDict


if __name__ == "__main__":
    result = JNTUResult("18XX1A0XXX", 1454)     # 1454 works
    # pprint(result.examCodeEstimate())
    pprint(result.recursiveGet())

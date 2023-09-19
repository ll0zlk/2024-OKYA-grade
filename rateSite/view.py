from django.contrib import admin
from django.urls import path
from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.shortcuts import render
import os
from django.views.decorators.csrf import csrf_exempt

# OAuth 2.0 인증 설정
urlpatterns = [
    path("admin/", admin.site.urls),
    
]

current_script_path = os.path.abspath(__file__)
current_script_directory = os.path.dirname(current_script_path)
file_path = os.path.join(current_script_directory, "ratesite-398619-99e9c3c10bb4.json")

def index(request):
    return render(request, 'index.html')

def upload(request):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key("1XZIPPweb2iyICKmrKiu3KuiHGLN7Nj8uBmZmfxn2q44").sheet1

    score = 0
    myDict = {"A" : 200, "B" : 180, "C" : 160, "D" : 120, "E": 100}
    if request.method == 'POST':
        # POST 요청 처리 및 원하는 작업 수행
        for period in range(2,4):
            for grade in range(1,3):
                for subject in ["kor","mat","eng"]:
                    hakGi = str(period)+"-"+str(grade)+"-"+str(subject)
                    b = myDict[request.POST.get(hakGi).upper()]
                    score += b
                    if subject == "mat":
                        score += b
        id = request.POST.get("id")
        name = request.POST.get("name")
        data = [id ,name, score/16]
        
        hakBun = sheet.col_values(1)
        exsitingData = False
        for i, x in enumerate(hakBun, start=1):
            if id == x:
                sheet.update(f"A{i}:C{i}",[data])
                exsitingData = True

        if not exsitingData:
            sheet.append_row(data, 1)
            
    return render(request,"index.html")
    

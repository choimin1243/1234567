
from fastapi import FastAPI,Depends

import models
from database import engine,SessionLocal
from router import auth,todos,admin,users
from openpyxl import load_workbook

# 엑셀 파일 로드
workbook = load_workbook('excelwrite.xlsx')

# 첫 번째 시트 선택
sheet = workbook.active

# A1 셀 값 출력
cell_value = sheet['A1'].value
print("A1 셀의 값:", cell_value)





app=FastAPI()
models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)






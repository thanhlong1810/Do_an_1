from flask import Flask

app = Flask(__name__)
app.secret_key = "do_an_m1"

import Ban_Tivi.app_Khach_tham_quan
import Ban_Tivi.app_Nhan_vien_Nhap_hang
import Ban_Tivi.app_Nhan_vien_Ban_hang
import Ban_Tivi.app_Quan_ly_Nhap_hang
import Ban_Tivi.app_Quan_ly_Ban_hang
import Ban_Tivi.app_Quan_ly_Cong_ty
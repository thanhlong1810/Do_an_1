from flask import render_template, request
from Ban_Tivi import app
from Ban_Tivi.Thu_vien.Khach_tham_quan.Xu_ly_3L import *

@app.route("/", methods=["GET", "POST"])
def Khach_tham_quan():
    # Khởi động dữ liệu
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    # Khai báo biến
    Danh_sach_Tivi_Xem = Danh_sach_Tivi
    Chuoi_Tra_cuu = ""

    # Xử lí tìm kiếm
    if request.form.get("Th_Chuoi_Tra_cuu"):
        Chuoi_Tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
        Danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi)

    # Xuất kết quả
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)


    return render_template('Khach_tham_quan/MH_Chinh.html',
                           Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi,
                           Chuoi_Tra_cuu=Chuoi_Tra_cuu)
from flask import render_template, request, redirect, session
from Ban_Tivi import app
from Ban_Tivi.Thu_vien.Nhan_vien_Nhap_hang.Xu_ly_3L import *
from datetime import datetime



@app.route("/nvnh/xem_danh_sach_tivi", methods=["GET", "POST"])
def NVNH_Ds_tivi():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_Xem = Danh_sach_Tivi

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)

    return render_template('Nhan_vien_Nhap_hang/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)



@app.route("/nvnh", methods= ["GET", "POST"])
def NVNH_Chinh():
    if session.get('session_NVNH') is None:
        return redirect(url_for("NVNH_Dang_nhap     "))

    Nhan_Vien_Dang_Nhap = session['session_NVNH']
    Chuoi_HTML_Nhan_Vien = Tao_chuoi_HTML_Nhan_vien(Nhan_Vien_Dang_Nhap)

    Dia_Chi_Man_Hinh = "/nvnh/xem_danh_sach_tivi"
    Chuoi_tra_cuu = ""
    if request.method == "POST":
        Ma_so = request.form.get('Th_Ma_so')
        if Ma_so == "DANH_SACH":
            Dia_Chi_Man_Hinh = "/nvnh/xem_danh_sach_tivi"
        elif Ma_so == "PHIEU_NHAP":
            Dia_Chi_Man_Hinh = "/nvnh/danh-sach-phieu-nhap"
        elif Ma_so == "TRA_CUU":
            Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
            if Chuoi_tra_cuu == "":
                Dia_Chi_Man_Hinh = "/nvnh/xem_danh_sach_tivi"
            else:
                Dia_Chi_Man_Hinh = "/nvnh/tra_cuu/" + Chuoi_tra_cuu

    return render_template('Nhan_vien_Nhap_hang/MH_Chinh.html',
                           Chuoi_HTML_Nhan_Vien = Chuoi_HTML_Nhan_Vien,
                           Dia_chi_MH = Dia_Chi_Man_Hinh,
                           Chuoi_Tra_cuu = Chuoi_tra_cuu)



@app.route('/nvnh/dang-nhap', methods=['GET','POST'])
def NVNH_Dang_nhap():
    # Kiểm tra nếu đã đăng nhập thì sẽ chuyển hướng về trang chính
    if session.get('session_NVNH') is not None:
        return redirect(url_for("NVNH_Chinh"))

    Ten_dang_nhap = ""
    Mat_khau = ""
    Thong_bao = ""
    if request.form.get("Th_Ten_dang_nhap"):
        Ten_dang_nhap = request.form.get("Th_Ten_dang_nhap")
        Mat_khau = request.form.get("Th_Mat_khau")

        # Lấy thông tin từ file cong ty.json
        Cong_ty = Doc_Cong_ty()
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Nhan_vien_Nhap_hang"], Ten_dang_nhap, Mat_khau)
        Hop_le = Nhan_vien is not None
        if Hop_le:
            session["session_NVNH"] = Nhan_vien  # thực hiện gán giá trị
            return redirect(url_for("NVNH_Chinh"))
        else:
            Thong_bao = "Đăng nhập không hợp lệ."

    return render_template('Nhan_vien_Nhap_hang/MH_Dang_nhap.html',
                           Ten_dang_nhap=Ten_dang_nhap,
                           Mat_khau=Mat_khau,
                           Chuoi_Thong_bao=Thong_bao)



@app.route("/nvnh/dang_xuat", methods=["GET", "POST"])
def NVNH_Dang_xuat():
    session.pop("session_NVNH", None)
    return redirect(url_for("NVNH_Dang_nhap"))



@app.route("/nvnh/tra_cuu/<string:Chuoi_tim_kiem>", methods=["GET", "POST"])
def NVNH_tim_kiem(Chuoi_tim_kiem):
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_xem = Tra_cuu_Tivi(Chuoi_tim_kiem, Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_xem)

    return render_template('Nhan_vien_Nhap_hang/MH_Xem_Danh_sach_Tivi.html',
                           Chuoi_HTML_Danh_sach_Tivi = Chuoi_HTML_Danh_sach_Tivi)



@app.route("/nvnh/nhap/<string:Ma_so>/", methods=["GET", "POST"])
def NVNH_Nhap(Ma_so):
    Nhan_vien_Dang_nhap = session["session_NVNH"]
    Danh_sach_tivi = Doc_Danh_sach_Tivi()
    Tivi_chon = Lay_chi_tiet_Tivi(Danh_sach_tivi, Ma_so)
    So_luong = "1"
    Thong_bao = ""
    if Tivi_chon is not None:
        if request.form.get("Th_So_luong"):
            So_luong = int(request.form.get("Th_So_luong"))
            Thanh_tien = Nhap_Tivi(Nhan_vien_Dang_nhap, Tivi_chon, So_luong)
            Ghi_Tivi(Tivi_chon)
            Thong_bao = "Vừa nhập " + str(So_luong) + " " + Tivi_chon["Ten"] + "<br>"
            Thong_bao += "Tiền phải nhập là: " + "{:,}".format(Thanh_tien).replace(",", ".")
    Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_chon, Thong_bao, So_luong)

    return render_template('Nhan_vien_Nhap_hang/MH_Nhap_Tivi.html',
                           Chuoi_HTML_Tivi = Chuoi_HTML_Tivi)



@app.route("/nvnh/danh-sach-phieu-nhap", methods=["GET", "POST"])
def NVNH_Thong_ke_Phieu_nhap():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    Ngay_hien_hanh = datetime.now().strftime("%d-%m-%Y")
    Danh_sach_Tivi_nhap = Danh_sach_Tivi_Nhap_Theo_ngay(Danh_sach_Tivi, Ngay_hien_hanh)
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_nhap, Ngay_hien_hanh)

    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)

    return render_template("Nhan_vien_Nhap_hang/MH_Xem_Phieu_nhap.html",
                            Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)
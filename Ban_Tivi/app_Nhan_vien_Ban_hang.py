from flask import render_template, request, redirect, session
from Ban_Tivi import app
from Ban_Tivi .Thu_vien.Nhan_vien_Ban_hang.Xu_ly_3L import *
from datetime import datetime

@app.route("/nvbh", methods=["GET", "POST"])
def NVBH_Chinh():
    # Kiểm tra nếu chưa đăng nhập thì sẽ chuyển hướng về trang đăng nhập
    if session.get('session_NVBH') is None:
        return redirect(url_for("NVBH_Dang_nhap"    ))

    # Lấy thông tin nhân viên đã đăng nhập để hiển thị ra màn hình
    Nhan_vien_Dang_nhap = session["session_NVBH"]
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

        # Xử lí màn hình
    Dia_chi_Man_hinh = "/nvbh/xem_danh_sach_tivi"
    Chuoi_tra_cuu = ""
    if request.method == "POST": # if request.form.get("Th_Ma_so")
        Ma_so = request.form.get("Th_Ma_so")
        if Ma_so == "DANH_SACH":
            Dia_chi_Man_hinh = "/nvbh/xem_danh_sach_tivi"
        elif Ma_so == "DOANH_THU":
            Dia_chi_Man_hinh = "/nvbh/danh-sach-phieu-ban"
        elif Ma_so == "TRA_CUU":
            Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
            if Chuoi_tra_cuu == "":
                Dia_chi_Man_hinh = "/nvbh/xem_danh_sach_tivi"
            else:
                Dia_chi_Man_hinh = "/nvbh/tra-cuu/" + Chuoi_tra_cuu

    return render_template('Nhan_vien_Ban_hang/MH_Chinh.html',
                           Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien,
                           Dia_chi_MH=Dia_chi_Man_hinh,
                           Chuoi_Tra_cuu=Chuoi_tra_cuu)


@app.route("/nvbh/ban/<string:Ma_so>/", methods=["GET", "POST"])
def NVBH_Ban(Ma_so):
    Nhan_vien_Dang_nhap = session["session_NVBH"]
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)
    So_luong = "1"
    Thong_bao = ""
    if Tivi_Chon is not None:
        if request.form.get("Th_So_luong"):
            So_luong = int(request.form.get("Th_So_luong"))
            Thanh_tien = Ban_Tivi(Nhan_vien_Dang_nhap, Tivi_Chon, So_luong)
            Ghi_Tivi(Tivi_Chon)
            Thong_bao = "Vừa bán " + str(So_luong) + " " + Tivi_Chon["Ten"] + "<br>"
            Thong_bao += "Tiền phải thu là: " + "{:,}".format(Thanh_tien).replace(",",".")

    Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, So_luong)

    return render_template('Nhan_vien_Ban_hang/MH_Ban_Tivi.html',
                            Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)


@app.route("/nvbh/tra-cuu/<string:Chuoi_tim_kiem>", methods=["GET", "POST"])
def NVBH_Tim_kiem(Chuoi_tim_kiem):
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_Xem = Tra_cuu_Tivi(Chuoi_tim_kiem, Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)

    return render_template('Nhan_vien_Ban_hang/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)


@app.route("/nvbh/danh-sach-phieu-ban", methods=["GET", "POST"])
def NVBH_Thong_ke_Phieu_ban():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    Ngay_hien_hanh = datetime.now().strftime("%d-%m-%Y")
    Danh_sach_Tivi_nhap = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay_hien_hanh)
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_nhap, Ngay_hien_hanh)

    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)

    return render_template("Nhan_vien_Ban_hang/MH_Xem_Doanh_thu.html",
                            Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_ke_Tivi)



@app.route("/nvbh/xem_danh_sach_tivi", methods=["GET", "POST"])
def NVBH_Ds_tivi():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_Xem = Danh_sach_Tivi

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)

    return render_template('Nhan_vien_Ban_hang/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)


@app.route('/nvbh/dang-nhap', methods=['GET','POST'])
def NVBH_Dang_nhap():
    # Kiểm tra nếu đã đăng nhập thì sẽ chuyển hướng về trang chính
    if session.get('session_NVBH') is not None:
        return redirect(url_for("NVBH_Chinh"))

    Ten_dang_nhap = ""
    Mat_khau = ""
    Thong_bao = ""
    if request.form.get("Th_Ten_dang_nhap"):
        Ten_dang_nhap = request.form.get("Th_Ten_dang_nhap")
        Mat_khau = request.form.get("Th_Mat_khau")

        # Lấy thông tin từ file cong ty.json
        Cong_ty = Doc_Cong_ty()
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Nhan_vien_Ban_hang"], Ten_dang_nhap, Mat_khau)
        Hop_le = Nhan_vien is not None
        if Hop_le:
            session["session_NVBH"] = Nhan_vien  # thực hiện gán giá trị
            return redirect(url_for("NVBH_Chinh"))
        else:
            Thong_bao = "Đăng nhập không hợp lệ."

    return render_template('Nhan_vien_Ban_hang/MH_Dang_nhap.html',
                           Ten_dang_nhap=Ten_dang_nhap,
                           Mat_khau=Mat_khau,
                           Chuoi_Thong_bao=Thong_bao)




@app.route("/nvbh/dang_xuat", methods=["GET", "POST"])
def NVBH_Dang_xuat():
    session.pop("session_NVBH", None)
    return redirect(url_for("NVBH_Dang_nhap"))

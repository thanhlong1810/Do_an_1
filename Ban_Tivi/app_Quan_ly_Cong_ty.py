from flask import render_template, request, session, redirect, url_for
from Ban_Tivi import app
from Ban_Tivi.Thu_vien.Quan_ly_Cong_ty.Xu_ly_3L import *
from datetime import datetime



@app.route('/qlct/dang-nhap', methods=['GET','POST'])
def QLCT_Dang_nhap():
    # Kiểm tra nếu đã đăng nhập thì sẽ chuyển hướng về trang chính
    if session.get('session_QLCT') is not None:
        return redirect(url_for("QLCT_Chinh"))

    Ten_dang_nhap = ""
    Mat_khau = ""
    Thong_bao = ""
    if request.form.get("Th_Ten_dang_nhap"):
        Ten_dang_nhap = request.form.get("Th_Ten_dang_nhap")
        Mat_khau = request.form.get("Th_Mat_khau")

        # Lấy thông tin từ file cong ty.json
        Cong_ty = Doc_Cong_ty()
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Quan_ly_Cong_ty"], Ten_dang_nhap, Mat_khau)
        Hop_le = Nhan_vien is not None
        if Hop_le:
            session["session_QLCT"] = Nhan_vien  # thực hiện gán giá trị
            return redirect(url_for("QLCT_Chinh"))
        else:
            Thong_bao = "Đăng nhập không hợp lệ."

    return render_template('Quan_ly_Cong_ty/MH_Dang_nhap.html',
                           Ten_dang_nhap=Ten_dang_nhap,
                           Mat_khau=Mat_khau,
                           Chuoi_Thong_bao=Thong_bao)



@app.route("/qlct/dang_xuat", methods=["GET", "POST"])
def QLCT_Dang_xuat():
    session.pop("session_QLCT", None)
    return redirect(url_for("QLCT_Dang_nhap"))



@app.route("/qlct/xem_danh_sach_tivi", methods=["GET", "POST"])
def QLCT_Ds_tivi():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_Xem = Danh_sach_Tivi

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)

    return render_template('Quan_ly_Cong_ty/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)



@app.route("/qlct", methods=["GET", "POST"])
def QLCT_Chinh():
    if session.get("session_QLCT") is None:
        return redirect(url_for("QLCT_Dang_nhap"))

    Nhan_vien_Dang_nhap = session["session_QLCT"]
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

    Dia_chi_Man_hinh = "/qlct/xem_danh_sach_tivi"
    Chuoi_tra_cuu = ""
    if request.method == "POST":  # if request.form.get("Th_Ma_so")
        Ma_so = request.form.get("Th_Ma_so")
        if Ma_so == "DANH_SACH":
            Dia_chi_Man_hinh = "/qlct/xem_danh_sach_tivi"
        elif Ma_so == "SO_LUONG_TON":
            Dia_chi_Man_hinh = "/qlct/thong-ke"
        elif Ma_so == "DOANH_THU_TIVI":
            Dia_chi_Man_hinh = "/qlct/doanh-thu-theo-tivi"
        elif Ma_so == "DOANH_THU_NHAN_VIEN":
            Dia_chi_Man_hinh = ""
        elif Ma_so == "TRA_CUU":
            Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
            if Chuoi_tra_cuu == "":
                Dia_chi_Man_hinh = "/qlbh/xem_danh_sach_tivi"
            else:
                Dia_chi_Man_hinh = "/qlbh/tra_cuu/" + Chuoi_tra_cuu

    return render_template('Quan_ly_Cong_ty/MH_Chinh.html',
                           Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien,
                           Dia_chi_MH=Dia_chi_Man_hinh,
                           Chuoi_Tra_cuu=Chuoi_tra_cuu)



@app.route("/qlct/thong-ke", methods=["GET", "POST"])
def QLCT_Thong_Ke():
    #Lấy danh sách nhóm
    Cong_ty = Doc_Cong_ty()

    Danh_sach_Nhom_TiVi = Cong_ty['Danh_sach_Nhom_Tivi']

    #Lấy danh sách Tivi
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    #Thống kê
    Danh_sach_Thong_ke = Thong_ke_So_luong_Ton(Danh_sach_Nhom_TiVi, Danh_sach_Tivi)

    #Xuất kết quả
    Chuoi_HTML_Thong_Ke_Tivi = Tao_Chuoi_HTML_Thong_ke_SL_Ton_Tivi(Danh_sach_Thong_ke)

    return render_template("Quan_ly_Cong_ty/MH_Xem_SL_Ton.html",
                           Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_Ke_Tivi)



@app.route("/qlct/tra_cuu/<string:Chuoi_tim_kiem>", methods= ["GET", "POST"])
def QLCT_tim_kiem(Chuoi_tim_kiem):
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_xem = Tra_cuu_Tivi(Chuoi_tim_kiem, Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_xem)

    return render_template('Quan_ly_Cong_ty/MH_Xem_Danh_sach_Tivi.html',
                           Chuoi_HTML_Danh_sach_Tivi= Chuoi_HTML_Danh_sach_Tivi)



@app.route("/qlct/doanh-thu-theo-tivi", methods=["GET", "POST"])
def QLCT_doanh_thu_theo_tivi():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    Ngay_hien_hanh = datetime.now().strftime("%d-%m-%Y")
    Danh_sach_Tivi_nhap = Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi,Ngay_hien_hanh )
    Danh_sach_Thong_ke = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_nhap, Ngay_hien_hanh)

    Chuoi_HTML_Thong_ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Doanh_thu_Tivi(Danh_sach_Thong_ke)

    return render_template("Quan_ly_Cong_ty/MH_Xem_Doanh_thu_Tivi.html",
                           Chuoi_HTML_Thong_ke_Tivi = Chuoi_HTML_Thong_ke_Tivi)

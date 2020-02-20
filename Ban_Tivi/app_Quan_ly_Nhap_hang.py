from flask import render_template, request, session, redirect, url_for
from Ban_Tivi import app
from Ban_Tivi.Thu_vien.Quan_ly_Nhap_hang.Xu_ly_3L import *
from datetime import datetime



@app.route("/qlnh", methods=["GET", "POST"])
def QLNH_Chinh():
    # Kiểm tra nếu chưa đăng nhập thì sẽ chuyển hướng về trang đăng nhập
    if session.get('session_QLNH') is None:
        return redirect(url_for("QLNH_Dang_nhap"))

    # Lấy thông tin nhân viên đã đăng nhập để hiển thị ra màn hình
    Nhan_vien_Dang_nhap = session["session_QLNH"]
    Chuoi_HTML_Nhan_vien = Tao_chuoi_HTML_Nhan_vien(Nhan_vien_Dang_nhap)

        # Xử lí màn hình
    Dia_chi_Man_hinh = "/qlnh/xem_danh_sach_tivi"
    Chuoi_tra_cuu = ""
    if request.method == "POST": # if request.form.get("Th_Ma_so")
        Ma_so = request.form.get("Th_Ma_so")
        if Ma_so == "DANH_SACH":
            Dia_chi_Man_hinh = "/qlnh/xem_danh_sach_tivi"
        elif Ma_so == "SO_LUONG_TON":
            Dia_chi_Man_hinh = "/qlnh/thong-ke"
        elif Ma_so == "TRA_CUU":
            Chuoi_tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
            if Chuoi_tra_cuu == "":
                Dia_chi_Man_hinh = "/qlnh/xem_danh_sach_tivi"
            else:
                Dia_chi_Man_hinh = "/qlnh/tra_cuu/" + Chuoi_tra_cuu

    return render_template('Quan_ly_Nhap_hang/MH_Chinh.html',
                           Chuoi_HTML_Nhan_vien=Chuoi_HTML_Nhan_vien,
                           Dia_chi_MH=Dia_chi_Man_hinh,
                           Chuoi_Tra_cuu=Chuoi_tra_cuu)



@app.route('/qlnh/dang-nhap', methods=['GET','POST'])
def QLNH_Dang_nhap():
    # Kiểm tra nếu đã đăng nhập thì sẽ chuyển hướng về trang chính
    if session.get('session_QLNH') is not None:
        return redirect(url_for("QLNH_Chinh"))

    Ten_dang_nhap = ""
    Mat_khau = ""
    Thong_bao = ""
    if request.form.get("Th_Ten_dang_nhap"):
        Ten_dang_nhap = request.form.get("Th_Ten_dang_nhap")
        Mat_khau = request.form.get("Th_Mat_khau")

        # Lấy thông tin từ file cong ty.json
        Cong_ty = Doc_Cong_ty()
        Nhan_vien = Dang_nhap_Nhan_vien(Cong_ty["Danh_sach_Quan_ly_Nhap_hang"], Ten_dang_nhap, Mat_khau)
        Hop_le = Nhan_vien is not None
        if Hop_le:
            session["session_QLNH"] = Nhan_vien  # thực hiện gán giá trị
            return redirect(url_for("QLNH_Chinh"))
        else:
            Thong_bao = "Đăng nhập không hợp lệ."

    return render_template('Quan_ly_Nhap_hang/MH_Dang_nhap.html',
                           Ten_dang_nhap=Ten_dang_nhap,
                           Mat_khau=Mat_khau,
                           Chuoi_Thong_bao=Thong_bao)



@app.route("/qlnh/thong-ke", methods=["GET", "POST"])
def QLNH_Thong_Ke():
    #Lấy danh sách nhóm
    Cong_ty = Doc_Cong_ty()

    Danh_sach_Nhom_TiVi = Cong_ty['Danh_sach_Nhom_Tivi']

    #Lấy danh sách Tivi
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()

    #Thống kê
    Danh_sach_Thong_ke = Thong_ke_So_luong_Ton(Danh_sach_Nhom_TiVi, Danh_sach_Tivi)

    #Xuất kết quả
    Chuoi_HTML_Thong_Ke_Tivi = Tao_Chuoi_HTML_Thong_ke_Tivi(Danh_sach_Thong_ke)

    return render_template("Quan_ly_Nhap_hang/MH_Xem_SL_Ton.html",
                           Chuoi_HTML_Thong_ke_Tivi=Chuoi_HTML_Thong_Ke_Tivi)



@app.route('/qlnh/cap-nhat/<string:Ma_so>/',methods=['GET','POST'])
def QLNH_Cap_Nhat(Ma_so):
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Tivi_Chon = Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so)
    Don_gia_nhap = Tivi_Chon['Don_gia_Nhap']
    Thong_bao=''
    if Tivi_Chon is not None:
        if request.form.get('Th_Don_gia_Nhap'):
            Don_gia_nhap = int(request.form.get('Th_Don_gia_Nhap'))
            Tivi_Chon['Don_gia_Nhap'] = Don_gia_nhap #cập nhật phần tử trong dict
            Ghi_Tivi(Tivi_Chon)
            Thong_bao= "Cập nhật thành công đơn giá mới là: " + str(Don_gia_nhap)


    Chuoi_HTML_Tivi = Tao_Chuoi_HTML_Tivi(Tivi_Chon, Thong_bao, Don_gia_nhap)

    return render_template('Quan_ly_Nhap_hang/MH_Cap_nhap_Tivi.html',
                           Chuoi_HTML_Tivi=Chuoi_HTML_Tivi)


@app.route("/qlnh/xem_danh_sach_tivi", methods=["GET", "POST"])
def QLNH_Ds_tivi():
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_Xem = Danh_sach_Tivi

    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_Xem)

    return render_template('Quan_ly_Nhap_hang/MH_Xem_Danh_sach_Tivi.html',
                            Chuoi_HTML_Danh_sach_Tivi=Chuoi_HTML_Danh_sach_Tivi)


@app.route("/qlnh/dang_xuat", methods=["GET", "POST"])
def QLNH_Dang_xuat():
    session.pop("session_QLNH", None)
    return redirect(url_for("QLNH_Dang_nhap"))



@app.route("/qlnh/tra_cuu/<string:Chuoi_tim_kiem>", methods= ["GET", "POST"])
def QLNH_tim_kiem(Chuoi_tim_kiem):
    Danh_sach_Tivi = Doc_Danh_sach_Tivi()
    Danh_sach_Tivi_xem = Tra_cuu_Tivi(Chuoi_tim_kiem, Danh_sach_Tivi)
    Chuoi_HTML_Danh_sach_Tivi = Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi_xem)

    return render_template('Quan_ly_Nhap_hang/MH_Xem_Danh_sach_Tivi.html',
                           Chuoi_HTML_Danh_sach_Tivi= Chuoi_HTML_Danh_sach_Tivi)





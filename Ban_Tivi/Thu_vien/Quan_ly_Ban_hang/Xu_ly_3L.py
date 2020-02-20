from flask import   Markup, url_for
import json
import os
from datetime import datetime
Thu_muc_Du_lieu ="Ban_Tivi/Du_lieu"
Thu_muc_Tivi = "Ban_Tivi/Du_lieu/Tivi/"
Thu_muc_Cong_ty= "Ban_Tivi/Du_lieu/Cong_ty/"
# Xử lý Lưu trữ 
def Doc_Danh_sach_Tivi():
    Danh_sach = []
    for Ten_Tap_tin in os.listdir(Thu_muc_Tivi):
        Duong_dan = Thu_muc_Tivi + Ten_Tap_tin  
        data_file = open(Duong_dan, encoding='utf-8')    
        Tivi = json.load(data_file)    
        data_file.close()
        Danh_sach.append(Tivi)   
    return Danh_sach

def Doc_Cong_ty():
    Duong_dan = Thu_muc_Cong_ty + "Cong_ty.json"  
    data_file = open(Duong_dan, encoding='utf-8')    
    Cong_ty = json.load(data_file)    
    data_file.close()
    return Cong_ty    

def Ghi_Tivi(Tivi):    
    Ten_tap_tin = Thu_muc_Tivi + Tivi["Ma_so"] +".json"
    f = open(Ten_tap_tin , 'w', encoding='utf-8')
    json.dump(Tivi, f, indent=4, ensure_ascii=False )
    f.close()
    print("Đã ghi Tivi!!!")    
    return

# Xử lý Nghiệp vụ 
def Dang_nhap_Nhan_vien(Danh_sach_Nhan_vien, Ten_dang_nhap, Mat_khau):
    Danh_sach = list(filter(
        lambda Nhan_vien: Nhan_vien['Ten_dang_nhap'] == Ten_dang_nhap and Nhan_vien["Mat_khau"] == Mat_khau
        , Danh_sach_Nhan_vien))
    nhan_vien = Danh_sach[0] if len(Danh_sach)==1 else None
    
    return nhan_vien

def Tra_cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi):
    Danh_sach=list(filter(
        lambda Tivi: Chuoi_Tra_cuu.upper() in Tivi["Ten"].upper() or Chuoi_Tra_cuu.upper() in Tivi["Nhom_Tivi"]["Ten"].upper() , Danh_sach_Tivi))
    return Danh_sach

def Lay_chi_tiet_Tivi(Danh_sach_Tivi, Ma_so):
    Danh_sach  = list(filter(
        lambda Tivi: Tivi["Ma_so"] == Ma_so, Danh_sach_Tivi
    ))
    Tivi = Danh_sach[0] if len(Danh_sach)==1 else None

    return Tivi

def Thong_ke_So_luong_Ton(Danh_sach_Nhom_Tivi, Danh_sach_Tivi):    
    Danh_sach = []
    for Nhom_Tivi in Danh_sach_Nhom_Tivi:
        Danh_sach_Tivi_Theo_nhom = list(filter(lambda Tivi: Tivi["Nhom_Tivi"]["Ma_so"] == Nhom_Tivi["Ma_so"], Danh_sach_Tivi))   
        Tong_SL_Ton = sum(map(lambda Tivi: int(Tivi["So_luong_Ton"]), Danh_sach_Tivi_Theo_nhom))
        Danh_sach.append({"Ma_so":Nhom_Tivi["Ma_so"], "Ten":Nhom_Tivi["Ten"], "So_luong_Ton":Tong_SL_Ton})
    return Danh_sach

def Tong_ket_1_Tivi_Theo_Ngay(Tivi, Ngay):    
    Tong_So_luong = 0
    Tong_Tien = 0
    Don_gia = 0
    for Phieu_ban in Tivi["Danh_sach_Phieu_Ban"]:
           if Phieu_ban["Ngay"] == Ngay: 
                Tong_So_luong += int(Phieu_ban["So_luong"])
                Tong_Tien += int(Phieu_ban["Tien"])
                Don_gia = Phieu_ban["Don_gia"]
    Thong_tin = {"Ten":Tivi["Ten"], "So_luong": Tong_So_luong, "Don_gia": Don_gia, "Tien": Tong_Tien}
    return Thong_tin

def Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi, Ngay):
    Danh_sach = []
    for Tivi in Danh_sach_Tivi:
        Thong_tin = Tong_ket_1_Tivi_Theo_Ngay(Tivi, Ngay)
        if Thong_tin["So_luong"] !=0:        
            Danh_sach.append(Thong_tin)
    return Danh_sach

def Danh_sach_Tivi_Da_ban_Theo_ngay(Danh_sach_Tivi, Ngay):
    Danh_sach = []
    for Tivi in Danh_sach_Tivi:
        for Phieu_ban in Tivi["Danh_sach_Phieu_Ban"]:
           if Phieu_ban["Ngay"] == Ngay:               
               Danh_sach.append(Tivi) 
               break
        Danh_sach
    return Danh_sach

def Doc_Danh_sach_Tivi_theo_Nhan_vien(Danh_sach_Tivi, Nhan_vien):
    Danh_sach = []
    for Loai_Tivi in Nhan_vien["Danh_sach_Nhom_Tivi"]:
        for Tivi in Danh_sach_Tivi:
            if Loai_Tivi["Ma_so"] == Tivi["Nhom_Tivi"]["Ma_so"]:
                Danh_sach.append(Tivi)
    return Danh_sach

# Xử lý Thể hiện
def Tao_chuoi_HTML_Nhan_vien(Nhan_vien):
    Chuoi_HTML_Nhan_vien = '<div class="row" >'
    Chuoi_Hinh = '<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Nhan_vien["Ma_so"]+'.png') + '" />'
    Chuoi_Thong_tin = '<div class="btn" style="text-align:left"> Xin chào Quản lý Bán hàng ' + \
                 Nhan_vien["Ho_ten"] + "</div>"
    
    Chuoi_HTML_Nhan_vien += Chuoi_Hinh + Chuoi_Thong_tin 
    
    return Markup(Chuoi_HTML_Nhan_vien)  

def Tao_Chuoi_HTML_Tivi(Tivi, Thong_bao, Don_gia_Ban):
    Chuoi_Hinh='<img  style="width:300px" src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
    Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
    Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
    Chuoi_SL_Ton = "Số lượng tồn:" + str(Tivi["So_luong_Ton"]) + "<br/>"
    Chuoi_Don_gia_Ban="Đơn giá Bán hiện hành {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".") 
    Chuoi_Ngay = "Ngày: "  + datetime.now().strftime('%d-%m-%Y')
    Chuoi_HTML_Tivi = '''
        <div class="container">
          <div class="card" align="center">
            <h4 class="card-title">Cập nhật Đơn giá bán</h4>
            <h6 class="card-title">'''+ Chuoi_Ngay+'''</h6>
            ''' + Chuoi_Hinh + '''
            <div class="card-body">
              <h4 class="card-title">'''+ Tivi["Ten"]+'''</h4>
              <p class="card-text">'''+ Chuoi_Don_gia_Ban +'''<br/>'''+ Chuoi_SL_Ton +''' </p>
    
              <form method="POST">
                <div class="container-fluid">
                  <div class="alert" style="height:30px">
                    Đơn giá Bán mới <input name="Th_Don_gia_Ban" type="number" required spellcheck="false" 
                    autocomplete="off" value="'''+ str(Don_gia_Ban) + '''"
                    />
                  </div>
                  <div class="alert" style="height:40px">
                    <button class="btn btn-danger" type="submit">Đồng ý</button>
                  </div>
                </div>
                <div>'''+ Thong_bao +'''</div>
              </form>
            </div>
          </div>
        </div>
        '''
    return Markup(Chuoi_HTML_Tivi)    

def Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi):   
    Chuoi_HTML_Danh_sach = '<div class="row" >'
    for Tivi in Danh_sach_Tivi:        
        Chuoi_Don_gia_Nhap="Đơn giá Bán {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".")   
        Chuoi_Hinh='<img  style="width:60px;height:60px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'        
        Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
        Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
        Chuoi_SL_Ton = "SL Tồn:" + str(Tivi["So_luong_Ton"]) + "<br/>"
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 Tivi["Ten"] + "<br />" + Chuoi_Don_gia_Nhap + "<br/>" + \
                 Chuoi_SL_Ton + \
                 '''<a href="/qlbh/cap-nhat/''' + Tivi["Ma_so"] +'''/">Cập nhật</a>'''+ '</div>'
        Chuoi_HTML ='<div class="col-md-4" >' +  \
                Chuoi_Hinh + Chuoi_Thong_tin + '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  
 
def Tao_Chuoi_HTML_Thong_ke_SL_Ton_Tivi(Danh_sach_Thong_ke):
    Ngay = "Ngày: " + datetime.now().strftime('%d-%m-%Y')     
    
    Chuoi_HTML_Danh_sach = '<div class="container"><h3>Thống kê Số lượng tồn</h3><br/><h5>' + Ngay +'</h5></div>'
    Chuoi_HTML_Danh_sach += '<div class="row" >'
    
    stt = 1
    header = '''
        <div class="dong">
        <div class="cot">STT</div>
        <div class="cot">Nhóm Tivi</div>
        <div class="cot">Số lượng Tồn</div>       
        </div>
        '''  
    Chuoi_HTML_Danh_sach +=header

    for Nhom_Tivi in Danh_sach_Thong_ke:
        Chuoi_HTML = '''
        <div class="dong">
        <div class="cot">'''+ str(stt) +'''</div>
        <div class="cot">'''+ Nhom_Tivi['Ten']+'''</div>
        <div class="cot">'''+ str(Nhom_Tivi['So_luong_Ton']) +'''</div>        
        </div>
        '''     
        stt += 1        
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  

def Tao_Chuoi_HTML_Thong_ke_Doanh_thu_Tivi(Danh_sach_Thong_ke):
    
    Ngay = "Ngày: " + datetime.now().strftime('%d-%m-%Y') 
    Chuoi_Tong_Doanh_Thu = "...Tổng tiền: {:,}".format(sum(Tivi['Tien'] for Tivi in Danh_sach_Thong_ke)).replace(",",".") 
    
    Chuoi_HTML_Danh_sach = '<div class="container"><h3>Thống kê Doanh thu theo Tivi </h3><br/><h5>' + Ngay + Chuoi_Tong_Doanh_Thu + '</h5></div>'
    Chuoi_HTML_Danh_sach += '<div class="row" >'
    
    stt = 1
    header = '''
        <div class="dong">
        <div class="cot">STT</div>
        <div class="cot">Tivi</div>
        <div class="cot">Số lượng</div>
        <div class="cot">Đơn giá</div>
        <div class="cot">Tiền</div>
        </div>
        '''  
    Chuoi_HTML_Danh_sach +=header

    for Tivi in Danh_sach_Thong_ke:
        Chuoi_HTML = '''
        <div class="dong">
        <div class="cot">'''+ str(stt) +'''</div>
        <div class="cot">'''+ Tivi['Ten']+'''</div>
        <div class="cot">'''+ str(Tivi['So_luong']) +'''</div>
        <div class="cot">'''+ "{:,}".format(Tivi["Don_gia"]).replace(",",".") +'''</div>
        <div class="cot">'''+ "{:,}".format(Tivi["Tien"]).replace(",",".") +'''</div>
        </div>
        '''     
        stt += 1
        
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  

def Tao_Chuoi_HTML_Doanh_thu_1_Nhan_vien(Danh_sach_Tivi_Ban, Nhan_vien):    
    Danh_sach_Tivi_Theo_nhan_vien = Doc_Danh_sach_Tivi_theo_Nhan_vien(Danh_sach_Tivi_Ban, Nhan_vien)
    Ngay = datetime.now().strftime('%d-%m-%Y')
    Danh_sach_Tivi_Nhan_vien_Ban = Tong_ket_Danh_sach_Tivi(Danh_sach_Tivi_Theo_nhan_vien, Ngay)
    Chuoi_Tong_Doanh_Thu = "...Tổng tiền: {:,}".format(sum(Tivi['Tien'] for Tivi in Danh_sach_Tivi_Nhan_vien_Ban)).replace(",",".") 
    
    Chuoi_HTML = '<div class="container"><h5>Nhân viên '+ Nhan_vien["Ho_ten"]+ Chuoi_Tong_Doanh_Thu + '</h5></div>'
    Chuoi_HTML += '<div class="row" >'
    
    stt = 1
    header = '''
        <div class="dong">
        <div class="cot">STT</div>
        <div class="cot">Tivi</div>
        <div class="cot">Số lượng</div>
        <div class="cot">Đơn giá</div>
        <div class="cot">Tiền</div>
        </div>
        '''  
    Chuoi_HTML +=header

    for Tivi in Danh_sach_Tivi_Nhan_vien_Ban:
        Chuoi_HTML_Ban = '''
        <div class="dong">
        <div class="cot">'''+ str(stt) +'''</div>
        <div class="cot">'''+ Tivi['Ten']+'''</div>
        <div class="cot">'''+ str(Tivi['So_luong']) +'''</div>
        <div class="cot">'''+ "{:,}".format(Tivi["Don_gia"]).replace(",",".") +'''</div>
        <div class="cot">'''+ "{:,}".format(Tivi["Tien"]).replace(",",".") +'''</div>
        </div>
        '''     
        stt += 1
        
        Chuoi_HTML +=Chuoi_HTML_Ban 

    Chuoi_HTML+= '</div>'
    return Chuoi_HTML     

def Tao_Chuoi_HTML_Thong_ke_Doanh_thu_Nhan_vien(Danh_sach_Tivi_ban):
    Cong_ty = Doc_Cong_ty()
    Danh_sach_Nhan_vien_Ban_hang = Cong_ty["Danh_sach_Nhan_vien_Ban_hang"]
    
    Ngay = "Ngày: " + datetime.now().strftime('%d-%m-%Y') 
    
    
    Chuoi_HTML_Danh_sach = '<div class="container"><h3>Thống kê Doanh thu theo Nhân viên</h3><br/><h5>' + Ngay + '</h5></div>'
    Chuoi_HTML_Danh_sach += '<div class="row" >'
    
    for Nhan_vien in Danh_sach_Nhan_vien_Ban_hang:
        Chuoi_HTML_Danh_sach += Tao_Chuoi_HTML_Doanh_thu_1_Nhan_vien(Danh_sach_Tivi_ban, Nhan_vien)
    
    Chuoi_HTML_Danh_sach += '</div>'               
 
    return Markup(Chuoi_HTML_Danh_sach)  


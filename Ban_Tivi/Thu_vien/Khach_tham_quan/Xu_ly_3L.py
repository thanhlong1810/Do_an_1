from flask import Markup, url_for
import json
import os


Thu_muc_Du_lieu ="Ban_Tivi/Du_lieu"
Thu_muc_Tivi = "Ban_Tivi/Du_lieu/Tivi/"


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

# Xử lý Nghiệp vụ 
def Tra_cuu_Tivi(Chuoi_Tra_cuu, Danh_sach_Tivi):
    Danh_sach=list(filter(
        lambda Tivi: Chuoi_Tra_cuu.upper() in Tivi["Ten"].upper(), Danh_sach_Tivi))
    return Danh_sach

    return Danh_sach

# Xử lý Thể hiện
def Tao_Chuoi_HTML_Danh_sach_Tivi(Danh_sach_Tivi):
    Chuoi_HTML_Danh_sach = '<div class="row" >'
    for Tivi in Danh_sach_Tivi:
        Chuoi_Don_gia_Ban="Đơn giá Bán {:,}".format(Tivi["Don_gia_Ban"]).replace(",",".")    
        Chuoi_Hinh_nho='<img  style="width:60px;height:60px" src="'+ url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
        Chuoi_Hinh_to='<img  style="width:300px"  src="'+ \
                 url_for('static', filename = Tivi["Ma_so"]+'.png') + '" />'
        Chuoi_Loai_Tivi = "Thuộc loại: " + Tivi["Nhom_Tivi"]["Ten"] + "<br/>"
        Chuoi_Ky_hieu = "Ký hiệu:" + Tivi["Ky_hieu"] + "<br/>"
        Chuoi_Thong_tin='<div class="btn" style="text-align:left">' + \
                 Tivi["Ten"] + "<br />" + Chuoi_Don_gia_Ban + "</div>"
        """
                 + "<br/>" + \
                 '''<a data-toggle="modal" href="#myModal">Xem chi tiết</a>'''+ '</div>'

        # hiển thị thông tin chi tiết của tivi trong modal khi người dùng click vào link xem thêm phía trên
        Chuoi_Xem_tivi = '''<div class="container">       
        <div class="modal fade" id="myModal">
            <div class="modal-dialog">
            <div class="modal-content">      
                <div class="modal-header">
                <h4 class="modal-title">''' + Tivi["Ten"] + '''</h4>                
                <button type="button" class="close" data-dismiss="modal">&times;</button>
                </div>                
               
                <div class="modal-body" align="center"> 
                ''' + Chuoi_Ky_hieu + Chuoi_Loai_Tivi + Chuoi_Hinh_to + '''<br/>''' + Chuoi_Don_gia_Ban + '''<br/>  
                </div>                
                
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Đóng</button>
                </div>
                
            </div>
            </div>
        </div>        
        </div>
        '''
        """
        Chuoi_HTML ='<div class="col-md-4" >' +  \
                Chuoi_Hinh_nho + Chuoi_Thong_tin + '</div>' 
        Chuoi_HTML_Danh_sach +=Chuoi_HTML 

    Chuoi_HTML_Danh_sach += '</div>'               
    return Markup(Chuoi_HTML_Danh_sach)  
 
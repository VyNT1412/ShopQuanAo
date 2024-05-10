import hashlib

from app import app, db
from app.models import  User, KhachHang, NhanVien, Hang, HoaDon, CongTySX, ChatLieu, CTHoaDon, BinhLuan, LoaiHang
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract

def get_user_by_id(id):
    return User.query.get(id)

def get_san_pham_by_id(id):
    return Hang.query.get(id)
def get_all_hang():
    return Hang.query.all()

def get_all_chat_lieu():
    return ChatLieu.query.all()



def get_all_cong_ty():
    return CongTySX.query.all()



def get_all_KH():
    return KhachHang.query.all()

def get_all_HoaDon():
    return HoaDon.query.all()

def get_all_loai_hang():
    return LoaiHang.query.all()

def get_CTHoaDon_by_id_HoaDon(id_hoadon):
    return CTHoaDon.query.get(id_hoadon)

def get_ten_chat_lieu(id):
    return ChatLieu.query.get(id)

def load_sanPham( kw=None, from_price=None,to_price=None, id_loaihang=None, page=None):
     hangs=Hang.query.filter(Hang.so_luong.__ge__(0))

     if id_loaihang:
         hangs = hangs.filter(Hang.loaihang_id.__eq__(id_loaihang))

     if kw:
         hangs = hangs.filter(Hang.ten_hang.like(f'%{kw}%'))

     if from_price:
         hangs = hangs.filter(Hang.don_gia_ban.__ge__(from_price))

     if to_price:
         hangs = hangs.filter(Hang.don_gia_ban.__le__(to_price))

     if page is not None:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return hangs.slice(start, start + page_size).all()
     return hangs.all()


def count_san_pham_by_id_loai_hang():
    danhmuc = LoaiHang.query.all()

    danhmuc_counts = []
    for dm in danhmuc:
        # Đếm số lượng sản phẩm thuộc loại hàng hiện tại
        sanpham_count = Hang.query.filter_by(loaihang_id=dm.id).count()

        # Lưu thông tin loại hàng và số lượng sản phẩm vào danh sách
        danhmuc_counts.append({
            'ten_hang': dm.ten_hang,
            'sanpham_count': sanpham_count
        })

    return danhmuc_counts

def count_san_pham():
    return Hang.query.filter(Hang.so_luong > 0).count()

def check_existing_user_kh(username=None, sdt = None):
    if username:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return True

    if sdt:
        existing_sdt = KhachHang.query.filter_by(so_dien_thoai=sdt).first()
        if existing_sdt:
            return True
    return False

def add_user(username, password):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    user = User(username=username.strip(), user_password=password)
    db.session.add(user)
    db.session.commit()

def add_user_kh(id_user, hoten_kh, dia_chi, sdt):
    kh = KhachHang(id_user=id_user, ten_khachhang = hoten_kh, dia_chi=dia_chi, so_dien_thoai = sdt)
    db.session.add(kh)
    db.session.commit()

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.id  # Trả về id của user nếu tìm thấy
    else:
        return None  # Trả về None nếu không tìm thấy user

def check_login(username, password):
    if username and password:
        password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
        return User.query.filter(User.username.__eq__(username.strip()), User.user_password.__eq__(password)).first()

def get_khach_hang_by_id_user(id_user):
    return KhachHang.query.filter(KhachHang.id_user.__eq__(id_user)).first()

def update_tt_khach_hang( id_user, tenkh, diachi, sdt):
    khachhang = get_khach_hang_by_id_user(id_user)
    if khachhang:
        khachhang.ten_khachhang = tenkh
        khachhang.dia_chi = diachi
        khachhang.so_dien_thoai = sdt

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        return True
    else:
        return False

def them_hoa_don(cart):
    if cart:
        giohang = count_cart(cart)
        kh = get_khach_hang_by_id_user(current_user.id)

        total_quantity = giohang["total_quantity"]
        total_amount = giohang["total_amount"]

        hoa_don = HoaDon(id_nhanvien=1, id_khach_hang=kh.id, tongtien=total_amount)
        db.session.add(hoa_don)
        db.session.commit()

        for c in cart.values():
            thanhtien = float(c['quantity']) * float(c['price'])  # Tính thành tiền
            d = CTHoaDon(id_hoadon=hoa_don.id, id_mahang=c['id'], so_luong_hang=c['quantity'], gia=c['price'],
                         thanhtien=thanhtien)
            db.session.add(d)

        db.session.commit()

def doi_mat_khau(id_user,mk_cu, mk_moi):

    if mk_cu and mk_moi:
        u = get_user_by_id(id_user)
        if u:
            mk_cu = hashlib.md5(mk_cu.strip().encode('utf-8')).hexdigest()
            if u.user_password.__eq__(mk_cu):
                mk_moi = hashlib.md5(mk_moi.strip().encode('utf-8')).hexdigest()
                u.user_password = mk_moi
                # Lưu thay đổi vào cơ sở dữ liệu
                db.session.commit()
                return True
            else:
                return False

def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            try:
                quantity = int(c['quantity'])  # Chuyển đổi quantity sang kiểu số nguyên
                price = float(c['price'])  # Chuyển đổi price sang kiểu số thực
                total_quantity += quantity
                total_amount += quantity * price
            except (ValueError, TypeError):
                # Xử lý ngoại lệ nếu không thể chuyển đổi sang số
                continue

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }
# THONG KE

def thong_ke_danh_muc():
    # return LoaiHang.query.join(Hang, Hang.loaihang_id.__eq__(LoaiHang.id)).add_columns(func.count(Hang.id)).group_by(LoaiHang.id, LoaiHang.ten_hang).all()
    return (db.session.query(LoaiHang.id, LoaiHang.ten_hang, func.count(Hang.id))
            .outerjoin(Hang, LoaiHang.id == Hang.loaihang_id)
            .group_by(LoaiHang.id, LoaiHang.ten_hang)
            .all())


def thong_ke_san_pham(kw=None, from_date=None, to_date=None):
    sp = (db.session.query(
            Hang.id,
            Hang.ten_hang,
            func.sum(CTHoaDon.thanhtien)
        )
        .outerjoin(CTHoaDon, CTHoaDon.id_mahang == Hang.id).outerjoin(HoaDon,HoaDon.id == CTHoaDon.id_hoadon)
        .group_by(Hang.id, Hang.ten_hang)
    )
    if kw:
        sp = sp.filter(Hang.ten_hang.like(f'%{kw}%'))
    if from_date:
        sp = sp.filter(HoaDon.ngay_ban.__ge__(from_date))
    if to_date:
        sp = sp.filter(HoaDon.ngay_ban.__le__(to_date))
    return sp.all()

def thong_ke_san_pham_theo_thang(year):
    return (db.session.query(extract('month', HoaDon.ngay_ban), func.sum(CTHoaDon.thanhtien))
            .outerjoin(CTHoaDon, CTHoaDon.id_hoadon == HoaDon.id)
            .filter(extract('year', HoaDon.ngay_ban) == year)
            # .order_by(extract('month', HoaDon.ngay_ban))  # Sắp xếp trước khi nhóm
            .group_by(extract('month', HoaDon.ngay_ban))
            .all())

def them_binh_luan(noi_dung, sanpham_id):
    c = BinhLuan(noi_dung=noi_dung, khachhang_id=current_user.id, sanpham_id=sanpham_id)
    db.session.add(c)
    db.session.commit()

    return c

def get_binh_luan(sp_id,page=1):
    page = int(page)
    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size
    return BinhLuan.query.filter(BinhLuan.sanpham_id.__eq__(sp_id)).order_by(-BinhLuan.id).slice(start, start + page_size).all()

def dem_binh_luan(sp_id):
    return BinhLuan.query.filter(BinhLuan.sanpham_id.__eq__(sp_id)).count()

def lay_danh_sach_don_hang_khach_hang(id_khach_hang):
    # Lấy tất cả đơn hàng của khách hàng có id là id_khach_hang
    don_hang = HoaDon.query.filter_by(id_khach_hang=id_khach_hang).all()

    # Duyệt qua từng đơn hàng và lấy thông tin chi tiết của từng đơn hàng
    for don_hang_item in don_hang:
        # Lấy chi tiết đơn hàng tương ứng với mỗi đơn hàng
        chi_tiet_don_hang = CTHoaDon.query.filter_by(id_hoadon=don_hang_item.id).all()

        # Thêm thông tin chi tiết vào mỗi đơn hàng
        don_hang_item.chi_tiet = chi_tiet_don_hang

    return don_hang



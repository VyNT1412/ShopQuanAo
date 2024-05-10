from sqlalchemy import Column, Integer, String, Double, ForeignKey, Date, Enum, DateTime
from app import db, app
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime
from flask_login import UserMixin

from sqlalchemy.orm import relationship
import enum

class Role_User(enum.Enum):
    KHACHHANG = 2
    NHANVIEN = 1


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel, UserMixin):
    __tablename__ = 'user'

    username = Column(String(20), nullable=False, unique=True)
    user_password = Column(String(255), nullable=False)
    user_role = Column(Enum(Role_User), default=Role_User.KHACHHANG)



    khachhang_rel = db.relationship('KhachHang', back_populates = "user")
    nhanvien_rel = relationship('NhanVien', back_populates='user')
    binhluan = relationship('BinhLuan', back_populates='user')
class KhachHang(BaseModel):
    __tablename__ = 'khachhang'

    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    ten_khachhang = Column(String(50), nullable=False)
    dia_chi = Column(String(255), nullable=False)
    so_dien_thoai = Column(String(10), nullable=False)

    user = relationship('User', back_populates ='khachhang_rel', lazy=True)
    hoadon_rel = relationship('HoaDon', back_populates='khachhang', lazy=True)


class NhanVien(BaseModel):
    __tablename__ = 'nhanvien'

    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    ten_nhanvien = Column(String(50), nullable=False)
    dia_chi = Column(String(50), nullable=False)
    so_dien_thoai = Column(String(10), nullable=False)
    ngay_sinh = Column(Date)
    gioi_tinh = Column(String(5), nullable=False)

    user = relationship('User', back_populates ='nhanvien_rel', lazy=True)
    hoadon = relationship('HoaDon', back_populates='nhanvien', lazy=True)


class ChatLieu(BaseModel):
    __tablename__ = 'chatlieu'

    ten_chatlieu = Column(String(255), nullable=False)

    hangs = db.relationship('Hang', back_populates = "chatlieu_rel")

    def __str__(self):
        return self.ten_chatlieu

class CongTySX(BaseModel):
    __tablename__='congtysanxuat'

    ten_cong_ty = Column(String(255), nullable=False)
    dia_chi = Column(String(255), nullable=False)
    sdt = Column(String(10), nullable=False)

    def __str__(self):
        return self.ten_cong_ty
    hangs = db.relationship('Hang', back_populates = "congtysx_rel")


class LoaiHang(BaseModel):
    __tablename__ = 'loaihang'

    ten_hang = Column(String(100), nullable=False)
    def __str__(self):
        return self.ten_hang
    # Đặt tên backref khác ở đây, ví dụ 'hang_loaihang'

    hangs = db.relationship('Hang', back_populates = "loaihang_rel")


class Hang(BaseModel):
    __tablename__ = 'hang'

    ten_hang = Column(String(100), nullable=False)
    chatlieu_id = Column(Integer, ForeignKey('chatlieu.id'), nullable=False)
    loaihang_id = Column(Integer, ForeignKey('loaihang.id'), nullable=False)
    id_cty_sx = Column(Integer, ForeignKey('congtysanxuat.id'), nullable=False)
    so_luong = Column(Integer, nullable=False)
    don_gia_nhap = Column(Double, nullable=False)
    don_gia_ban = Column(Double, nullable=False)
    anh = Column(String(255))
    ghichu = Column(String(100))

    chatlieu_rel = db.relationship('ChatLieu', back_populates = "hangs")
    loaihang_rel = relationship('LoaiHang', back_populates='hangs')
    congtysx_rel = relationship('CongTySX', back_populates='hangs')
    cthoadon_rel = relationship('CTHoaDon', back_populates='hangs')
    comment_rel = relationship('BinhLuan', back_populates='sanpham')



class HoaDon(BaseModel):
    __tablename__ = 'hoadon'

    id_nhanvien = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    ngay_ban = Column(DateTime, default=datetime.now())
    id_khach_hang = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    tongtien = Column(Double, nullable=False)

    cthoadon = relationship('CTHoaDon', back_populates='hoadon_rel', lazy=True)
    nhanvien = relationship('NhanVien', back_populates='hoadon', lazy=True)
    khachhang = relationship('KhachHang', back_populates='hoadon_rel', lazy=True)

class CTHoaDon(BaseModel):
    __tablename__ = 'chitiethoadon'

    id_hoadon = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    id_mahang = Column(Integer, ForeignKey(Hang.id), nullable=False)
    so_luong_hang = Column(Integer, nullable=False)
    gia = Column(Double, nullable=False)
    thanhtien = Column(Double, nullable=False)

    hangs = relationship('Hang', back_populates='cthoadon_rel')
    hoadon_rel = relationship('HoaDon', back_populates='cthoadon')

class BinhLuan(BaseModel):
    __tablename__ = 'binhluan'
    noi_dung = Column(String(255), nullable=False)
    sanpham_id = Column(Integer, ForeignKey(Hang.id), nullable=False)
    khachhang_id = Column(Integer, ForeignKey(User.id), nullable=False)
    thoi_gian_binh_luan = Column(DateTime, default=datetime.now())

    sanpham = relationship('Hang', back_populates='comment_rel')
    user = relationship('User', back_populates='binhluan')

    def __str__(self):
        return self.noi_dung
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
    #LOAIHANG

        # loaihang1=LoaiHang(ten_hang='quan')
        # loaihang2=LoaiHang(ten_hang='ao')
        # loaihang3=LoaiHang(ten_hang='bop')
        # db.session.add_all([loaihang1, loaihang2, loaihang3])
        # db.session.commit()
    # # USER
    #     u1 = User(username='vanb123', user_password=str(hashlib.md5('Password@123'.encode('utf-8')).hexdigest()),
    #           user_role=Role_User.KHACHHANG)
    #     u2 = User(username='anhhung234', user_password=str(hashlib.md5('Password@123'.encode('utf-8')).hexdigest()),
    #           user_role=Role_User.KHACHHANG)
    #     u3 = User(username='shopee567', user_password=str(hashlib.md5('Password@123'.encode('utf-8')).hexdigest()),
    #           user_role=Role_User.KHACHHANG)
    #     u4 = User(username='love234', user_password=str(hashlib.md5('Password@123'.encode('utf-8')).hexdigest()),
    #           user_role=Role_User.KHACHHANG)
    #     u5 = User(username='nhaviencute', user_password=str(hashlib.md5('Password@123'.encode('utf-8')).hexdigest()),
    #          user_role=Role_User.NHANVIEN)
    #
    #     db.session.add_all([u1, u2, u3, u4, u5])
    #     db.session.commit()
    # USER_KH
    #     kh1 = KhachHang(id_user=1, ten_khachhang='Nguyen Van Bich',
    #                  dia_chi='455 duong Le Van Luong, phuong Tan Phong, Quan 7, Tp HCM', so_dien_thoai='0913674451')
    # #
    #     kh2 = KhachHang(id_user=2, ten_khachhang='Tran Van B',
    #                  dia_chi='46 duong 3/2, phuong 7, Quan Tan Binh, Tp HCM', so_dien_thoai='0872342699')
    # #
    #     kh3 = KhachHang(id_user=3, ten_khachhang='Quach Thi Bich Thu',
    #                  dia_chi='66 duong 27, phuong Tan Phong, Quan 7, Tp HCM', so_dien_thoai='0893467551')
    # #
    #     kh4 = KhachHang(id_user=4, ten_khachhang='Nguyen Tran Hung',
    #                  dia_chi='343 duong Duong Ba Trac, phuong A, Quan 8, Tp HCM', so_dien_thoai='0982351179')
    # #
    #     db.session.add_all([kh1, kh2, kh3, kh4])
    #     db.session.commit()
     # USER_NHANVIEN
     #
        # nv1 = NhanVien(id_user=5, ten_nhanvien='Nguyen Thao Vy', dia_chi='79/20 duong so 2, quan Go Vap, Tp HCM',
        #            so_dien_thoai='0912524422', ngay_sinh=date(2002, 10, 4), gioi_tinh='Nu')
        # db.session.add(nv1)
        # db.session.commit()

    # ChatLieu

        # cl1 = ChatLieu(ten_chatlieu='Vai cotton')
        # cl2 = ChatLieu(ten_chatlieu='Vai kaki')
        # cl3 = ChatLieu(ten_chatlieu='Vai jean')
        # cl4 = ChatLieu(ten_chatlieu='Vai len')
        # cl5 = ChatLieu(ten_chatlieu='Vai lua')
        # cl6 = ChatLieu(ten_chatlieu='Da')
        # db.session.add_all([cl1, cl2, cl3, cl4, cl5, cl6])
        # db.session.commit()
    # # CongTySX
    #
    #     ct1 = CongTySX(ten_cong_ty='Cong A', dia_chi='32 duong X, quan A, Tp Binh Duong', sdt='0999912333')
    #     ct2 = CongTySX(ten_cong_ty='Cong X', dia_chi='123 duong T, quan BC, Tp Vung Tau', sdt='0984221234')
    #     ct3 = CongTySX(ten_cong_ty='Cong Y', dia_chi='54 duong MN, quan CV, Tp Di An', sdt='098887654')
    #     ct4 = CongTySX(ten_cong_ty='Cong Z', dia_chi='32 duong 4, quan WE, Tp Thu Dau Mot', sdt='0966111234')
    #     db.session.add_all([ct1, ct2, ct3, ct4])
    #     db.session.commit()
    # #

    #
    #  # HANG
    # #
    #     h1 = Hang(ten_hang='Quan jean nu ong rong', chatlieu=3, loaihang=1 , id_cty_sx=1, so_luong=30, don_gia_nhap=110000,
    #               don_gia_ban=155000, anh='https://ann.com.vn/wp-content/uploads/11835-clean-2ae2ab6bd35628087147.jpg',
    #               ghichu='quan nu mau xanh dam')
    #     # #
    #     h2 = Hang(ten_hang='Quan jean nam', chatlieu=3, loaihang=1, id_cty_sx=1, so_luong=30, don_gia_nhap=120000,
    #               don_gia_ban=170000,
    #               anh='https://quanaoxuongmay.com/wp-content/uploads/10193-cfdfcdd77b169d48c407-1.png',
    #               ghichu='quan jean nam xanh nhat')
    #     # #
    #     h3 = Hang(ten_hang='Ao thun nam', chatlieu=1, loaihang=2, id_cty_sx=2, so_luong=30, don_gia_nhap=100000, don_gia_ban=155000,
    #               #               anh='https://aoxuanhe.com/upload/product/axh-156/ao-thun-cotton-nam-den-cuc-chat.jpg',
    #               ghichu='ao thun nam')
    #     # #
    #     h4 = Hang(ten_hang='Ao thun nu tay ngan', chatlieu=1, loaihang=2 ,id_cty_sx=3, so_luong=30, don_gia_nhap=120000,
    #               don_gia_ban=180000,
    #               anh='https://lzd-img-global.slatic.net/g/p/e749bae79fd21519d69aba88a61373d3.jpg_550x550.jpg',
    #               ghichu='ao thun nu tay ngan')
    #     # #
    #     h5 = Hang(ten_hang='Ao len nu', chatlieu=4, loaihang=2, id_cty_sx=3, so_luong=30, don_gia_nhap=1100000, don_gia_ban=175000,
    #               anh='https://img.lazcdn.com/g/p/16b848129fafdd79166e81d6d62ee719.jpg_960x960q80.jpg_.webp',
    #               ghichu='ao len nu')
    #     # #
    #     h6 = Hang(ten_hang='Khan lua dai', chatlieu=5, loaihang=4, id_cty_sx=3, so_luong=30, don_gia_nhap=110000,
    #               don_gia_ban=220000,
    #               anh='https://jes.edu.vn/wp-content/uploads/2020/03/khan-lua-dai.jpg', ghichu='khan lua nu')
    #     # #
    #     h7 = Hang(ten_hang='Quan kaki nu', chatlieu=2, loaihang=1, id_cty_sx=4, so_luong=30, don_gia_nhap=100000,
    #               don_gia_ban=150000,
    #               anh='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTC1QHwiafFtLpfxUQfYk55fX8oDiqELUufoA&usqp=CAU',
    #               ghichu='quan kaki nu mau be')
    #     # #
    #     h8 = Hang(ten_hang='Bop da nam', chatlieu=6, loaihang=3, id_cty_sx=2, so_luong=30, don_gia_nhap=110000, don_gia_ban=160000,
    #               anh='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS02tQ_HUt-gCkp81i-Ml6rsZTznsaENuJPQM7f-yVcDylNGezOS2Auf-ueg788Xc01gl4&usqp=CAU',
    #               ghichu='da bo')
    #     # #
    #     h9 = Hang(ten_hang='Bop da nu', chatlieu=6, loaihang=3, id_cty_sx=2, so_luong=30, don_gia_nhap=120000, don_gia_ban=185000,
    #               anh='https://oneshoppi.com/wp-content/uploads/2019/12/Anh-Dai-Dien-Vi-Nu-Da-That-Vi-Da-Nu-Hang-Hieu-Cao-Cap-OSP0265-8-1.jpg',
    #               ghichu='bop nu')
    #     db.session.add_all([h1, h2, h3, h4, h5, h6, h7, h8, h9])
    #     db.session.commit()

    # #HOA DON, CT HOA DON

        # # hoadon1 = HoaDon(id_nhanvien = 1, ngay_ban = date(2024,4,30), id_khach_hang = 1, tongtien=1025000)
        # cthoadon1 = CTHoaDon(id_hoadon=1, id_mahang=1, so_luong_hang=2, gia=155000, thanhtien=310000)
        # cthoadon2 = CTHoaDon(id_hoadon=1, id_mahang=4, so_luong_hang=1, gia=180000, thanhtien=18000)
        # cthoadon3 = CTHoaDon(id_hoadon=1, id_mahang=5, so_luong_hang=2, gia=175000, thanhtien=350000)
        # cthoadon4 = CTHoaDon(id_hoadon=1, id_mahang=9, so_luong_hang=1, gia=185000,, thanhtien=185000)
        # #
        # #
        # # hoadon2 = HoaDon(id_nhanvien = 1, ngay_ban = date(2024,3,7), id_khach_hang = 2, tongtien=325000)
        # cthoadon5 = CTHoaDon(id_hoadon=2, id_mahang=2, so_luong_hang=1, gia=170000, thanhtien=170000)
        # cthoadon6 = CTHoaDon(id_hoadon=2, id_mahang=3, so_luong_hang=1, gia=155000, thanhtien=155000)
        # #
        # # hoadon3 = HoaDon(id_nhanvien=1, ngay_ban=date(2024, 2, 23), id_khach_hang=3, tongtien=370000)
        # cthoadon7 = CTHoaDon(id_hoadon=3, id_mahang=7, so_luong_hang=1, gia=150000, thanhtien=150000)
        # cthoadon8 = CTHoaDon(id_hoadon=3, id_mahang=6, so_luong_hang=1, gia=220000, thanhtien=220000)
        # #
        # # hoadon4 = HoaDon(id_nhanvien = 1, ngay_ban = date(2024,4,2), id_khach_hang = 4, tongtien=325000)
        # cthoadon9 = CTHoaDon(id_hoadon=4, id_mahang=3, so_luong_hang=2, gia=155000, thanhtien=310000)
        # cthoadon10 = CTHoaDon(id_hoadon=4, id_mahang=8, so_luong_hang=1, gia=160000, thanhtien=160000)
        #
        # #  db.session.add_all([hoadon1, hoadon2, hoadon3, hoadon4])
        # db.session.add_all(
        #     [cthoadon1, cthoadon2, cthoadon3, cthoadon4, cthoadon5, cthoadon6, cthoadon7, cthoadon8, cthoadon9,
        #      cthoadon10])
        # db.session.commit()

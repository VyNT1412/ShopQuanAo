from datetime import datetime

import self
from flask import url_for, request

from app import app, db, ultis
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import ChatLieu, Hang, CongTySX, LoaiHang, HoaDon, CTHoaDon, KhachHang, Role_User, BinhLuan
from flask import redirect
from flask_login import logout_user, current_user




class CongTySXView(ModelView):
    can_view_details = True
    column_display_pk = True
    can_export = True
    column_filters = ['ten_cong_ty']
    column_sortable_list = ['ten_cong_ty']
    column_searchable_list = ['ten_cong_ty', 'dia_chi']
    column_labels = {
        'ten_cong_ty': 'Tên công ty',
        'dia_chi': 'Địa chỉ',
        'sdt': 'Số điện thoại',
    }


class SanPhamView(ModelView):

    column_list = ['id', 'ten_hang', 'chatlieu_id', 'loaihang_id', 'id_cty_sx',
        'don_gia_nhap', 'don_gia_ban', 'anh', 'ghichu', 'so_luong'
    ]
    form_columns = ['ten_hang','chatlieu_rel','loaihang_rel', 'congtysx_rel', 'don_gia_nhap','don_gia_ban','anh', 'ghichu', 'so_luong']
    form_args = {
        'chatlieu_rel': {'label': 'Chất liệu' },
        'loaihang_rel': {'label': 'Loại hàng'},
        'congtysx_rel': {'label': 'Công ty sản xuất'}
    }
    can_view_details = True
    column_display_pk = True
    can_export = True
    column_searchable_list = ['ten_hang', 'chatlieu_id', 'loaihang_id', 'id_cty_sx']
    column_filters = ['ten_hang', 'chatlieu_id', 'loaihang_id', 'id_cty_sx', 'don_gia_nhap', 'don_gia_ban']
    column_labels = {
        'ten_hang': 'Tên sản phẩm',
        'chatlieu_id': 'Chất liệu',
        'loaihang_id': 'Loại hàng',
        'id_cty_sx': 'Công ty sản xuất',
        'don_gia_nhap': 'Giá nhập',
        'don_gia_ban': 'Giá nhập',
        'anh': 'Hình ảnh',
        'ghichu': 'Ghi chú',
        'so_luong': 'Số lượng'
    }
    column_sortable_list = ['don_gia_nhap', 'don_gia_ban', 'ten_hang', 'id_cty_sx']

class LoaiHangView(ModelView):
    column_display_pk = True
    can_export = True
    column_filters = ['ten_hang']
    column_sortable_list = ['ten_hang']
    column_searchable_list = ['ten_hang']
    column_labels = {
        'ten_hang': 'Tên danh mục',

    }


class ChatLieuView(ModelView):
    column_display_pk = True
    can_export = True
    column_filters = ['ten_chatlieu']
    column_sortable_list = ['ten_chatlieu']
    column_searchable_list = ['ten_chatlieu']
    column_labels = {
        'ten_chatlieu': 'Tên danh mục',
    }

class BinhLuanView(ModelView):
    column_list = ['id', 'noi_dung', 'sanpham_id', 'khachhang_id', 'thoi_gian_binh_luan']
    form_columns = ['id', 'sanpham', 'user']
    form_args = {
        'sanpham': {'label': 'Id san pham'},
        'user': {'label': 'id khach hang'},
    }
    can_view_details = True
    column_display_pk = True
    can_export = True
    column_searchable_list = ['sanpham_id', 'khachhang_id']
    column_filters = ['sanpham_id', 'khachhang_id']
    column_labels = {
         'noi_dung': 'Nội dung',
        'sanpham_id': 'Sản phẩm ID',
        'khachhang_id':'ID Khách hàng',
        'thoi_gian_binh_luan': 'Thời gian bình luận'
    }


class KhachHangView(ModelView):
    can_view_details = True
    column_display_pk = True
    can_export = True
    column_searchable_list = ['ten_khachhang', 'dia_chi', 'so_dien_thoai']
    column_filters = ['ten_khachhang']
    column_labels = {
        'ten_khachhang': 'Tên khách hàng',
        'dia_chi': 'Địa chỉ',
        'so_dien_thoai': 'Số điện thoại',
    }
    column_sortable_list = ['ten_khachhang']

    def can_create(self):
        # Không cho phép tạo mới bản ghi
        return False

    def can_edit(self, obj):
        # Không cho phép chỉnh sửa bản ghi đã tồn tại
        return False

    def can_delete(self, obj):
        # Không cho phép xóa bản ghi
        return False

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('dang_nhap'))

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats = ultis.thong_ke_danh_muc())

class ThongKeView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/thongke.html',month_stats = ultis.thong_ke_san_pham_theo_thang(year=year), stats=ultis.thong_ke_san_pham(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == Role_User.NHANVIEN

admin = Admin(app=app, name='Airi Store', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_views(ChatLieuView(ChatLieu, db.session, name='Chất liệu'))
admin.add_view(SanPhamView(Hang, db.session, name='Sản phẩm'))
admin.add_views(LoaiHangView(LoaiHang, db.session, name='Danh mục'))
admin.add_views(CongTySXView(CongTySX, db.session, name='Công ty sản xuất'))
admin.add_views(KhachHangView(KhachHang, db.session, name='Khách hàng'))
admin.add_views(LogoutView(name='Đăng xuất'))
admin.add_views(ThongKeView(name='Thống kê'))
admin.add_views(BinhLuanView(BinhLuan, db.session,name='Bình luận'))



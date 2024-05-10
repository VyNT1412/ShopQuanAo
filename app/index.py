import math

from flask import render_template, request, flash, redirect, session, jsonify
from app import app, login
from app import ultis
from flask_login import login_user, logout_user, current_user, login_required

from app.models import Role_User


# Đường dẫn đến thư mục chứa các hình ảnh

@app.route("/")
def home():
    # Lấy danh sách các tệp hình ảnh trong thư mục
    # Tạo danh sách đường dẫn đầy đủ tới từng tệp hình ảnh
    hang = ultis.get_all_hang()
    return render_template('index.html', hangs=hang, active_page='home')


@app.route("/sanpham")
def hang_list():
    kw = request.args.get('keywords')
    page = request.args.get("page", 1, type=int)
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    # Đếm số lượng sản phẩm phù hợp với điều kiện tìm kiếm
    total = ultis.count_san_pham()

    # Tải danh sách sản phẩm theo từ khóa và trang hiện tại
    hangs = ultis.load_sanPham(kw=kw, from_price=from_price,to_price=to_price, page=page)

    # Thêm thuộc tính 'ten_chat_lieu' vào mỗi sản phẩm nếu có
    for hang in hangs:
        chat_lieu = ultis.get_ten_chat_lieu(hang.chatlieu_id)
        hang.ten_chat_lieu = chat_lieu

    # Tính toán số trang dựa trên số lượng sản phẩm và kích thước trang
    page_size = app.config['PAGE_SIZE']
    pages = math.ceil(total / page_size)
    return render_template('sanpham.html', hangs=hangs, active_page='products', pages=pages)


@app.route("/danhmuc")
def danhmuc_list():
    danhmuc = ultis.count_san_pham_by_id_loai_hang()

    return render_template('danhmuc.html', danhmuchang=danhmuc, active_page='categories')


@app.route("/sanpham/<int:id>")
def chi_tiet_san_pham(id):
    try:
        # Lấy thông tin sản phẩm từ cơ sở dữ liệu
        product = ultis.get_san_pham_by_id(id)
        chat_lieu = ultis.get_ten_chat_lieu(product.chatlieu_id)
        product.ten_chat_lieu = chat_lieu
        binhluan=ultis.get_binh_luan(page=request.args.get('page',1), sp_id=id)

        total = ultis.dem_binh_luan(sp_id=id)
        page_size = app.config['COMMENT_SIZE']
        pages = math.ceil(total / page_size)
        # Trả về template HTML hoặc chuỗi HTML hiển thị thông tin sản phẩm
        return render_template('chi_tiet_san_pham.html', product=product, binhluan=binhluan, pages=pages)
    except Exception as e:
        # Xử lý ngoại lệ và in ra thông báo lỗi
        print(str(e))


@app.route('/dangky', methods=['GET', 'POST'])
def khachang_dangky():
    error_message = None

    if request.method == 'POST':
        hoten = request.form.get('tenkh')
        tendn = request.form.get('tendangnhap')
        mk = request.form.get('mk')
        xacnhanmk = request.form.get('xacnhanmk')
        dc = request.form.get('diachi')
        sdt = request.form.get('sdt')
        check_user = ultis.check_existing_user_kh(tendn, sdt)
        print(check_user)
        # Kiểm tra xem username đã tồn tại trong cơ sở dữ liệu hay chưa
        if check_user:
            error_message = 'Tên đăng nhập hoặc số điện thoại đã tồn tại. Vui lòng chọn thông tin khác.'
            # Trả về lại form đăng ký với thông báo lỗi
            flash(error_message, 'danger')
        else:
            if mk.strip().__eq__(xacnhanmk.strip()) and len(mk.strip()) >= 8:
                ultis.add_user(tendn, mk)
                ultis.add_user_kh(ultis.get_user_by_username(tendn), hoten, dc, sdt)
                print(ultis.get_user_by_username(tendn))
                error_message = 'Đăng ký thành công'
                flash(error_message, 'success')
            else:
                error_message = 'Mật khẩu xác nhận không chính xác hoặc mật khẩu bé hơn 8 ký tự'
                flash(error_message, 'danger')

            # Trả về lại form đăng ký với thông báo lỗi

    # Nếu là phương thức GET hoặc không có lỗi, trả về form đăng ký rỗng
    return render_template('dangky.html', active_page='register', error_message=error_message)


@app.route('/api/add-cart', methods=['post'])
def them_vao_gio_hang():
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart:  # san pham da co trong gio
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:  # san pham chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(ultis.count_cart(cart))

@app.route('/api/update-cart', methods=['put'])
def cap_nhat_gio_hang():
    data = request.json
    id = str(data.get("id"))
    quantity = data.get('quantity')
    cart = session.get('cart')

    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart
    return jsonify(ultis.count_cart(cart))

@app.route('/api/delete-cart/<sanpham_id>', methods=['delete'])
def xoa_gio_hang(sanpham_id):
    cart =  session.get('cart')
    if cart and sanpham_id in cart:
        del cart[sanpham_id]
        session['cart']=cart

    return jsonify(ultis.count_cart(cart))

@app.route("/api/binhluan", methods=['post'])
@login_required
def them_binh_luan():
    data = request.json
    noi_dung = data.get('noi_dung')
    sanpham_id = data.get('sanpham_id')

    try:
        c = ultis.them_binh_luan(noi_dung=noi_dung, sanpham_id=sanpham_id)
    except:
        return jsonify({'status': 404, 'err_msg': 'Hệ thống đang có lỗi!'})
    else:

        return jsonify({
            'status': 201,
            "comment":{
                'id': c.id,
                'noi_dung': c.noi_dung,
                'thoi_gian_binh_luan':  c.thoi_gian_binh_luan,
                'user': {
                    'username': current_user.username
                }
            }})

@app.route('/giohang')
def gio_hang():
    # return render_template('gio_hang.html', stat=ultis.count_cart(session['cart']))
    cart = session.get('cart', {})
    cart_stats = ultis.count_cart(cart)
    return render_template('gio_hang.html', cart_stats=cart_stats)

@app.route('/api/pay', methods = ['post'])
def thanhtoan():
    try:
        kh = ultis.get_khach_hang_by_id_user(current_user.id)
        cart = session.get('cart')  # Get cart from session
        if not cart:
            raise Exception("Cart is empty")

        ultis.them_hoa_don(cart)  # Call function to add invoice based on cart

        del session['cart']  # Remove cart from session after successful payment
        return jsonify({'status': 200})
    except Exception as e:
        return jsonify({'status': 500, 'err_msg': str(e)})
@app.route('/dangnhap', methods=['GET', 'POST'])
def dang_nhap():
    error_message = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = ultis.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            if user.user_role == Role_User.NHANVIEN:
                # Nếu người dùng là nhân viên, chuyển hướng đến trang admin của Flask Admin
                return redirect(url_for('admin.index'))
            else:
                # Nếu người dùng không phải nhân viên, chuyển hướng đến trang khác (ví dụ: trang sản phẩm)
                return redirect(url_for('hang_list'))
        else:
            err_mess = 'Tên đăng nhập hoặc mật khẩu không chính xác'
            flash(err_mess, 'danger')

    return render_template('dangnhap.html', active_page='login', error_message=error_message)


@app.route('/dangxuat')
def dang_xuat():
    logout_user()
    return redirect(url_for('dang_nhap'))


@app.route('/info_user')
def info_user():
    khachhang = ultis.get_khach_hang_by_id_user(current_user.id)
    return render_template('thongtin_user.html', khachhang=khachhang)


@app.route('/sua_thong_tin_tk', methods=['GET', 'POST'])
def sua_tt_tk():
    khachhang = ultis.get_khach_hang_by_id_user(current_user.id)
    if request.method.__eq__('GET'):
        return render_template('suathongtinuser.html', khachhang=khachhang)
    elif request.method.__eq__('POST'):
        tenkh = request.form.get('tenkh')
        diachi = request.form.get('diachi')
        sdt = request.form.get('sdt')

        ultis.update_tt_khach_hang(current_user.id, tenkh=tenkh, diachi=diachi, sdt=sdt)
        flash('Thông tin tài khoản đã được cập nhật thành công!', 'success')
        return redirect(url_for('info_user'))
@app.route('/lichsumua')
def lich_su_mua_hang():


    # Lấy danh sách đơn hàng của khách hàng
    danh_sach_don_hang  = ultis.lay_danh_sach_don_hang_khach_hang(current_user.id)

    # Trả về template với dữ liệu đã lấy
    return render_template('lichsumuahang.html',  danh_sach_don_hang =danh_sach_don_hang )
@app.route('/doi_mk', methods=['GET', 'POST'])
def doi_mk():
    if request.method.__eq__('POST'):
        old_pass = request.form.get('oldpassword')
        new_pass = request.form.get('newpassword')
        conf_pass = request.form.get('confpassword')

        # Kiểm tra new_pass và conf_pass
        if new_pass != conf_pass:
            flash('Xác nhận mật khẩu mới không trùng khớp!', 'danger')
            return render_template('doi_mk.html')

        # Gọi hàm doi_mat_khau từ ultis và xử lý kết quả
        if ultis.doi_mat_khau(current_user.id, old_pass, new_pass):
            flash('Đổi mật khẩu thành công!', 'success')
            return redirect(url_for('info_user'))
        else:
            flash('Đổi mật khẩu thất bại!', 'danger')
            return render_template('doi_mk.html')

    return render_template('doi_mk.html')


@login.user_loader
def user_load(user_id):
    return ultis.get_user_by_id(id=user_id)


@app.context_processor
def common_response():
    return {
        'cart_stats': ultis.count_cart(session.get('cart'))
    }

if __name__ == '__main__':
    from app.admin import *

    app.run(debug=True)

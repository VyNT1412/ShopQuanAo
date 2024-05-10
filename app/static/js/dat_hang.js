function them_vao_gio_hang(event, id, ten_sp, gia) {
    event.preventDefault(); // Ngăn chặn hành động mặc định của thẻ <a>
    // alert("Đã thêm sản phẩm vào giỏ hàng!");
    //promise
    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': ten_sp,
            'price': gia,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (res) {
        console.info(res)
        return res.json()
    }).then(function (data) {
        console.info(data)

        let counter = document.getElementsByClassName('cart_counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
    }).catch(function (err) {
        console.error(err)
    })
}

function thanhtoan() {
    if (confirm("Bạn chắc chắn thanh toán!") === true) {
        fetch("/api/pay", {
            method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert(data.err_msg);
        })
    }
}

function cap_nhat_gio_hang(id, obj) {
    fetch("/api/update-cart", {
        method: "put",
        body: JSON.stringify({
            'id': id,
            'quantity': parseInt(obj.value)
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let counter = document.getElementsByClassName('cart_counter')
        for (let i = 0; i < counter.length; i++)
            counter[i].innerText = data.total_quantity
        let tongtien = document.getElementById('tong_tien')
        tongtien.innerText = new Intl.NumberFormat().format(data.total_amount);
    })
}

function xoa_gio_hang(id) {
    if (confirm("Bạn chắc chắn muốn xóa?") == true) {
        fetch('/api/delete-cart/'+id, {
            method: "delete",
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            let counter = document.getElementsByClassName('cart_counter')
            for (let i = 0; i < counter.length; i++)
                counter[i].innerText = data.total_quantity
            let tongtien = document.getElementById('tong_tien')
            tongtien.innerText = new Intl.NumberFormat().format(data.total_amount);

            let e = document.getElementById('sanpham'+id)
            e.style.display='none'
        }).catch(err=> console.error(err))
    }
}


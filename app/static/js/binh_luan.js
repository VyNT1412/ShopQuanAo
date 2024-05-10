function them_binh_luan(productId) {
    let nd = document.getElementById('commentId');
    if (nd !== null) {
        let noiDung = nd.value;

        fetch('/api/binhluan', {
            method: "post",
            body: JSON.stringify({
                'sanpham_id': productId,
                'noi_dung': noiDung
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(res => res.json()).then(data => {
            if (data.status == 201) {
                let c = data.comment;
                let thoiGianBinhLuan = new Date(c.thoi_gian_binh_luan);

                let cm = document.getElementById('comments');

                // Thêm HTML mới vào cuối của comments
                cm.innerHTML += `
                    <div class="row">
                        <div class="col-md-1 col-xs-4 text-center">
                                        <span><b>${c.user.username}</b></span>

                        </div>
                        <div class="col-md-11 col-xs-8 align-self-center">
                            <p>${c.noi_dung}</p>
            <p><em>${moment(thoiGianBinhLuan).locale("vi").fromNow()}</em></p>
                        </div>
                    </div>
                `;
            } else if (data.status == 404) {
                alert(data.err_msg);
            }
        });
    }
}
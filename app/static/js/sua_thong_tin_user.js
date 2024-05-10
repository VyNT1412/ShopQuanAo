document.addEventListener('DOMContentLoaded', function () {
    const editInfoBtn = document.getElementById('btn_suatt');
    const changePasswordBtn = document.getElementById('btn_doimk');

    if (editInfoBtn) {
        editInfoBtn.addEventListener('click', function () {
            const url = editInfoBtn.getAttribute('data-url');
            window.location.href = url;
        });
    }

    if (changePasswordBtn) {
        changePasswordBtn.addEventListener('click', function () {
            const url = changePasswordBtn.getAttribute('data-url');
            window.location.href = url;
        });
    }
});
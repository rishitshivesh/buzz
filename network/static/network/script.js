document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById("bt");
    const nav = document.getElementById("navb");
    btn.addEventListener('click', () => {
        nav.classList.toggle("active");
        btn.classList.toggle("active");
    });
    $(function() {
        $('.space').on('keypress', function(e) {
            if (e.which < 46 || e.which == 47 || e.which == 58 || e.which == 59 || e.which == 60 || e.which == 61 || e.which == 62 || e.which == 63 || e.which == 64 || e.which == 91 || e.which == 92 || e.which == 93 || e.which == 94 || e.which == 96 || e.which > 122) {
                return false;
            }
        });
    });

});
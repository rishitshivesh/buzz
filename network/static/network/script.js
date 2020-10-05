document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById("bt");
    const nav = document.getElementById("navb");
    btn.addEventListener('click', () => {
        nav.classList.toggle("active");
        btn.classList.toggle("active");
    });
    $(function() {
        $('.space').on('keypress', function(e) {
            if (e.which == 32) {
                console.log('Space Not Allowed');
                return false;
            } else if ((e.which < 48 && e.which >= 57) || (e.which >= 65 && e.which <= 122)) {
                console.log(`Character ${e.which} not allowed`);
                return false;
            }
        });
    });

});
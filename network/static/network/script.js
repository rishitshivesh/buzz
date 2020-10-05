document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById("bt");
    const nav = document.getElementById("navb");
    btn.addEventListener('click', () => {
        nav.classList.toggle("active");
        btn.classList.toggle("active");
    });

});
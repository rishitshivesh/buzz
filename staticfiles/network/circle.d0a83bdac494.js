document.addEventListener('DOMContentLoaded', () => {
    var count = 0;
    circle = document.querySelector('#circle');
    text = document.querySelector('#circlet');
    document.getElementById('body').onkeyup = function() {
        var perc = this.value.length / 500 * 100;
        var percent = perc.toFixed(0);
        document.getElementById('circlet').innerHTML = `${this.value.length}`;
        if (percent == '100') {
            document.getElementById('circle').className = `c100 p${percent} small orange float-right`
        } else {
            document.getElementById('circle').className = `c100 p${percent} small float-right`
        }

    };
});
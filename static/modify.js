function c(cbi, cbd) {
    var cb = document.getElementById(cbi);
    var d = document.getElementById(cbd);
    if (cb.checked) {
        d.remove();
    } else {
        var dcb = document.createElement('input');
        dcb.type = 'hidden';
        dcb.name = cbi;
        dcb.value = 'False';
        dcb.id = cbd;
        cb.parentElement.appendChild(dcb);
    }
}
parent.load_bar1();
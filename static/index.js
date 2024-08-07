function load_page(id) {
    document.getElementById('page_view').src = `/list/${id}`;
}
function add_page(){
    document.getElementById('page_view').src = `/add`;
}
document.getElementById('page_view').src = `/init`;
function load_page(id) {
    document.getElementById('page_view').src = `/list/${id}`;
}
function add_page(){
    document.getElementById('page_view').src = `/add`;
}
function load_bar1(){
    document.getElementById('bar_view').src = `/bar1`;
}
function load_bar2(){
    document.getElementById('bar_view').src = `/bar2`;
}
function bar_exec(sel){
    const view = document.getElementById('page_view');
    const dom = view.contentDocument;
    dom.querySelector('#action').value = sel;
    dom.getElementById('bar_exec').submit();
}
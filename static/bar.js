function del_page(event) {
    var userConfirmed = confirm('本当に削除しても良いですか?');
    if (userConfirmed) {
        parent.bar_exec('delete');
    }
}
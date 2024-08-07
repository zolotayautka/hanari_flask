function openModal(imageBase64) {
    var modal = document.getElementById("picModal");
    var modalImg = document.getElementById("modalImg");
    modal.style.display = "block";
    modalImg.src = "data:image/jpeg;base64," + imageBase64;
}
function closeModal() {
    var modal = document.getElementById("picModal");
    modal.style.display = "none";
}
function osirase(event) {
    var userConfirmed = confirm('本当に削除しても良いですか?');
    if (!userConfirmed) {
        event.preventDefault();
    }
}
function k(event) {
    var a = event.submitter;
    if (a.value === 'delete') {
        return osirase(event);
    }
    return true;
}
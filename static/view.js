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
parent.load_bar2()
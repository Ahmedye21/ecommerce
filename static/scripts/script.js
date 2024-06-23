document.addEventListener("DOMContentLoaded", () => {
    const addToCartButtons = document.querySelectorAll(".add-to-cart");
    const modal = document.getElementById("modal");
    const modalMessage = document.getElementById("modal-message");
    const confirmYes = document.getElementById("confirm-yes");
    const confirmNo = document.getElementById("confirm-no");
    let selectedProduct = {};

    addToCartButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            selectedProduct.price = event.target.getAttribute("data-price");
            selectedProduct.name = event.target.getAttribute("data-name");
            modalMessage.textContent = `Are you sure about that? We will take $${selectedProduct.price} from your account.`;
            modal.style.display = "flex";
        });
    });

    confirmYes.addEventListener("click", () => {
        const userData = JSON.parse(localStorage.getItem("userData"));
        const orderCode = Math.random().toString(36).substring(2, 9).toUpperCase();
        localStorage.setItem("orderData", JSON.stringify({ product: selectedProduct, orderCode, ...userData }));
        window.location.href = "order-confirmation.html";
    });

    confirmNo.addEventListener("click", () => {
        modal.style.display = "none";
    });
});

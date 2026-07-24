// AUTO MESSAGE (uses data from HTML)
document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("live-message-container");
    if (!container) return;

    const messageText = container.dataset.messageText;
    const messageType = container.dataset.messageType;

    if (messageText) {
        showMessage(messageText, messageType);
    }
});

// DOWNLOAD HANDLER
document.addEventListener("click", function (e) {

    const link = e.target.closest("a.download-btn");
    if (!link) return;

    e.preventDefault();

    const url = link.href;
    const message = link.dataset.message || "Download started";
    const type = link.dataset.type || "success";

    showMessage(message, type);

    setTimeout(() => {
        window.location.href = url;
    }, 300);
});

// MESSAGE FUNCTION
function showMessage(text, type = "success") {

    const container = document.getElementById("live-message-container");

    const msg = document.createElement("div");

    msg.className = `alert alert-${getBootstrapType(type)} alert-dismissible fade show`;

    msg.innerHTML = `
        ${text}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    container.appendChild(msg);

    setTimeout(() => {
        msg.classList.remove("show");
        msg.classList.add("fade");
        setTimeout(() => msg.remove(), 300);
    }, 3000);
}

function getBootstrapType(type) {
    if (type === "error") return "danger";
    if (type === "warning") return "warning";
    return "success";
}
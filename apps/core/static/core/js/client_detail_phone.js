function showPopupMessage(message, isError = false) {
    const popup = document.getElementById("popup");
    popup.innerText = message;
    popup.classList.remove("alert-success", "alert-danger");
    popup.classList.add(isError ? "alert-danger" : "alert-success");
    popup.style.display = "block";
    setTimeout(() => {
        popup.style.display = "none";
    }, 3000);
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("phone-form");
    if (!form) return;

    const url = form.dataset.url;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken
                },
                body: formData,
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showPopupMessage(data.message || "Phone update success✅");
                location.reload()
            } else {
                console.error("Server returned error", data);
                showPopupMessage(data.message || "❌ Error", true);
            }

        } catch (error) {
            console.error("JS fetch error:", error);
            showPopupMessage("❌ Error", true);
        }
    });
});

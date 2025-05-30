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
    const form = document.getElementById("address-form");
    if (!form) return;

    const btnDelete = document.getElementById("address_delete_btn");
    const urlDelete = form.dataset.urlDelete;

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
        const url = form.dataset.url;
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
                showPopupMessage(data.message || "Address success update ✅");
            } else {
                console.error("Server returned error", data);
                showPopupMessage(data.message || "❌ Error", true);
            }

        } catch (error) {
            console.error("JS fetch error:", error);
            showPopupMessage("❌ Error", true);
        }
    });

     btnDelete.addEventListener("click", async function (e) {
        e.preventDefault();
        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;
        try {
            const response = await fetch(urlDelete, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ delete: true }),
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showPopupMessage(data.message || "Address delete ✅");
                form.reset()
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

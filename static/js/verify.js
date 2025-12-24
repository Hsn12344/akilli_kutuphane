async function verifyAccount() {
    const emailEl = document.getElementById("verifyEmail");
    const codeEl = document.getElementById("verifyCode");
    const msgEl = document.getElementById("verifyMessage");

    if (!emailEl || !codeEl) return;

    const email = emailEl.value.trim();
    const code = codeEl.value.trim();

    if (code.length !== 6) {
        msgEl.textContent = "Doğrulama kodu 6 haneli olmalıdır.";
        return;
    }

    try {
        const res = await fetch(`${API_URL}/auth/verify`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, code })
        });

        const data = await res.json();
        msgEl.textContent = data.message || "";

        if (res.ok) {
            msgEl.classList.remove("text-danger");
            msgEl.classList.add("text-success");

            setTimeout(() => {
                window.location.href = "/login";
            }, 1200);
        }

    } catch (err) {
        msgEl.textContent = "Sunucu hatası oluştu.";
    }
}

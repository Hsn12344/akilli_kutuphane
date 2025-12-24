window.addEventListener("DOMContentLoaded", () => {
    const token = getToken();
    const role = getRole();
    const path = window.location.pathname;

    // Eğer zaten login ise login/register'a girerse yönlendir
    if (token && (path === "/" || path === "/login" || path === "/register")) {
        if (role === "admin") window.location.href = "/admin";
        else window.location.href = "/user";
    }
});

async function login() {
    const emailEl = document.getElementById("loginEmail");
    const passEl = document.getElementById("loginPassword");
    const msgEl = document.getElementById("loginMessage");

    if (!emailEl || !passEl) return;

    const email = emailEl.value;
    const password = passEl.value;

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();
        if (msgEl) msgEl.textContent = data.message || data.error || "";

        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("role", data.role);
            localStorage.setItem("email", email);

            if (data.role === "admin") {
                window.location.href = "/admin";
            } else {
                window.location.href = "/user";
            }
        }
    } catch (err) {
        if (msgEl) msgEl.textContent = "Sunucu hatası.";
    }
}

async function register() {
  const nameEl = document.getElementById("registerName");
  const emailEl = document.getElementById("registerEmail");
  const passEl = document.getElementById("registerPassword");
  const msgEl = document.getElementById("registerMessage");

  const name = (nameEl?.value || "").trim();
  const email = (emailEl?.value || "").trim();
  const password = (passEl?.value || "").trim();

  try {
    const res = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password })
    });

    let data = {};
    try { data = await res.json(); } catch (e) {}

    console.log("REGISTER status:", res.status, "data:", data);

    if (msgEl) msgEl.textContent = data.message || data.error || "";

    if (res.status === 201 || res.status === 200) {
      localStorage.setItem("verify_email", email);
      window.location.replace("/verify");
    }

  } catch (err) {
    console.error(err);
    if (msgEl) msgEl.textContent = "Sunucu hatası.";
  }
}

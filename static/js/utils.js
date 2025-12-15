// Global API URL
const API_URL = "http://127.0.0.1:5000";

function getToken() {
    return localStorage.getItem("token");
}

function getRole() {
    return localStorage.getItem("role");
}

function getEmail() {
    return localStorage.getItem("email");
}

// Sayfa bazlı rol kontrolü
function requireAuth(allowedRoles = null) {
    const token = getToken();
    const role = getRole();

    if (!token || isTokenExpired(token)) {
        localStorage.clear();
        window.location.href = "/login";
        return false;
    }

    if (allowedRoles && !allowedRoles.includes(role)) {
        if (role === "admin") window.location.href = "/admin";
        else window.location.href = "/user";
        return false;
    }
    return true;
}

function logout() {
    localStorage.clear();
    window.location.href = "/login";
}

// Sidebar toggle (hem user hem admin layout)
document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("menu-toggle");
    const wrapper = document.getElementById("wrapper");
    if (toggleBtn && wrapper) {
        toggleBtn.addEventListener("click", () => {
            wrapper.classList.toggle("toggled");
        });
    }

    // Email gösterimi
    const email = getEmail();
    const userEmailDisplay = document.getElementById("userEmailDisplay");
    const adminEmailDisplay = document.getElementById("adminEmailDisplay");
    if (email && userEmailDisplay) userEmailDisplay.textContent = email;
    if (email && adminEmailDisplay) adminEmailDisplay.textContent = email;
});


function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        const now = Math.floor(Date.now() / 1000);
        return payload.exp < now;
    } catch (e) {
        return true;
    }
}


// =======================================
// USER FINES PAGE
// =======================================

document.addEventListener("DOMContentLoaded", () => {
    if (!requireAuth(["user", "admin"])) return;
    loadUserFines();
});

// ---------------------------------------
// KULLANICININ CEZALARINI GETİR
// ---------------------------------------
async function loadUserFines() {
    const token = getToken();
    if (!token) return;

    const tbody = document.getElementById("userFinesTableBody");
    if (!tbody) return;

    try {
        const res = await fetch(`${API_URL}/borrow/my-fines`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const fines = await res.json();
        tbody.innerHTML = "";

        if (!Array.isArray(fines) || fines.length === 0) {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td colspan="4" class="text-center text-muted">
                    Aktif cezanız bulunmamaktadır.
                </td>
            `;
            tbody.appendChild(tr);
            return;
        }

        fines.forEach(f => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${f.id}</td>
                <td>${f.borrow_id}</td>
                <td>${f.amount.toFixed(2)} ₺</td>
                <td>
                    <button class="btn btn-sm btn-success"
                        onclick="payFine(${f.id})">
                        Öde
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error("Cezalar alınamadı:", err);
    }
}

// ---------------------------------------
// CEZA ÖDE
// ---------------------------------------
async function payFine(fineId) {
    const token = getToken();
    if (!token) return;

    if (!confirm("Bu cezayı ödemek istiyor musunuz?")) return;

    try {
        const res = await fetch(`${API_URL}/borrow/pay-fine/${fineId}`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await res.json();
        alert(data.message || "Ceza ödendi.");

        loadUserFines();

    } catch (err) {
        console.error("Ceza ödeme hatası:", err);
    }
}

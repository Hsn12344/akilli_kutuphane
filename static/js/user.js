window.addEventListener("DOMContentLoaded", () => {
    if (!requireAuth(["user", "admin"])) return;

    const path = window.location.pathname;

    if (path === "/user" || path === "/user/") {
        loadUserDashboard();
    } else if (path === "/user/books") {
        fetchBooks();
    } else if (path === "/user/borrows") {
        fetchBorrowed();
    }
});


// --------------------------------------------
// DASHBOARD
// --------------------------------------------
async function loadUserDashboard() {
    const token = getToken();
    if (!token) return;

    try {
        const res = await fetch(`${API_URL}/borrow/borrows`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const borrows = await res.json();

        let total = borrows.length;
        let active = borrows.filter(b => !b.return_date).length;
        let late = 0;

        const now = new Date();
        borrows.forEach(b => {
            if (!b.return_date && b.due_date) {
                const due = new Date(b.due_date);
                if (due < now) late++;
            }
        });

        document.getElementById("statTotalBorrows").textContent = total;
        document.getElementById("statActiveBorrows").textContent = active;
        document.getElementById("statLateBorrows").textContent = late;

    } catch (err) {
        console.error(err);
    }
}


// ---------------------------------------------------
// KİTAPLARI GETİR
// ---------------------------------------------------
async function fetchBooks(search = "") {
    try {
        let url = `${API_URL}/books`;
        if (search) {
            url = `${API_URL}/books/search?title=${encodeURIComponent(search)}`;
        }

        const res = await fetch(url);
        const books = await res.json();

        const tbody = document.querySelector("#booksTable tbody");
        const msgEl = document.getElementById("booksMessage");

        if (!tbody) return;

        tbody.innerHTML = "";

        if (!Array.isArray(books) || books.length === 0) {
            if (msgEl) msgEl.textContent = "Hiç kitap bulunamadı.";
            return;
        }

        if (msgEl) msgEl.textContent = "";

        books.forEach(book => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.category}</td>
                <td>${book.available_copies}</td>
                <td>
                    ${book.available_copies > 0
                        ? `<button class="btn btn-sm btn-primary" onclick="borrowBook(${book.id})">Ödünç Al</button>`
                        : '<span class="badge bg-secondary">Stokta Yok</span>'}
                </td>
            `;

            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error(err);
    }
}


// ---------------------------------------------------
// ÖDÜNÇ AL
// ---------------------------------------------------
async function borrowBook(bookId) {
    const token = getToken();
    if (!token) {
        alert("Lütfen giriş yapın.");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/borrow`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ book_id: bookId })
        });

        const data = await res.json();
        alert(data.message || "Kitap ödünç alındı!");

        fetchBooks();
        fetchBorrowed();

    } catch (err) {
        console.error(err);
        alert("Bir hata oluştu.");
    }
}


// ---------------------------------------------------
// ÖDÜNÇLERİ GETİR
// ---------------------------------------------------
async function fetchBorrowed() {
    const token = getToken();
    if (!token) return;

    try {
        const res = await fetch(`${API_URL}/borrow/borrows`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const borrows = await res.json();
        const tbody = document.querySelector("#borrowedTable tbody");

        if (!tbody) return;

        tbody.innerHTML = "";

        borrows.forEach(b => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${b.id}</td>
                <td>${b.book}</td>
                <td>${b.borrow_date}</td>
                <td>${b.due_date}</td>
                <td>${b.return_date || '-'}</td>
                <td>
                    ${!b.return_date
                        ? `<button class="btn btn-sm btn-outline-success" onclick="returnBook(${b.id})">İade Et</button>`
                        : ''}
                </td>
            `;

            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error(err);
    }
}


// ---------------------------------------------------
// İADE ET
// ---------------------------------------------------
async function returnBook(borrowId) {
    const token = getToken();
    if (!token) {
        alert("Lütfen giriş yapın.");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/borrow/return/${borrowId}`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await res.json();
        alert(data.message || "İade işlemi tamamlandı!");

        fetchBooks();
        fetchBorrowed();

    } catch (err) {
        console.error(err);
    }
}


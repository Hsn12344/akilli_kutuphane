window.addEventListener("DOMContentLoaded", () => {
    if (!requireAuth(["admin"])) return;

    const path = window.location.pathname;

    if (path === "/admin" || path === "/admin/") {
        loadAdminDashboard();
    } else if (path === "/admin/books") {
        fetchBooksAdmin();
    } else if (path === "/admin/categories") {
        fetchCategories();
    } else if (path === "/admin/users") {
        loadUsers();
    } else if (path === "/admin/borrows") {
        fetchAllBorrowed();
    } else if (path === "/admin/fines") {
        fetchFines();
    }
});

// DASHBOARD
async function loadAdminDashboard() {
    const token = getToken();
    if (!token) return;

    try {
        const [booksRes, catRes, borrowsRes, finesRes] = await Promise.all([
            fetch(`${API_URL}/books`),
            fetch(`${API_URL}/categories`),
            fetch(`${API_URL}/borrow/borrows`, {
                headers: { "Authorization": `Bearer ${token}` }
            }),
            fetch(`${API_URL}/borrow/fines`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
        ]);

        const books = await booksRes.json();
        const categories = await catRes.json();
        const borrows = await borrowsRes.json();
        const fines = await finesRes.json();

        const statBooks = document.getElementById("adminStatBooks");
        const statCats = document.getElementById("adminStatCategories");
        const statBorrows = document.getElementById("adminStatBorrows");
        const statFines = document.getElementById("adminStatFines");

        if (statBooks) statBooks.textContent = books.length || 0;
        if (statCats) statCats.textContent = categories.length || 0;
        if (statBorrows) statBorrows.textContent = borrows.filter(b => !b.return_date).length || 0;

        let totalFine = 0;
        fines.forEach(f => totalFine += f.amount || 0);
        if (statFines) statFines.textContent = totalFine.toFixed(2);
    } catch (err) {
        console.error(err);
    }
}

// KITAP YÖNETİMİ
async function fetchBooksAdmin(search = "") {
    try {
        let url = `${API_URL}/books`;
        if (search) {
            url = `${API_URL}/books/search?title=${encodeURIComponent(search)}`;
        }

        const res = await fetch(url);
        const books = await res.json();

        const tbody = document.querySelector("#adminBooksTable tbody");
        if (!tbody) return;

        tbody.innerHTML = "";
        books.forEach(book => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.category}</td>
                <td>${book.available_copies}</td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteBook(${book.id})">
                        Sil
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
    }
}

async function addBook() {
    const token = getToken();
    const role = getRole();
    if (!token || role !== "admin") {
        alert("Admin girişi gerekli.");
        return;
    }

    const title = document.getElementById("adminBookTitle").value;
    const isbn = document.getElementById("adminBookISBN").value;
    const author_name = document.getElementById("adminBookAuthor").value;
    const category_id = parseInt(document.getElementById("adminBookCategory").value);
    const available_copies = parseInt(document.getElementById("adminBookCopies").value);
    const msgEl = document.getElementById("adminBookMessage");

    try {
        const res = await fetch(`${API_URL}/books`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ title, isbn, author_name, category_id, available_copies })
        });

        const data = await res.json();
        if (msgEl) msgEl.textContent = data.message || "Kitap eklendi.";

        fetchBooksAdmin();
    } catch (err) {
        console.error(err);
        if (msgEl) msgEl.textContent = "Hata oluştu.";
    }
}

async function deleteBook(bookId) {
    const token = getToken();
    const role = getRole();
    if (!token || role !== "admin") {
        alert("Admin girişi gerekli.");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/books/${bookId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await res.json();
        alert(data.message || data.error || "");
        fetchBooksAdmin();
    } catch (err) {
        console.error(err);
    }
}

// KATEGORİLER
async function fetchCategories() {
    try {
        const res = await fetch(`${API_URL}/categories`);
        const categories = await res.json();

        const tbody = document.querySelector("#categoryTable tbody");
        if (!tbody) return;

        tbody.innerHTML = "";
        categories.forEach(cat => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${cat.id}</td>
                <td>${cat.name}</td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteCategory(${cat.id})">
                        Sil
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
    }
}

async function addCategory() {
    const token = getToken();
    const role = getRole();
    if (!token || role !== "admin") {
        alert("Admin girişi gerekli.");
        return;
    }

    const name = document.getElementById("adminCategoryName").value;

    try {
        await fetch(`${API_URL}/categories`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ name })
        });

        fetchCategories();
    } catch (err) {
        console.error(err);
    }
}

async function deleteCategory(catId) {
    const token = getToken();
    const role = getRole();
    if (!token || role !== "admin") {
        alert("Admin girişi gerekli.");
        return;
    }

    try {
        await fetch(`${API_URL}/categories/${catId}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        });

        fetchCategories();
        fetchBooksAdmin();
    } catch (err) {
        console.error(err);
    }
}

// KULLANICI İŞLEMLERİ
async function makeAdmin() {
    const token = getToken();
    const role = getRole();
    if (!token || role !== "admin") {
        alert("Admin girişi gerekli.");
        return;
    }

    const email = document.getElementById("adminMakeEmail").value;
    const msgEl = document.getElementById("adminMakeMessage");

    try {
        const res = await fetch(`${API_URL}/api/admin/make-admin`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ email })
        });

        const data = await res.json();
        if (msgEl) msgEl.textContent = data.message || data.error || "";
    } catch (err) {
        console.error(err);
        if (msgEl) msgEl.textContent = "Hata oluştu.";
    }
}

// ÖDÜNÇ KAYITLARI
async function fetchAllBorrowed() {
    const token = getToken();
    const role = getRole();
    if (!token || role !== "admin") return;

    try {
        const res = await fetch(`${API_URL}/borrow/borrows`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const borrows = await res.json();
        const tbody = document.querySelector("#adminBorrowedTable tbody");
        if (!tbody) return;

        tbody.innerHTML = "";
        borrows.forEach(b => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${b.id}</td>
                <td>${b.book}</td>
                <td>${b.user}</td>
                <td>${b.borrow_date}</td>
                <td>${b.due_date}</td>
                <td>${b.return_date || '-'}</td>
                <td>
                    ${!b.return_date
                        ? `<button class="btn btn-sm btn-outline-success" onclick="adminReturnBook(${b.id})">İade Et</button>`
                        : ''}
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
    }
}

async function adminReturnBook(borrowId) {
    const token = getToken();
    const role = getRole();
    if (!token || role !== "admin") {
        alert("Admin girişi gerekli.");
        return;
    }

    try {
        const res = await fetch(`${API_URL}/borrow/return/${borrowId}`, {
            method: "POST",
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await res.json();
        alert(data.message || "İade işlemi tamamlandı!");

        fetchAllBorrowed();
        fetchBooksAdmin();
    } catch (err) {
        console.error(err);
    }
}

// CEZALAR
async function fetchFines() {
    const token = getToken();
    if (!token) return;

    try {
        const res = await fetch(`${API_URL}/borrow/fines`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const fines = await res.json();
        const tbody = document.querySelector("#adminFinesTable tbody");
        if (!tbody) return;

        tbody.innerHTML = "";

        fines.forEach(f => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${f.id}</td>
                <td>${f.user_name || "-"}</td>
                <td>${f.borrow_id}</td>
                <td>${f.amount.toFixed(2)} TL</td>
                <td>
                    ${f.is_paid
                        ? '<span class="badge bg-success">Ödendi</span>'
                        : '<span class="badge bg-danger">Ödenmedi</span>'}
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error("Cezalar alınamadı:", err);
    }
}

async function loadUsers() {
    const token = getToken();

    try {
        const res = await fetch(`${API_URL}/api/admin/users`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const users = await res.json();
        const tbody = document.getElementById("userTableBody");

        tbody.innerHTML = "";

        users.forEach(u => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${u.id}</td>
                <td>${u.name}</td>
                <td>${u.email}</td>
                <td>${u.role}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error("Kullanıcı listesi alınamadı:", err);
    }
}

function fetchBooksAdmin() {
    fetch("/books")
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById("adminBooksTable");
            tbody.innerHTML = "";

            data.forEach(book => {
                const tr = document.createElement("tr");

                tr.innerHTML = `
                    <td>${book.id}</td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.category_id}</td>
                    <td>${book.available_copies}</td>
                    <td>
                        <button class="btn btn-sm btn-warning"
                            onclick="openEditBookModal(
                                ${book.id},
                                '${book.title}',
                                '${book.isbn}',
                                '${book.category_id}',
                                ${book.available_copies}
                            )">
                            Düzenle
                        </button>
                    </td>
                `;

                tbody.appendChild(tr);
            });
        });
}

function openEditBookModal(id, title, isbn, category_id, stock) {
    document.getElementById("editBookId").value = id;
    document.getElementById("editTitle").value = title;
    document.getElementById("editIsbn").value = isbn;
    document.getElementById("editCategory").value = category_id;
    document.getElementById("editStock").value = stock;

    const modal = new bootstrap.Modal(document.getElementById("editBookModal"));
    modal.show();
}

async function updateBook() {
    const id = document.getElementById("editBookId").value;

    const data = {
        title: document.getElementById("editTitle").value,
        isbn: document.getElementById("editIsbn").value,
        category_id: parseInt(document.getElementById("editCategory").value),
        available_copies: parseInt(document.getElementById("editStock").value)
    };

    try {
        const res = await fetch(`/books/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) {
            alert(result.error || "Güncelleme başarısız");
            return;
        }

        alert("Kitap güncellendi");
        location.reload();

    } catch (err) {
        console.error(err);
        alert("Sunucu hatası");
    }
}

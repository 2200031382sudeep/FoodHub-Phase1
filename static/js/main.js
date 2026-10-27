// ---------- Toast notifications ----------
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = "toast " + type;
  toast.textContent = message; // textContent (not innerHTML) prevents XSS
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// ---------- Mobile menu ----------
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");
menuToggle.addEventListener("click", () => {
  const open = navLinks.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", open);
});

// ---------- Delivery location (remembered in the browser) ----------
const locationText = document.getElementById("locationText");
const savedLocation = localStorage.getItem("fx_location");
if (savedLocation) locationText.textContent = savedLocation;

document.getElementById("locationBtn").addEventListener("click", () => {
  const city = prompt("Enter your delivery city or area:");
  if (city && city.trim()) {
    locationText.textContent = city.trim();
    localStorage.setItem("fx_location", city.trim());
    showToast("Delivery location updated", "success");
  }
});

// ---------- Features that arrive in later phases ----------
document.querySelectorAll("[data-coming]").forEach((el) => {
  el.addEventListener("click", (e) => {
    e.preventDefault();
    showToast(el.dataset.coming);
  });
});

const searchForm = document.getElementById("searchForm");
if (searchForm) {
  searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    showToast("Search connects to MySQL in Phase 7");
  });
}

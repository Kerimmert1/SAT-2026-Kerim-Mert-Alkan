/**
 * TR3MX Devamsızlık ve İzin Takip Sistemi
 * Ana Kullanıcı Arayüzü & Etkileşim Scripti
 */

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initClock();
    initSidebarToggle();
    initDateCalculators();
    initFlashAlerts();
});

// --- TEMA YÖNETİMİ (DARK / LIGHT MODE) ---
function initTheme() {
    const savedTheme = localStorage.getItem('tr3mx_theme') || 'light';
    setTheme(savedTheme);

    const themeToggleBtn = document.getElementById('themeToggleBtn');
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            setTheme(newTheme);
        });
    }
}

function setTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('tr3mx_theme', theme);
    
    const icon = document.getElementById('themeIcon');
    if (icon) {
        if (theme === 'dark') {
            icon.className = 'fas fa-sun text-warning';
        } else {
            icon.className = 'fas fa-moon text-secondary';
        }
    }
}

// --- DİNAMİK CANLI SAAT ---
function initClock() {
    const clockElements = document.querySelectorAll('.live-clock');
    if (clockElements.length === 0) return;

    function update() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('tr-TR', { hour12: false });
        clockElements.forEach(el => el.textContent = timeStr);
    }
    update();
    setInterval(update, 1000);
}

// --- MOBİL MENÜ TOGGLE ---
function initSidebarToggle() {
    const toggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebar = document.querySelector('.sidebar');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('show');
        });

        document.addEventListener('click', (e) => {
            if (window.innerWidth < 992 && !sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        });
    }
}

// --- İZİN TALEP TARİH VE GÜN HESAPLAYICI ---
function initDateCalculators() {
    const startDateInput = document.getElementById('leave_start_date');
    const endDateInput = document.getElementById('leave_end_date');
    const daysBadge = document.getElementById('calculated_days_badge');

    if (startDateInput && endDateInput && daysBadge) {
        function calculateDays() {
            const startVal = startDateInput.value;
            const endVal = endDateInput.value;
            if (startVal && endVal) {
                const d1 = new Date(startVal);
                const d2 = new Date(endVal);
                const diffTime = d2 - d1;
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

                if (diffDays > 0) {
                    daysBadge.textContent = `${diffDays} Gün Talep Ediliyor`;
                    daysBadge.className = 'badge bg-primary fs-6 px-3 py-2';
                } else {
                    daysBadge.textContent = 'Bitiş tarihi başlangıçtan önce olamaz!';
                    daysBadge.className = 'badge bg-danger fs-6 px-3 py-2';
                }
            }
        }

        startDateInput.addEventListener('change', calculateDays);
        endDateInput.addEventListener('change', calculateDays);
    }
}

// --- BİLDİRİMLERİN OTOMATİK KAPANMASI ---
function initFlashAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });
}

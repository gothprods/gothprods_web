// Countdown Timer Logic for "Caos Sonoro"
document.addEventListener('DOMContentLoaded', () => {
    // Set the date we're counting down to
    const countdownEl = document.getElementById('countdown');
    if (!countdownEl) return;
    const rawDate = countdownEl.getAttribute('data-date');
    if (!rawDate) return;
    
    const countDownDate = new Date(rawDate).getTime();

    // Update the count down every 1 second
    const x = setInterval(function() {

        // Get today's date and time
        const now = new Date().getTime();

        // Find the distance between now and the count down date
        const distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the elements
        document.getElementById("days").innerHTML = days < 10 ? '0'+days : days;
        document.getElementById("hours").innerHTML = hours < 10 ? '0'+hours : hours;
        document.getElementById("minutes").innerHTML = minutes < 10 ? '0'+minutes : minutes;
        document.getElementById("seconds").innerHTML = seconds < 10 ? '0'+seconds : seconds;

        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("countdown").innerHTML = "<div style='color: var(--accent-color); font-size: 2rem; font-weight: bold;'>EL STREAM HA COMENZADO</div>";
        }
    }, 1000);

    // Sidebar Menu Toggle
    const menuToggle = document.getElementById('mobile-menu');
    const closeBtn = document.getElementById('close-menu');
    const sidebarMenu = document.getElementById('sidebar-menu');
    const sidebarLinks = document.querySelectorAll('.sidebar-links a');

    if(menuToggle && sidebarMenu) {
        menuToggle.addEventListener('click', () => {
            sidebarMenu.classList.add('active');
        });
    }

    if(closeBtn && sidebarMenu) {
        closeBtn.addEventListener('click', () => {
            sidebarMenu.classList.remove('active');
        });
    }

    if(sidebarLinks) {
        sidebarLinks.forEach(link => {
            link.addEventListener('click', () => {
                sidebarMenu.classList.remove('active');
            });
        });
    }

    // Review Modal Logic
    const openReviewBtns = document.querySelectorAll('.open-review-modal');
    const closeReviewBtns = document.querySelectorAll('.close-modal');

    openReviewBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = btn.getAttribute('data-target');
            const modal = document.getElementById(targetId);
            if (modal) {
                modal.classList.add('show');
                document.body.style.overflow = 'hidden'; // Prevent background scrolling
            }
        });
    });

    closeReviewBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal');
            if (modal) {
                modal.classList.remove('show');
                document.body.style.overflow = '';
                // Remove hash if closing modal
                if (window.location.hash.startsWith('#article-')) {
                    history.replaceState(null, null, ' ');
                }
            }
        });
    });

    // Check URL for direct link to an item
    const urlParams = new URLSearchParams(window.location.search);
    const itemId = urlParams.get('item');
    if (itemId) {
        const directModal = document.getElementById('dynNewsModal' + itemId);
        if (directModal) {
            directModal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    }

    // Close modal if clicked outside of content
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('show');
            document.body.style.overflow = '';
        }
    });

    // Close modals and sidebar on Escape key press
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' || e.keyCode === 27) {
            // Close any open modals
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                modal.classList.remove('show');
                document.body.style.overflow = '';
            });

            // Close sidebar menu if open
            if (sidebarMenu && sidebarMenu.classList.contains('active')) {
                sidebarMenu.classList.remove('active');
            }
        }
    });
});

window.copyShareLink = function(itemId) {
    const link = window.location.origin + window.location.pathname + '?item=' + itemId;
    navigator.clipboard.writeText(link).then(() => {
        alert('¡Enlace copiado al portapapeles!\n' + link);
    }).catch(err => {
        prompt('Copia este enlace para compartir:', link);
    });
};

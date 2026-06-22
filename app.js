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



    // Review Modal Logic
    const openReviewBtns = document.querySelectorAll('.open-review-modal');
    const closeReviewBtns = document.querySelectorAll('.close-modal');

    openReviewBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = btn.getAttribute('data-target');
            const itemId = btn.getAttribute('data-id');
            const itemType = btn.getAttribute('data-type') || 'content';
            const modal = document.getElementById(targetId);
            if (modal) {
                modal.classList.add('show');
                document.body.style.overflow = 'hidden'; // Prevent background scrolling
                
                // Track view
                if (itemId) {
                    fetch('/api/track_view/' + itemId + '?type=' + itemType, { method: 'POST' })
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                document.querySelectorAll('.view-count-' + itemId + '[data-type="' + itemType + '"]').forEach(el => {
                                    el.innerText = data.views;
                                });
                            }
                        })
                        .catch(err => console.error('Error tracking view:', err));
                        
                    // Load comments
                    loadComments(itemId, itemType);
                }
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

    // Like button logic
    const likeBtns = document.querySelectorAll('.like-btn');
    likeBtns.forEach(btn => {
        const itemId = btn.getAttribute('data-id');
        const itemType = btn.getAttribute('data-type') || 'content';
        // Check local storage
        if (localStorage.getItem('liked_' + itemType + '_' + itemId)) {
            const icon = btn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-regular');
                icon.classList.add('fa-solid');
            }
            btn.style.color = 'var(--accent-color)';
            btn.style.background = 'transparent';
            btn.style.cursor = 'default';
            btn.disabled = true;
        }

        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation(); // prevent opening modal if inside link (though it's not)
            
            if (btn.disabled || localStorage.getItem('liked_' + itemType + '_' + itemId)) return;

            fetch('/api/track_like/' + itemId + '?type=' + itemType, { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        localStorage.setItem('liked_' + itemType + '_' + itemId, 'true');
                        document.querySelectorAll('.like-btn[data-id="' + itemId + '"]').forEach(b => {
                            const bType = b.getAttribute('data-type') || 'content';
                            if (bType !== itemType) return;
                            
                            const icon = b.querySelector('i');
                            if (icon) {
                                icon.classList.remove('fa-regular');
                                icon.classList.add('fa-solid');
                            }
                            b.style.color = 'var(--accent-color)';
                            b.style.background = 'transparent';
                            b.style.cursor = 'default';
                            b.disabled = true;
                        });
                        
                        // Update ALL standalone counts for this type exactly
                        document.querySelectorAll('.like-count-' + itemId + '[data-type="' + itemType + '"]').forEach(el => {
                            el.innerText = data.likes;
                        });
                    }
                })
                .catch(err => console.error('Error tracking like:', err));
        });
    });

    // Check URL for direct link to an item
    const urlParams = new URLSearchParams(window.location.search);
    const directItemId = urlParams.get('item');
    if (directItemId) {
        const directModal = document.getElementById('dynNewsModal' + directItemId);
        if (directModal) {
            directModal.classList.add('show');
            document.body.style.overflow = 'hidden';
            loadComments(directItemId);
        }
    }

    // Close modal if clicked outside of content
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('show');
            document.body.style.overflow = '';
            if (window.location.hash.startsWith('#article-')) {
                history.replaceState(null, null, ' ');
            }
        }
        
        // Close sidebar if clicking outside of it and not on the hamburger menu
        if (sidebarMenu && sidebarMenu.classList.contains('active')) {
            if (!sidebarMenu.contains(e.target) && (!menuToggle || !menuToggle.contains(e.target))) {
                sidebarMenu.classList.remove('active');
            }
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

// Agenda Metalera Tabs Logic
function openAgendaTab(monthName) {
    // Hide all panels
    const panels = document.querySelectorAll('.agenda-month-panel');
    panels.forEach(panel => panel.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.agenda-tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show the selected panel
    const targetPanel = document.getElementById('tab-' + monthName.replace(/ /g, '-'));
    if (targetPanel) {
        targetPanel.classList.add('active');
    }

    // Add active class to clicked button
    const targetBtn = Array.from(buttons).find(btn => btn.getAttribute('data-month') === monthName);
    if (targetBtn) {
        targetBtn.classList.add('active');
    }
}

// Initialize the first valid tab on load
document.addEventListener('DOMContentLoaded', () => {
    // Try to find the first month that is NOT past
    let targetTabBtn = document.querySelector('.agenda-tab-btn:not(.past-month)');
    
    // If all are past, pick the last past month
    if (!targetTabBtn) {
        const allBtns = document.querySelectorAll('.agenda-tab-btn');
        if (allBtns.length > 0) {
            targetTabBtn = allBtns[allBtns.length - 1];
        }
    }
    
    if (targetTabBtn) {
        const monthName = targetTabBtn.getAttribute('data-month');
        if (monthName) {
            openAgendaTab(monthName);
        }
    }
});

// --- Comments Logic ---
window.loadComments = function(itemId, itemType = 'content') {
    const listDiv = document.getElementById('comments-list-' + itemId);
    if (!listDiv) return;
    
    listDiv.innerHTML = '<div style="text-align: center; color: #888; margin-top: 20px;">Cargando comentarios...</div>';
    
    fetch('/api/comments/' + itemId + '?type=' + itemType)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                renderComments(itemId, itemType, data.comments);
            }
        })
        .catch(err => console.error('Error loading comments:', err));
};

function renderComments(itemId, itemType, comments) {
    const listDiv = document.getElementById('comments-list-' + itemId);
    listDiv.innerHTML = '';
    
    if (comments.length === 0) {
        listDiv.innerHTML = '<div style="text-align: center; color: #888; font-size: 0.9rem; margin-top: 20px;">Sé el primero en comentar.</div>';
        return;
    }

    comments.forEach(c => {
        listDiv.appendChild(createCommentElement(c, itemId, itemType, false));
        if (c.replies && c.replies.length > 0) {
            c.replies.forEach(r => {
                listDiv.appendChild(createCommentElement(r, itemId, itemType, true));
            });
        }
    });
    
    // Scroll to bottom
    listDiv.scrollTop = listDiv.scrollHeight;
}

function createCommentElement(c, itemId, itemType, isReply) {
    const div = document.createElement('div');
    div.className = 'comment-bubble' + (isReply ? ' reply' : '');
    
    const date = new Date(c.created_at + 'Z');
    const dateStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    
    const liked = localStorage.getItem('liked_comment_' + c.id);
    const iconClass = liked ? 'fa-solid fa-heart' : 'fa-regular fa-heart';
    const btnClass = liked ? 'liked' : '';
    const disabled = liked ? 'disabled' : '';

    div.innerHTML = `
        <div class="comment-author">
            <span>${escapeHtml(c.author_name)}</span>
            <span class="comment-date">${dateStr}</span>
        </div>
        <div>${escapeHtml(c.content)}</div>
        <div class="comment-actions">
            <button type="button" class="${btnClass}" onclick="likeCommentModal(${c.id}, this)" ${disabled}><i class="${iconClass}"></i> <span class="c-like-count">${c.likes}</span></button>
            ${!isReply ? `<button type="button" onclick="replyTo(${c.id}, '${escapeHtml(c.author_name)}', ${itemId}, '${itemType}')"><i class="fa-solid fa-reply"></i> Responder</button>` : ''}
        </div>
    `;
    return div;
}

window.submitComment = function(e, itemId, itemType = 'content') {
    e.preventDefault();
    const authorInput = document.getElementById('comment-name-' + itemId);
    const textInput = document.getElementById('comment-text-' + itemId);
    const parentInput = document.getElementById('comment-parent-' + itemId);
    
    const author_name = authorInput.value;
    const content = textInput.value;
    const parent_id = parentInput.value || null;
    
    fetch('/api/comments/' + itemId + '?type=' + itemType, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ author_name, content, parent_id })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            textInput.value = '';
            cancelReply(itemId);
            loadComments(itemId, itemType);
        } else {
            alert(data.error || 'Error al publicar comentario');
        }
    })
    .catch(err => console.error('Error posting comment:', err));
};

window.replyTo = function(commentId, authorName, itemId, itemType) {
    const parentInput = document.getElementById('comment-parent-' + itemId);
    const indicator = document.getElementById('replying-to-' + itemId);
    const nameSpan = document.getElementById('replying-name-' + itemId);
    const textInput = document.getElementById('comment-text-' + itemId);
    
    parentInput.value = commentId;
    nameSpan.innerText = 'Respondiendo a ' + authorName;
    indicator.style.display = 'flex';
    textInput.focus();
};

window.cancelReply = function(itemId) {
    document.getElementById('comment-parent-' + itemId).value = '';
    document.getElementById('replying-to-' + itemId).style.display = 'none';
};

window.likeCommentModal = function(commentId, btnEl) {
    if (btnEl.disabled || localStorage.getItem('liked_comment_' + commentId)) return;
    
    fetch('/api/comments/like/' + commentId, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                localStorage.setItem('liked_comment_' + commentId, 'true');
                btnEl.querySelector('.c-like-count').innerText = data.likes;
                btnEl.querySelector('i').classList.remove('fa-regular');
                btnEl.querySelector('i').classList.add('fa-solid');
                btnEl.classList.add('liked');
                btnEl.disabled = true;
            }
        });
};

function escapeHtml(unsafe) {
    return (unsafe || '').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

// gp_metrics.js - Goth Productions Analytics v6.0
(function() {
    // Generate UUID
    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // Get or Create User ID (Persistent)
    var userId = localStorage.getItem('gp_user_id');
    var isNewUser = false;
    if (!userId) {
        userId = generateUUID();
        localStorage.setItem('gp_user_id', userId);
        isNewUser = true;
    }

    // Get or Create Session ID (Session length)
    var sessionId = sessionStorage.getItem('gp_session_id');
    if (!sessionId) {
        sessionId = generateUUID();
        sessionStorage.setItem('gp_session_id', sessionId);
    }

    // Detect Device Type
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    var deviceType = isMobile ? 'mobile' : 'desktop';

    // Get Referrer
    var referrer = document.referrer || '';

    // Analytics State
    var recordId = null;
    var maxScrollDepth = 0;
    var activeSeconds = 0;
    var lastActivityTime = Date.now();
    var MAX_ALLOWED_SECONDS = 600; // Cap at 10 minutes to prevent background/idle tab inflation
    
    // Section Time Tracking
    var sectionTimes = {};
    var currentVisibleSections = new Set();

    // Determine default fallback section based on URL path if no DOM sections trigger
    var path = window.location.pathname.toLowerCase();
    var defaultSection = null;
    if (path.indexOf('/articulo/') !== -1) {
        defaultSection = 'articulo-lectura';
    } else if (path.indexOf('/banda/') !== -1) {
        defaultSection = 'banda-semana';
    } else if (path.indexOf('/evento/') !== -1) {
        defaultSection = 'agenda';
    } else if (path.indexOf('/mexapedia/') !== -1) {
        defaultSection = 'mexapedia';
    }

    // Track user interaction to detect active engagement
    function recordActivity() {
        lastActivityTime = Date.now();
    }

    ['mousemove', 'keydown', 'touchstart', 'scroll', 'click'].forEach(function(evt) {
        window.addEventListener(evt, recordActivity, { passive: true });
    });

    // IntersectionObserver for Section Time / Heatmap
    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                var secId = entry.target.id || entry.target.getAttribute('data-metric-section');
                if (secId) {
                    if (entry.isIntersecting && entry.intersectionRatio >= 0.05) {
                        currentVisibleSections.add(secId);
                    } else {
                        currentVisibleSections.delete(secId);
                    }
                }
            });
        }, { threshold: [0.05, 0.2] });
        
        function observeSections() {
            var sections = document.querySelectorAll('section[id], header[id], div[id^="section-"], article[id], main[id], [data-metric-section]');
            sections.forEach(function(sec) {
                observer.observe(sec);
            });
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', observeSections);
        } else {
            observeSections();
        }
    }

    // 1-second active timer tick
    setInterval(function() {
        if (document.visibilityState !== 'hidden') {
            // Only count if active within last 30 seconds (prevents background/idle tab inflation)
            if (Date.now() - lastActivityTime < 30000 && activeSeconds < MAX_ALLOWED_SECONDS) {
                activeSeconds++;
                if (currentVisibleSections.size > 0) {
                    currentVisibleSections.forEach(function(id) {
                        sectionTimes[id] = Math.min((sectionTimes[id] || 0) + 1, MAX_ALLOWED_SECONDS);
                    });
                } else if (defaultSection) {
                    sectionTimes[defaultSection] = Math.min((sectionTimes[defaultSection] || 0) + 1, MAX_ALLOWED_SECONDS);
                }
            }
        }
    }, 1000);

    // Track scroll depth
    function checkScroll() {
        var h = document.documentElement, 
            b = document.body,
            st = 'scrollTop',
            sh = 'scrollHeight';
        var scrollHeight = (h[sh] || b[sh]) - h.clientHeight;
        if (scrollHeight > 0) {
            var percent = Math.round(((h[st] || b[st]) / scrollHeight) * 100);
            if (percent >= 25 && maxScrollDepth < 25) maxScrollDepth = 25;
            if (percent >= 50 && maxScrollDepth < 50) maxScrollDepth = 50;
            if (percent >= 75 && maxScrollDepth < 75) maxScrollDepth = 75;
            if (percent >= 90 && maxScrollDepth < 100) maxScrollDepth = 100;
        }
    }
    window.addEventListener('scroll', checkScroll, { passive: true });

    // Send payload function
    function sendUpdate(isFinal) {
        if (!recordId) return;
        
        var payload = JSON.stringify({
            record_id: recordId,
            scroll_depth: Math.min(maxScrollDepth, 100),
            time_on_page: Math.min(activeSeconds, MAX_ALLOWED_SECONDS),
            section_times: sectionTimes
        });

        if (isFinal && navigator.sendBeacon) {
            var blob = new Blob([payload], { type: 'application/json' });
            navigator.sendBeacon('/api/analytics/update', blob);
        } else {
            fetch('/api/analytics/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: payload,
                keepalive: true
            }).catch(function(e) {});
        }
    }

    // Initialize analytics immediately
    function initAnalytics(clientCountry) {
        fetch('/api/analytics/init', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                user_id: userId,
                page_url: window.location.href,
                device_type: deviceType,
                country: clientCountry || "Detecting",
                referrer: referrer,
                is_new_user: isNewUser
            })
        })
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (data && data.success) {
                recordId = data.record_id;
                // If we already accumulated initial seconds, send an update
                if (activeSeconds > 0) {
                    sendUpdate(false);
                }
            }
        })
        .catch(function(err) {});
    }

    // Call init immediately without waiting for external geo APIs
    initAnalytics("Detecting");

    // Asynchronously try to get client-side country as supplemental hint (non-blocking)
    try {
        fetch('https://get.geojs.io/v1/ip/geo.json', { cache: 'force-cache' })
            .then(function(res) { return res.json(); })
            .then(function(data) {
                if (data && data.country && recordId) {
                    var cName = data.country;
                    if (cName === 'Mexico') cName = 'México';
                    fetch('/api/analytics/update', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ record_id: recordId, country: cName }),
                        keepalive: true
                    }).catch(function() {});
                }
            })
            .catch(function() {});
    } catch(e) {}

    // Periodically update (every 8 seconds)
    setInterval(function() {
        sendUpdate(false);
    }, 8000);

    // Update on page unload/visibility change
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
            sendUpdate(true);
        }
    });

    window.addEventListener('pagehide', function() {
        sendUpdate(true);
    });

    window.addEventListener('beforeunload', function() {
        sendUpdate(true);
    });

})();

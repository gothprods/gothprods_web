// analytics.js
(function() {
    // Generate UUID
    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // Get or Create User ID (Persistent)
    let userId = localStorage.getItem('gp_user_id');
    let isNewUser = false;
    if (!userId) {
        userId = generateUUID();
        localStorage.setItem('gp_user_id', userId);
        isNewUser = true;
    }

    // Get or Create Session ID (Session length)
    let sessionId = sessionStorage.getItem('gp_session_id');
    if (!sessionId) {
        sessionId = generateUUID();
        sessionStorage.setItem('gp_session_id', sessionId);
    }

    // Detect Device Type
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    const deviceType = isMobile ? 'mobile' : 'desktop';

    // Get Referrer
    const referrer = document.referrer;

    // Analytics State
    let recordId = null;
    let maxScrollDepth = 0;
    let startTime = Date.now();
    let timeOnPage = 0;

    // Track scroll
    window.addEventListener('scroll', () => {
        // Calculate scroll percentage
        let h = document.documentElement, 
            b = document.body,
            st = 'scrollTop',
            sh = 'scrollHeight';
        let percent = Math.round((h[st]||b[st]) / ((h[sh]||b[sh]) - h.clientHeight) * 100);
        
        if (percent >= 25 && maxScrollDepth < 25) maxScrollDepth = 25;
        if (percent >= 50 && maxScrollDepth < 50) maxScrollDepth = 50;
        if (percent >= 75 && maxScrollDepth < 75) maxScrollDepth = 75;
        if (percent >= 90 && maxScrollDepth < 100) maxScrollDepth = 100;
    });

    // Send payload function
    function sendUpdate(isFinal = false) {
        if (!recordId) return;
        timeOnPage = Math.round((Date.now() - startTime) / 1000);
        
        const payload = JSON.stringify({
            record_id: recordId,
            scroll_depth: maxScrollDepth,
            time_on_page: timeOnPage
        });

        if (isFinal && navigator.sendBeacon) {
            navigator.sendBeacon('/api/analytics/update', payload);
        } else {
            fetch('/api/analytics/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: payload,
                keepalive: true
            }).catch(e => console.error(e));
        }
    }

    // Initialize analytics
    function initAnalytics(country = "Unknown") {
        fetch('/api/analytics/init', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                user_id: userId,
                page_url: window.location.pathname + window.location.hash,
                device_type: deviceType,
                country: country,
                referrer: referrer,
                is_new_user: isNewUser
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                recordId = data.record_id;
            }
        })
        .catch(err => console.error("Analytics Init Error:", err));
    }

    // Fetch country and init
    fetch('https://ipapi.co/json/')
        .then(res => res.json())
        .then(data => {
            initAnalytics(data.country_name || data.country || "Unknown");
        })
        .catch(() => {
            // Fallback if IP API fails
            initAnalytics("Unknown");
        });

    // Periodically update (every 15 seconds)
    setInterval(() => {
        sendUpdate(false);
    }, 15000);

    // Update on page unload/hide
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {
            sendUpdate(true);
        }
    });

    window.addEventListener('beforeunload', () => {
        sendUpdate(true);
    });

})();

(function() {
    const Analytics = {
        init: function() {
            console.log('Analytics initialized');
            this.startTime = new Date();
            this.sendData();
            
            // Track page visibility changes
            document.addEventListener('visibilitychange', () => {
                if (document.visibilityState === 'hidden') {
                    this.sendData('exit');
                }
            });

            // Track page unload
            window.addEventListener('beforeunload', () => {
                this.sendData('exit');
            });

            // Update duration periodically
            setInterval(() => {
                if (document.visibilityState === 'visible') {
                    this.sendData('update');
                }
            }, 5000); // Update every 5 seconds
        },

        sendData: function(eventType = 'entry') {
            const data = {
                path: window.location.pathname,
                referrer: document.referrer,
                screenResolution: `${window.screen.width}x${window.screen.height}`,
                eventType: eventType,
                duration: Math.round((new Date() - this.startTime) / 1000),
                timestamp: new Date().toISOString()
            };

            // Use sendBeacon for exit events
            if (eventType === 'exit') {
                navigator.sendBeacon('/analytics/collect', JSON.stringify(data));
                return;
            }

            fetch('/analytics/collect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => console.log('Success:', data))
            .catch(error => console.error('Error:', error));
        }
    };

    Analytics.init();
})();
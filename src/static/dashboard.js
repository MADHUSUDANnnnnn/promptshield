document.addEventListener('DOMContentLoaded', () => {
    // API Configuration
    const API_BASE = 'http://127.0.0.1:5001';

    // DOM Elements
    const alertsBody = document.getElementById('alerts-body');
    const mitigationBody = document.getElementById('mitigation-body');
    
    // Stats elements
    const statTotalScans = document.getElementById('stat-total-scans');
    const statThreatsBlocked = document.getElementById('stat-threats-blocked');
    const statCooldownIps = document.getElementById('stat-cooldown-ips');
    const statBlockedIps = document.getElementById('stat-blocked-ips');

    // Toast Notification System
    function showToast(title, message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = type === 'success' ? '✅' : type === 'danger' ? '🚫' : type === 'warning' ? '⚠️' : 'ℹ️';
        
        toast.innerHTML = `
            <div class="toast-icon">${icon}</div>
            <div class="toast-content">
                <h4>${title}</h4>
                <p>${message}</p>
            </div>
        `;
        
        container.appendChild(toast);
        
        // Remove toast after 4 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s forwards';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // Fetch alerts list from API
    async function fetchAlerts() {
        try {
            const response = await fetch(`${API_BASE}/api/alerts`);
            const data = await response.json();
            
            if (statThreatsBlocked) {
                statThreatsBlocked.textContent = data.length;
            }

            if (!alertsBody) return;

            if (data.length === 0) {
                alertsBody.innerHTML = `<tr><td colspan="6" class="empty-row">No security alerts logged. System secure.</td></tr>`;
                return;
            }

            alertsBody.innerHTML = data.map(alert => {
                let badgeClass = 'none';
                if (alert.risk_level === 'medium') badgeClass = 'medium';
                if (alert.risk_level === 'high') badgeClass = 'high';
                if (alert.risk_level === 'critical') badgeClass = 'critical';

                let actionBadge = 'clean';
                if (alert.mitigation_triggered === 'cooldown') actionBadge = 'flagged';
                if (alert.mitigation_triggered === 'blocked') actionBadge = 'blocked';

                return `
                    <tr>
                        <td>${alert.timestamp}</td>
                        <td style="font-family: var(--font-mono); font-weight: 600;">${alert.ip}</td>
                        <td>${alert.detected_categories.join(', ') || 'N/A'}</td>
                        <td style="font-family: var(--font-mono); font-weight: 600; color: ${alert.risk_score >= 50 ? 'var(--danger-red)' : 'var(--text-main)'}">${alert.risk_score}</td>
                        <td><span class="badge-severity ${badgeClass}">${alert.risk_level}</span></td>
                        <td><span class="badge-status ${actionBadge}">${alert.mitigation_triggered.toUpperCase()}</span></td>
                    </tr>
                `;
            }).join('');

        } catch (error) {
            console.error('Error fetching alerts:', error);
        }
    }

    // Fetch IP registry states from API
    async function fetchIps() {
        try {
            const response = await fetch(`${API_BASE}/api/ips`);
            const data = await response.json();

            let cooldownCount = 0;
            let blockedCount = 0;

            // Compute counts and total scans
            let totalScans = 0;
            data.forEach(ipInfo => {
                totalScans += ipInfo.suspicious_attempts;
                if (ipInfo.status === 'flagged') cooldownCount++;
                if (ipInfo.status === 'blocked') blockedCount++;
            });

            if (statTotalScans) statTotalScans.textContent = totalScans;
            if (statCooldownIps) statCooldownIps.textContent = cooldownCount;
            if (statBlockedIps) statBlockedIps.textContent = blockedCount;

            if (!mitigationBody) return;

            if (data.length === 0) {
                mitigationBody.innerHTML = `<tr><td colspan="5" class="empty-row">No active IP constraints.</td></tr>`;
                return;
            }

            mitigationBody.innerHTML = data.map(ipInfo => {
                let statusClass = 'clean';
                if (ipInfo.status === 'flagged') {
                    statusClass = 'flagged';
                } else if (ipInfo.status === 'blocked') {
                    statusClass = 'blocked';
                }

                const cooldownText = ipInfo.remaining_cooldown > 0 
                    ? `<span style="color: var(--warning-gold); font-family: var(--font-mono); font-weight: 600;">${ipInfo.remaining_cooldown}s</span>` 
                    : 'Expired / None';

                const actionButton = ipInfo.status !== 'clean'
                    ? `<button class="action-btn unblock" onclick="resetIpAddress('${ipInfo.ip}')">Unblock / Reset</button>`
                    : '<span style="color: var(--text-muted);">No action</span>';

                return `
                    <tr>
                        <td style="font-family: var(--font-mono); font-weight: 600;">${ipInfo.ip}</td>
                        <td><span class="badge-status ${statusClass}">${ipInfo.status.toUpperCase()}</span></td>
                        <td>${ipInfo.suspicious_attempts} suspicious checks</td>
                        <td>${cooldownText}</td>
                        <td>${actionButton}</td>
                    </tr>
                `;
            }).join('');

        } catch (error) {
            console.error('Error fetching IPs:', error);
        }
    }

    // Expose resetIpAddress globally so inline onclick handlers can call it
    window.resetIpAddress = async function(ip) {
        try {
            const response = await fetch(`${API_BASE}/api/ip/reset`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ip })
            });
            const result = await response.json();
            
            if (response.ok) {
                showToast('IP Address Reset', `Successfully cleared mitigation rules for ${ip}.`, 'success');
                fetchIps();
                fetchAlerts();
            } else {
                showToast('Reset Failed', result.error || 'Could not reset IP address.', 'danger');
            }
        } catch (error) {
            console.error('Error resetting IP:', error);
            showToast('API Connection Error', 'Could not reach server to reset IP.', 'danger');
        }
    };

    // Auto polling updates
    fetchAlerts();
    fetchIps();
    setInterval(fetchAlerts, 3000);
    setInterval(fetchIps, 3000);
});

// Magic Mirror JavaScript
let currentMode = 'intro';

// Function to switch between modes
function switchMode(mode) {
    document.body.className = mode;
    currentMode = mode;
    
    // Hide all mode-specific content
    const overlay = document.querySelector('.overlay');
    const mirrorFrame = document.querySelector('.mirror-frame');
    const trollContent = document.querySelector('.troll-content');
    
    // Show/hide elements based on mode
    if (overlay) overlay.style.display = mode === 'intro' ? 'flex' : 'none';
    if (mirrorFrame) mirrorFrame.style.display = mode === 'mirror' ? 'block' : 'none';
    if (trollContent) trollContent.style.display = mode === 'troll' ? 'flex' : 'none';
    
    // Update background based on mode
    const background = document.getElementById('background');
    if (background) {
        switch(mode) {
            case 'intro':
                background.style.backgroundImage = "url('images/2.png')";
                background.style.backgroundColor = '';
                background.style.animation = 'rotateBackground 20s linear infinite';
                break;
            case 'mirror':
                background.style.backgroundImage = "url('images/2.jpg')";
                background.style.backgroundColor = '';
                background.style.animation = 'rotateBackground 20s linear infinite';
                break;
            case 'troll':
                background.style.backgroundImage = 'none';
                background.style.backgroundColor = '#000';
                background.style.animation = 'none';
                break;
        }
    }
}

// Camera access for mirror mode
async function startCamera() {
    try {
        const video = document.getElementById('video');
        if (video) {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                } 
            });
            video.srcObject = stream;
            console.log('Camera started successfully');
        }
    } catch (err) {
        console.log('Camera access denied or not available:', err);
        // Show fallback message
        const video = document.getElementById('video');
        if (video) {
            video.style.background = '#333';
            video.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: white; font-family: BaseNeue, Arial, sans-serif;">Camera not available</div>';
        }
    }
}

// Stop camera
function stopCamera() {
    const video = document.getElementById('video');
    if (video && video.srcObject) {
        const tracks = video.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
    }
}

// Auto-progression through modes (for demo purposes)
function startAutoProgression() {
    // Stay on intro for 8 seconds
    setTimeout(() => {
        switchMode('mirror');
        startCamera();
    }, 8000);
    
    // Switch to troll mode after 15 seconds total
    setTimeout(() => {
        stopCamera();
        switchMode('troll');
        
        // Animate the mass meter after switching
        setTimeout(() => {
            const fill = document.querySelector('.fill');
            if (fill) {
                fill.style.width = '75%';
            }
        }, 1000);
    }, 15000);
    
    // Loop back to intro after 25 seconds
    setTimeout(() => {
        switchMode('intro');
        // Reset meter
        const fill = document.querySelector('.fill');
        if (fill) {
            fill.style.width = '0%';
        }
        // Restart the cycle
        startAutoProgression();
    }, 25000);
}

// Manual controls for testing
document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case '1':
            switchMode('intro');
            stopCamera();
            // Reset meter
            const fill1 = document.querySelector('.fill');
            if (fill1) fill1.style.width = '0%';
            break;
        case '2':
            switchMode('mirror');
            startCamera();
            break;
        case '3':
            switchMode('troll');
            stopCamera();
            setTimeout(() => {
                const fill3 = document.querySelector('.fill');
                if (fill3) fill3.style.width = '75%';
            }, 500);
            break;
        case 'r':
        case 'R':
            // Restart auto-progression
            location.reload();
            break;
    }
});

// Touch/click controls for mobile
let touchStartTime = 0;
document.addEventListener('touchstart', () => {
    touchStartTime = Date.now();
});

document.addEventListener('touchend', (e) => {
    const touchDuration = Date.now() - touchStartTime;
    if (touchDuration < 500) { // Quick tap
        switch(currentMode) {
            case 'intro':
                switchMode('mirror');
                startCamera();
                break;
            case 'mirror':
                switchMode('troll');
                stopCamera();
                setTimeout(() => {
                    const fill = document.querySelector('.fill');
                    if (fill) fill.style.width = '75%';
                }, 500);
                break;
            case 'troll':
                switchMode('intro');
                const fill = document.querySelector('.fill');
                if (fill) fill.style.width = '0%';
                break;
        }
    }
});

// Handle visibility change (when tab becomes inactive/active)
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Pause animations when tab is not visible
        const background = document.getElementById('background');
        if (background) {
            background.style.animationPlayState = 'paused';
        }
    } else {
        // Resume animations when tab becomes visible
        const background = document.getElementById('background');
        if (background && currentMode !== 'troll') {
            background.style.animationPlayState = 'running';
        }
    }
});

// Font loading check
function checkFontsLoaded() {
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(() => {
            console.log('Custom fonts loaded successfully');
        });
    }
    
    // Fallback check after 3 seconds
    setTimeout(() => {
        const testElement = document.createElement('div');
        testElement.style.fontFamily = 'BaseNeue';
        testElement.style.position = 'absolute';
        testElement.style.visibility = 'hidden';
        testElement.innerHTML = 'Test';
        document.body.appendChild(testElement);
        
        const computedFont = getComputedStyle(testElement).fontFamily;
        if (!computedFont.includes('BaseNeue')) {
            console.warn('BaseNeue font may not have loaded properly');
        }
        
        document.body.removeChild(testElement);
    }, 3000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Magic Mirror initialized');
    checkFontsLoaded();
    
    // Start auto-progression
    startAutoProgression();
    
    // Ensure intro mode is active
    switchMode('intro');
});

// Handle errors
window.addEventListener('error', (e) => {
    console.error('Error occurred:', e.error);
});

// Export functions for external use
window.MagicMirror = {
    switchMode,
    startCamera,
    stopCamera,
    startAutoProgression
};
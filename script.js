// --- Image Capture & Prediction ---
function sendImageToServer(blob) {
    const formData = new FormData();
    formData.append('image', blob, 'webcam.jpg');

    fetch('https://magicmirror-cnf3.onrender.com/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    })
    .catch(error => console.error('Error sending image:', error));
}

function captureAndSend(video) {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(sendImageToServer, 'image/jpeg');
}

// --- Camera Setup ---
let captureInterval;

async function startCamera() {
    try {
        const video = document.getElementById('video');
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // Start prediction loop every 5 seconds
        if (captureInterval) clearInterval(captureInterval);
        captureInterval = setInterval(() => {
            captureAndSend(video);
        }, 5000);

        console.log('Camera started');
    } catch (err) {
        console.error('Camera access failed:', err);
    }
}

function stopCamera() {
    const video = document.getElementById('video');
    if (video && video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
        video.srcObject = null;
    }
    if (captureInterval) clearInterval(captureInterval);
}

// --- Mode Switching ---
let currentMode = 'intro';

function switchMode(mode) {
    document.body.className = mode;
    currentMode = mode;

    const overlay = document.querySelector('.overlay');
    const mirrorFrame = document.querySelector('.mirror-frame');
    const trollContent = document.querySelector('.troll-content');

    overlay.style.display = mode === 'intro' ? 'flex' : 'none';
    mirrorFrame.style.display = mode === 'mirror' ? 'block' : 'none';
    trollContent.style.display = mode === 'troll' ? 'flex' : 'none';

    const background = document.getElementById('background');
    if (background) {
        switch (mode) {
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

    // Camera control
    if (mode === 'mirror') startCamera();
    else stopCamera();

    // Troll mode meter
    if (mode === 'troll') {
        setTimeout(() => {
            const fill = document.querySelector('.fill');
            if (fill) fill.style.width = '75%';
        }, 1000);
    } else {
        const fill = document.querySelector('.fill');
        if (fill) fill.style.width = '0%';
    }
}

// --- Auto Progression ---
function startAutoProgression() {
    setTimeout(() => switchMode('mirror'), 8000);
    setTimeout(() => switchMode('troll'), 15000);
    setTimeout(() => {
        switchMode('intro');
        startAutoProgression();
    }, 25000);
}

// --- Manual Controls ---
document.addEventListener('keydown', e => {
    if (e.key === '1') switchMode('intro');
    if (e.key === '2') switchMode('mirror');
    if (e.key === '3') switchMode('troll');
    if (e.key.toLowerCase() === 'r') location.reload();
});

// --- Touch Controls ---
let touchStartTime = 0;

document.addEventListener('touchstart', () => {
    touchStartTime = Date.now();
});

document.addEventListener('touchend', () => {
    const duration = Date.now() - touchStartTime;
    if (duration < 500) {
        if (currentMode === 'intro') switchMode('mirror');
        else if (currentMode === 'mirror') switchMode('troll');
        else switchMode('intro');
    }
});

// --- Visibility Handling ---
document.addEventListener('visibilitychange', () => {
    const background = document.getElementById('background');
    if (background) {
        background.style.animationPlayState = document.hidden ? 'paused' : 'running';
    }
});

// --- Font Check ---
function checkFontsLoaded() {
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(() => {
            console.log('Fonts loaded');
        });
    }

    setTimeout(() => {
        const testEl = document.createElement('div');
        testEl.style.fontFamily = 'BaseNeue';
        testEl.style.position = 'absolute';
        testEl.style.visibility = 'hidden';
        testEl.textContent = 'Test';
        document.body.appendChild(testEl);

        const computed = getComputedStyle(testEl).fontFamily;
        if (!computed.includes('BaseNeue')) {
            console.warn('BaseNeue may not have loaded');
        }
        document.body.removeChild(testEl);
    }, 3000);
}

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    switchMode('intro');
    checkFontsLoaded();
    startAutoProgression();
    console.log('Magic Mirror initialized');
});

// --- Error Logging ---
window.addEventListener('error', e => {
    console.error('Global error:', e.error);
});

// --- Export (if needed globally) ---
window.MagicMirror = {
    switchMode,
    startCamera,
    stopCamera,
    startAutoProgression
};

/* ==================================================
   THREE.JS 3D BACKGROUND ANIMATION
   ================================================== */
const canvas = document.getElementById('bg-canvas');
const scene = new THREE.Scene();

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 50;

// Renderer setup
const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // optimize for high DPI but limit to 2

// Particles Setup (Neural Network vibe)
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 700;

const posArray = new Float32Array(particlesCount * 3);
const colorsArray = new Float32Array(particlesCount * 3);

const color1 = new THREE.Color(0x00f0ff); // Cyan
const color2 = new THREE.Color(0x7000ff); // Purple

for(let i = 0; i < particlesCount * 3; i+=3) {
    // Spread particles in a large area
    posArray[i] = (Math.random() - 0.5) * 150;     // x
    posArray[i+1] = (Math.random() - 0.5) * 150;   // y
    posArray[i+2] = (Math.random() - 0.5) * 100;   // z

    // Mix colors
    const mixedColor = color1.clone().lerp(color2, Math.random());
    colorsArray[i] = mixedColor.r;
    colorsArray[i+1] = mixedColor.g;
    colorsArray[i+2] = mixedColor.b;
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorsArray, 3));

// Material for particles
const particlesMaterial = new THREE.PointsMaterial({
    size: 0.4,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
});

// Create Point Cloud
const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

// Connecting Lines (Optional for deeper tech feel)
const lineMaterial = new THREE.LineBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.05
});

// Mouse Interaction
let mouseX = 0;
let mouseY = 0;
let targetX = 0;
let targetY = 0;

const windowHalfX = window.innerWidth / 2;
const windowHalfY = window.innerHeight / 2;

document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX - windowHalfX);
    mouseY = (event.clientY - windowHalfY);
});

// Handle Resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Animation Loop
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    // Slow rotation
    particlesMesh.rotation.y = elapsedTime * 0.05;
    particlesMesh.rotation.x = elapsedTime * 0.02;

    // Subtle floating wave effect based on time
    const positions = particlesGeometry.attributes.position.array;
    for(let i = 0; i < particlesCount; i++) {
        const i3 = i * 3;
        const x = positions[i3];
        const y = positions[i3 + 1];
        // Don't modify base positions too much, just a tiny wave
    }
    particlesGeometry.attributes.position.needsUpdate = true;

    // Mouse interactive rotation targeting
    targetX = mouseX * 0.001;
    targetY = mouseY * 0.001;

    // Smooth lerp to target
    particlesMesh.rotation.y += 0.05 * (targetX - particlesMesh.rotation.y);
    particlesMesh.rotation.x += 0.05 * (targetY - particlesMesh.rotation.x);

    renderer.render(scene, camera);
}
animate();

/* ==================================================
   FORM HANDLING & API INTEGRATION
   ================================================== */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const modal = document.getElementById('result-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const loadingOverlay = document.getElementById('loading-overlay');
    const statusBadge = document.getElementById('result-status');
    const confidenceSpan = document.querySelector('#result-confidence span');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show Loader
        loadingOverlay.classList.remove('hidden');

        // Gather Data
        const payload = {
            CGPA: parseFloat(document.getElementById('CGPA').value),
            Internships: parseInt(document.getElementById('Internships').value),
            Projects: parseInt(document.getElementById('Projects').value),
            "Workshops/Certifications": parseInt(document.getElementById('Workshops').value),
            AptitudeTestScore: parseFloat(document.getElementById('AptitudeTestScore').value),
            SoftSkillsRating: parseFloat(document.getElementById('SoftSkillsRating').value),
            ExtracurricularActivities: document.getElementById('Extracurricular').value,
            PlacementTraining: document.getElementById('PlacementTraining').value,
            SSC_Marks: parseFloat(document.getElementById('SSC_Marks').value),
            HSC_Marks: parseFloat(document.getElementById('HSC_Marks').value)
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();

            // Populate Modal
            statusBadge.textContent = data.result;
            statusBadge.className = 'status-badge ' + (data.result === 'Placed' ? 'placed' : 'not-placed');
            confidenceSpan.textContent = data.confidence;

            // Hide Loader, Show Modal
            loadingOverlay.classList.add('hidden');
            modal.classList.remove('hidden');

            // Trigger a 3D effect burst on success
            if(data.result === 'Placed') {
                // Temporary speed up in particles to simulate excitement
                particlesMesh.material.color.setHex(0x00ff88);
            } else {
                particlesMesh.material.color.setHex(0xff3366);
            }
            
            // Reset color after a few seconds
            setTimeout(() => {
                particlesMesh.material.color.setHex(0xffffff);
            }, 3000);

        } catch (error) {
            console.error('Error:', error);
            loadingOverlay.classList.add('hidden');
            alert('Failed to get prediction. Ensure the backend server is running.');
        }
    });

    closeModalBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    // Close modal on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
});

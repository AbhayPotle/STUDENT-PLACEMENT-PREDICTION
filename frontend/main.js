import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

/* ==================================================
   THREE.JS 3D BACKGROUND ANIMATION - CINEMATIC UPGRADE
   ================================================== */
const canvas = document.getElementById('bg-canvas');
const scene = new THREE.Scene();

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 60;

// Renderer setup
const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ReinhardToneMapping;

// Post-Processing (Bloom)
const renderScene = new RenderPass(scene, camera);
const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    1.5, // strength
    0.4, // radius
    0.85 // threshold
);
bloomPass.strength = 1.2;
bloomPass.radius = 0.5;
bloomPass.threshold = 0;

const composer = new EffectComposer(renderer);
composer.addPass(renderScene);
composer.addPass(bloomPass);

// Lighting
const ambientLight = new THREE.AmbientLight(0x111122, 1.5);
scene.add(ambientLight);

const pointLight1 = new THREE.PointLight(0x00f0ff, 200, 150);
pointLight1.position.set(20, 20, 20);
scene.add(pointLight1);

const pointLight2 = new THREE.PointLight(0x7000ff, 200, 150);
pointLight2.position.set(-20, -20, 20);
scene.add(pointLight2);

// The Data Core (Central Icosahedron)
const coreGeometry = new THREE.IcosahedronGeometry(15, 2);
const coreMaterial = new THREE.MeshStandardMaterial({
    color: 0x050505,
    emissive: 0x00f0ff,
    emissiveIntensity: 0.2,
    wireframe: true,
    roughness: 0.2,
    metalness: 0.8
});
const dataCore = new THREE.Mesh(coreGeometry, coreMaterial);
scene.add(dataCore);

// Inner Core (Solid)
const innerGeometry = new THREE.IcosahedronGeometry(10, 1);
const innerMaterial = new THREE.MeshStandardMaterial({
    color: 0x111111,
    emissive: 0x7000ff,
    emissiveIntensity: 0.5,
    roughness: 0.1,
    metalness: 1.0
});
const innerCore = new THREE.Mesh(innerGeometry, innerMaterial);
dataCore.add(innerCore);

// Floating Data Particles around the core
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 1000;
const posArray = new Float32Array(particlesCount * 3);
const colorsArray = new Float32Array(particlesCount * 3);

const color1 = new THREE.Color(0x00f0ff);
const color2 = new THREE.Color(0x7000ff);

for(let i = 0; i < particlesCount * 3; i+=3) {
    // Generate particles in a spherical distribution
    const radius = 25 + Math.random() * 40;
    const theta = Math.random() * 2 * Math.PI;
    const phi = Math.acos(2 * Math.random() - 1);
    
    posArray[i] = radius * Math.sin(phi) * Math.cos(theta);
    posArray[i+1] = radius * Math.sin(phi) * Math.sin(theta);
    posArray[i+2] = radius * Math.cos(phi);

    const mixedColor = color1.clone().lerp(color2, Math.random());
    colorsArray[i] = mixedColor.r;
    colorsArray[i+1] = mixedColor.g;
    colorsArray[i+2] = mixedColor.b;
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorsArray, 3));

const particlesMaterial = new THREE.PointsMaterial({
    size: 0.3,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
});

const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

// Mouse Interaction & Parallax
let mouseX = 0;
let mouseY = 0;
let targetX = 0;
let targetY = 0;

const windowHalfX = window.innerWidth / 2;
const windowHalfY = window.innerHeight / 2;

document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX - windowHalfX);
    mouseY = (event.clientY - windowHalfY);
    
    // 3D Tilt Effect for Form Container
    const formContainer = document.querySelector('.main-container');
    if (formContainer) {
        const tiltX = (mouseY / windowHalfY) * -5;
        const tiltY = (mouseX / windowHalfX) * 5;
        formContainer.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale3d(1.02, 1.02, 1.02)`;
    }
});

// Reset tilt when mouse leaves
document.addEventListener('mouseleave', () => {
    const formContainer = document.querySelector('.main-container');
    if (formContainer) {
        formContainer.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    }
});

// Handle Resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
});

// Animation Loop
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    // Rotate Data Core
    dataCore.rotation.y = elapsedTime * 0.2;
    dataCore.rotation.x = elapsedTime * 0.1;
    innerCore.rotation.y = elapsedTime * -0.3;
    innerCore.rotation.z = elapsedTime * 0.15;

    // Rotate Particle Field slowly
    particlesMesh.rotation.y = elapsedTime * -0.05;

    // Mouse interactive rotation targeting for camera/scene parallax
    targetX = mouseX * 0.002;
    targetY = mouseY * 0.002;

    scene.rotation.y += 0.05 * (targetX - scene.rotation.y);
    scene.rotation.x += 0.05 * (targetY - scene.rotation.x);
    
    // Pulse inner core emissive intensity
    innerMaterial.emissiveIntensity = 0.5 + Math.sin(elapsedTime * 2) * 0.3;

    // Use Composer instead of Renderer
    composer.render();
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
    const insightsContainer = document.getElementById('insights-container');
    const insightsList = document.getElementById('insights-list');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Excitement animation before request
        bloomPass.strength = 3.0; // Overdrive bloom
        coreMaterial.emissiveIntensity = 1.0;
        
        loadingOverlay.classList.remove('hidden');

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
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error('Network error');

            const data = await response.json();

            statusBadge.textContent = data.result;
            statusBadge.className = 'status-badge ' + (data.result === 'Placed' ? 'placed' : 'not-placed');
            confidenceSpan.textContent = data.confidence;

            // Handle Insights
            insightsList.innerHTML = ''; // clear previous
            if (data.insights && data.insights.length > 0) {
                data.insights.forEach(insight => {
                    const li = document.createElement('li');
                    li.textContent = insight;
                    insightsList.appendChild(li);
                });
                insightsContainer.classList.remove('hidden');
            } else {
                insightsContainer.classList.add('hidden');
            }

            loadingOverlay.classList.add('hidden');
            modal.classList.remove('hidden');

            // Result Cinematic Reaction
            if(data.result === 'Placed') {
                coreMaterial.emissive.setHex(0x00ff88);
                innerMaterial.emissive.setHex(0x00ff88);
                pointLight1.color.setHex(0x00ff88);
                bloomPass.strength = 2.5;
            } else {
                coreMaterial.emissive.setHex(0xff3366);
                innerMaterial.emissive.setHex(0xff3366);
                pointLight1.color.setHex(0xff3366);
                bloomPass.strength = 2.5;
            }
            
            // Cooldown effect
            setTimeout(() => {
                coreMaterial.emissive.setHex(0x00f0ff);
                innerMaterial.emissive.setHex(0x7000ff);
                pointLight1.color.setHex(0x00f0ff);
                bloomPass.strength = 1.2;
                coreMaterial.emissiveIntensity = 0.2;
            }, 4000);

        } catch (error) {
            console.error('Error:', error);
            loadingOverlay.classList.add('hidden');
            alert('Failed to get prediction. Ensure backend is running.');
            bloomPass.strength = 1.2; // Reset on error
            coreMaterial.emissiveIntensity = 0.2;
        }
    });

    closeModalBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.classList.add('hidden');
    });
});

import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

/* ==================================================
   THREE.JS 3D BACKGROUND ANIMATION - HOLOGRAPHIC CORE
   ================================================== */
const canvas = document.getElementById('bg-canvas');
const scene = new THREE.Scene();

// Camera setup
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
// Move camera to the right so the core isn't hidden behind the main form
camera.position.z = 50;
camera.position.x = -15;

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
const coreGeometry = new THREE.IcosahedronGeometry(12, 2);
const coreMaterial = new THREE.MeshStandardMaterial({
    color: 0x050505,
    emissive: 0x00f0ff,
    emissiveIntensity: 0.2,
    wireframe: true,
    roughness: 0.2,
    metalness: 0.8
});
const dataCore = new THREE.Mesh(coreGeometry, coreMaterial);
// Position it to the right background for the dashboard layout
dataCore.position.x = 25;
scene.add(dataCore);

// Inner Core (Solid)
const innerGeometry = new THREE.IcosahedronGeometry(8, 1);
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
const particlesCount = 800;
const posArray = new Float32Array(particlesCount * 3);
const colorsArray = new Float32Array(particlesCount * 3);

const color1 = new THREE.Color(0x00f0ff);
const color2 = new THREE.Color(0x7000ff);

for(let i = 0; i < particlesCount * 3; i+=3) {
    const radius = 20 + Math.random() * 30;
    const theta = Math.random() * 2 * Math.PI;
    const phi = Math.acos(2 * Math.random() - 1);
    
    // Shift particle origin to the right
    posArray[i] = (radius * Math.sin(phi) * Math.cos(theta)) + 25;
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

// Mouse Interaction Parallax
let mouseX = 0;
let mouseY = 0;
let targetX = 0;
let targetY = 0;

const windowHalfX = window.innerWidth / 2;
const windowHalfY = window.innerHeight / 2;

document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX - windowHalfX);
    mouseY = (event.clientY - windowHalfY);

    // Full Dashboard 3D Parallax Tilt
    const dashboard = document.querySelector('.dashboard-layout');
    if (dashboard) {
        // Subtle tilt values for professional look
        const tiltX = (mouseY / windowHalfY) * -3; 
        const tiltY = (mouseX / windowHalfX) * 3;
        dashboard.style.transform = `perspective(1500px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale3d(1.01, 1.01, 1.01)`;
    }
});

// Reset tilt on mouse leave
document.addEventListener('mouseleave', () => {
    const dashboard = document.querySelector('.dashboard-layout');
    if (dashboard) {
        dashboard.style.transform = 'perspective(1500px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
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

    // Camera Parallax based on mouse
    targetX = mouseX * 0.001;
    targetY = mouseY * 0.001;

    scene.rotation.y += 0.05 * (targetX - scene.rotation.y);
    scene.rotation.x += 0.05 * (targetY - scene.rotation.x);
    
    // Pulse inner core
    innerMaterial.emissiveIntensity = 0.5 + Math.sin(elapsedTime * 2) * 0.3;

    composer.render();
}
animate();

/* ==================================================
   FORM HANDLING & API INTEGRATION (DASHBOARD)
   ================================================== */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Sidebar elements
    const analyticsWidget = document.getElementById('analytics-widget');
    const statusBadge = document.getElementById('result-status');
    const confidenceSpan = document.querySelector('#result-confidence span');
    const companyBadge = document.getElementById('predicted-company');
    
    // Analytics Panel Elements
    const analyticsPanel = document.getElementById('analytics-panel');
    const jobFitDesc = document.getElementById('job-fit-description');
    const insightsList = document.getElementById('insights-list');

    // Dynamic Education Path Toggle
    const edPathSelect = document.getElementById('education_path');
    const interFields = document.querySelectorAll('.dynamic-inter');
    const diplomaFields = document.querySelectorAll('.dynamic-diploma');
    const interInputs = [document.getElementById('inter_1'), document.getElementById('inter_2')];
    const diplomaInput = document.getElementById('diploma_marks');

    edPathSelect.addEventListener('change', (e) => {
        if (e.target.value === 'intermediate') {
            interFields.forEach(el => el.classList.remove('hidden'));
            diplomaFields.forEach(el => el.classList.add('hidden'));
            interInputs.forEach(i => i.required = true);
            diplomaInput.required = false;
        } else {
            interFields.forEach(el => el.classList.add('hidden'));
            diplomaFields.forEach(el => el.classList.remove('hidden'));
            interInputs.forEach(i => i.required = false);
            diplomaInput.required = true;
        }
    });
    // Trigger change initially to set correct required attributes
    edPathSelect.dispatchEvent(new Event('change'));

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Excitement animation
        bloomPass.strength = 3.0; 
        coreMaterial.emissiveIntensity = 1.0;
        
        loadingOverlay.classList.remove('hidden');

        const edPath = document.getElementById('education_path').value;
        const inter1 = document.getElementById('inter_1').value;
        const inter2 = document.getElementById('inter_2').value;
        const diploma = document.getElementById('diploma_marks').value;

        const payload = {
            current_course: document.getElementById('current_course').value,
            education_path: edPath,
            inter_1: inter1 ? parseFloat(inter1) : null,
            inter_2: inter2 ? parseFloat(inter2) : null,
            diploma_marks: diploma ? parseFloat(diploma) : null,

            board_10th: document.getElementById('board_10th').value,
            CGPA: parseFloat(document.getElementById('CGPA').value),
            SSC_Marks: parseFloat(document.getElementById('SSC_Marks').value),
            Projects: parseInt(document.getElementById('Projects').value),
            Internships: parseInt(document.getElementById('Internships').value),
            "Workshops/Certifications": parseInt(document.getElementById('Workshops').value),
            
            key_skills: document.getElementById('key_skills').value,
            target_job_description: document.getElementById('target_job_description').value,
            work_experience: document.getElementById('work_experience').value,
            certification_details: document.getElementById('certification_details').value,
            
            ExtracurricularActivities: document.getElementById('Extracurricular').value,
            PlacementTraining: document.getElementById('PlacementTraining').value
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error('Network error');

            const data = await response.json();

            // Populate Sidebar Widget
            statusBadge.textContent = data.result;
            statusBadge.className = 'status-badge ' + (data.result === 'Placed' ? 'placed' : 'not-placed');
            confidenceSpan.textContent = data.confidence;
            companyBadge.textContent = data.predicted_company;
            analyticsWidget.classList.remove('hidden');

            // Populate Analytics Panel
            jobFitDesc.textContent = data.job_fit_description;
            
            insightsList.innerHTML = '';
            if (data.insights && data.insights.length > 0) {
                data.insights.forEach(insight => {
                    const li = document.createElement('li');
                    li.textContent = insight;
                    insightsList.appendChild(li);
                });
            }
            analyticsPanel.classList.remove('hidden');

            loadingOverlay.classList.add('hidden');

            // Result Cinematic Reaction
            if(data.result === 'Placed') {
                coreMaterial.emissive.setHex(0x00ff88);
                innerMaterial.emissive.setHex(0x00ff88);
                pointLight1.color.setHex(0x00ff88);
                bloomPass.strength = 2.0;
            } else {
                coreMaterial.emissive.setHex(0xff3366);
                innerMaterial.emissive.setHex(0xff3366);
                pointLight1.color.setHex(0xff3366);
                bloomPass.strength = 2.0;
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
            bloomPass.strength = 1.2;
            coreMaterial.emissiveIntensity = 0.2;
        }
    });
});

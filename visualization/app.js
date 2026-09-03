import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const planes = [
  { id: 'capability', label: 'Capability library', color: '#6bc7ff', description: 'The functional reference: Industrial Engineering, QA, Production, Aerospace, Program, Materials, Reliability, and Digital Operations.', docs: [
    ['Industrial Engineering', 16], ['Aerospace Manufacturing', 10], ['Quality Assurance', 9], ['Production Management', 9], ['Program Management', 7], ['Materials & Supply Chain', 7], ['Maintenance & Reliability', 7], ['Digital Operations & Data', 7],
  ]},
  { id: 'process', label: 'Process plane', color: '#b08cff', description: 'Cross-functional work flows. A process selects the relevant capability playbooks and carries the case across handoffs.', docs: [
    ['Commitment → Ready Work', 1], ['Build → Acceptance', 1], ['Exception → Disposition', 1], ['Change → Effective Control', 1], ['Constraint → Recovery', 1], ['Asset Loss → Reliability', 1], ['Decision → Data Product', 1],
  ]},
  { id: 'agents', label: 'Process agents', color: '#7fe29b', description: 'Future harness-facing roles. Each card states inputs, allowed actions, specialist critics, escalation gates, and outputs.', docs: [
    ['Readiness', 1], ['Conformance', 1], ['Exception', 1], ['Change-impact', 1], ['Recovery', 1], ['Reliability', 1], ['Decision-intelligence', 1],
  ]},
  { id: 'authority', label: 'Authority gates', color: '#ffd166', description: 'The human decision boundaries agents cannot cross: release, disposition, compliance, change, commitment, return-to-service, and access.', docs: [['Decision rights', 1], ['Specialist critics', 1], ['ADR: process agents', 1]] },
  { id: 'learning', label: 'Learning & templates', color: '#ff8f70', description: 'Discovery patterns, local learning inputs, and reusable field artifacts. This is where future sanitized observations enter.', docs: [['Discovery patterns', 8], ['Operational templates', 14], ['Reference vs. reality ledger', 1], ['Next items plan', 1]] },
  { id: 'governance', label: 'Governance kernel', color: '#f58ad8', description: 'The planned layer that will classify reference, baseline, observation, and adopted practice; govern supersession, review, and agent evaluation.', docs: [['Corpus quality bar', 1], ['Architecture decisions', 3], ['Next-items kernel plan', 8]] },
  { id: 'automation', label: 'Optional automation', color: '#69d7d2', description: 'A future implementation seed: schemas, fixtures, integrity checks, adapter and MCP contracts. Not required to use the Markdown corpus.', docs: [['Schemas', 3], ['Fixture case', 4], ['Integrity tests', 2], ['MCP contract', 1], ['CSV adapter', 1], ['Reference architecture', 3]] },
];

const canvas = document.querySelector('#scene');
const panelTitle = document.querySelector('#title');
const panelDescription = document.querySelector('#description');
const facts = document.querySelector('#facts');
const tooltip = document.querySelector('#tooltip');
const legend = document.querySelector('#legend');

const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a1020');
scene.fog = new THREE.FogExp2('#0a1020', 0.00055);
const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 1, 3000);
camera.position.set(0, 240, 930);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setAnimationLoop(render);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = .06;
controls.minDistance = 180;
controls.maxDistance = 1500;
controls.target.set(0, 0, 0);

scene.add(new THREE.HemisphereLight('#a9c8ff', '#0a1022', 2.2));
const raycaster = new THREE.Raycaster();
raycaster.params.Points.threshold = 18;
const pointer = new THREE.Vector2();
const selectable = [];
const focus = { target: new THREE.Vector3(), position: new THREE.Vector3(), active: false };

function color(hex) { return new THREE.Color(hex); }
function makeLabel(text, hex, position) {
  const canvas = document.createElement('canvas');
  canvas.width = 512; canvas.height = 96;
  const context = canvas.getContext('2d');
  context.font = '700 32px system-ui'; context.textAlign = 'center';
  context.fillStyle = hex; context.fillText(text.toUpperCase(), 256, 58);
  const texture = new THREE.CanvasTexture(canvas);
  const material = new THREE.SpriteMaterial({ map: texture, transparent: true, opacity: 1, depthWrite: false, depthTest: false, fog: false });
  const sprite = new THREE.Sprite(material);
  sprite.position.copy(position); sprite.position.y += 76;
  sprite.scale.set(155, 29, 1); scene.add(sprite);
}
function edge(a, b, hex, opacity = .22) {
  const geometry = new THREE.BufferGeometry().setFromPoints([a, b]);
  const material = new THREE.LineBasicMaterial({ color: hex, transparent: true, opacity });
  scene.add(new THREE.Line(geometry, material));
}
function setPanel(data) {
  panelTitle.textContent = data.label;
  panelDescription.textContent = data.description;
  facts.innerHTML = `<div><dt>PLANE</dt><dd>${data.plane || 'Corpus overview'}</dd></div><div><dt>REPRESENTS</dt><dd>${data.detail || 'DigitalIE architecture and its connected documentation.'}</dd></div>`;
}
function focusOn(position, data) {
  focus.target.copy(position);
  focus.position.copy(position).add(new THREE.Vector3(0, 64, 220));
  focus.active = true; setPanel(data);
}

const root = new THREE.Group(); scene.add(root);
const rootSphere = new THREE.Mesh(
  new THREE.IcosahedronGeometry(25, 2), new THREE.MeshStandardMaterial({ color: '#f3f8ff', emissive: '#6bc7ff', emissiveIntensity: 1.7, roughness: .35 }),
);
rootSphere.userData = { label: 'DigitalIE', description: 'The clean-room manufacturing operations corpus. Click a district to examine its role.', plane: 'Root', detail: 'Capability library × process plane × authority gates' };
root.add(rootSphere); selectable.push(rootSphere);

planes.forEach((plane, index) => {
  const theta = (index / planes.length) * Math.PI * 2 - Math.PI / 2;
  const district = new THREE.Vector3(Math.cos(theta) * 300, (index % 2 ? 45 : -45), Math.sin(theta) * 300);
  const group = new THREE.Group(); group.position.copy(district); root.add(group);
  const districtNode = new THREE.Mesh(
    new THREE.IcosahedronGeometry(20, 2), new THREE.MeshStandardMaterial({ color: plane.color, emissive: plane.color, emissiveIntensity: 1.7, roughness: .42 }),
  );
  districtNode.userData = { label: plane.label, description: plane.description, plane: 'Corpus district', detail: `${plane.docs.length} document clusters` };
  group.add(districtNode); selectable.push(districtNode); edge(new THREE.Vector3(), district, plane.color, .36);
  makeLabel(plane.label, plane.color, district);
  const count = plane.docs.length;
  plane.docs.forEach(([label, pages], docIndex) => {
    const angle = (docIndex / count) * Math.PI * 2;
    const radial = 74 + (docIndex % 2) * 22;
    const local = new THREE.Vector3(Math.cos(angle) * radial, Math.sin(angle * 2.3) * 20, Math.sin(angle) * radial);
    const node = new THREE.Mesh(
      new THREE.SphereGeometry(4 + Math.min(pages, 16) * .55, 18, 18),
      new THREE.MeshStandardMaterial({ color: plane.color, emissive: plane.color, emissiveIntensity: 1.1, roughness: .48 }),
    );
    node.position.copy(local);
    node.userData = { label, description: `${pages} represented document${pages === 1 ? '' : 's'} in the ${plane.label} district.`, plane: plane.label, detail: `Click to focus · derived from repository structure` };
    group.add(node); selectable.push(node); edge(district, district.clone().add(local), plane.color, .16);
  });
});

planes.forEach((plane) => {
  const row = document.createElement('div'); row.className = 'legend-row';
  row.innerHTML = `<span class="dot" style="background:${plane.color}"></span>${plane.label}`;
  legend.append(row);
});

function pick(event, click = false) {
  pointer.x = (event.clientX / innerWidth) * 2 - 1;
  pointer.y = -(event.clientY / innerHeight) * 2 + 1;
  raycaster.setFromCamera(pointer, camera);
  const hit = raycaster.intersectObjects(selectable, false)[0];
  if (!hit) { tooltip.hidden = true; return; }
  const data = hit.object.userData;
  if (click) focusOn(hit.object.getWorldPosition(new THREE.Vector3()), data);
  tooltip.hidden = false; tooltip.textContent = data.label;
  tooltip.style.left = `${event.clientX + 14}px`; tooltip.style.top = `${event.clientY + 14}px`;
}
canvas.addEventListener('pointermove', event => pick(event));
canvas.addEventListener('pointerleave', () => { tooltip.hidden = true; });
canvas.addEventListener('click', event => pick(event, true));
addEventListener('keydown', event => { if (event.key.toLowerCase() === 'r') { focus.active = false; controls.target.set(0, 0, 0); camera.position.set(0, 240, 930); setPanel({ label: 'The whole corpus', description: 'Orbit the map. Colored districts are the major corpus planes; each node is a document or a process/agent asset.', detail: 'Drag to orbit · scroll to zoom · click to focus · R to reset' }); } });
addEventListener('resize', () => { camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });

function render(time) {
  if (focus.active) {
    controls.target.lerp(focus.target, .06); camera.position.lerp(focus.position, .045);
    if (camera.position.distanceTo(focus.position) < 1) focus.active = false;
  }
  rootSphere.scale.setScalar(1 + Math.sin(time * .002) * .08);
  controls.update(); renderer.render(scene, camera);
}

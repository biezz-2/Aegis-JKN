<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import * as THREE from "three";

  let containerEl = $state<HTMLDivElement | null>(null);
  let canvasEl = $state<HTMLCanvasElement | null>(null);

  // Interactive UI state
  let activeMode = $state<"shield" | "graph" | "pulse">("shield");
  let isHovered = $state(false);
  let isDragging = $state(false);
  let verificationStatus = $state("PERISAI AKTIF · KLAIM AMAN");
  let pulseCount = $state(0);

  // Three.js internal references
  let renderer: THREE.WebGLRenderer | null = null;
  let scene: THREE.Scene | null = null;
  let camera: THREE.PerspectiveCamera | null = null;
  let animFrameId: number | null = null;
  let resizeObserver: ResizeObserver | null = null;

  // Groups and objects for animation
  let mainGroup: THREE.Group | null = null;
  let shieldGroup: THREE.Group | null = null;
  let ringsGroup: THREE.Group | null = null;
  let networkGroup: THREE.Group | null = null;
  let pulseWaveMesh: THREE.Mesh | null = null;
  let crossEmblem: THREE.Mesh | null = null;

  // Mouse & physics tracking
  let targetRotationX = 0;
  let targetRotationY = 0;
  let currentRotationX = 0;
  let currentRotationY = 0;
  let prevPointerX = 0;
  let prevPointerY = 0;
  let pulseIntensity = 0;

  function triggerVerificationPulse() {
    pulseIntensity = 1.0;
    pulseCount += 1;
    verificationStatus = `VERIFIKASI MHGSL AI #${pulseCount} BERJALAN`;
    setTimeout(() => {
      verificationStatus = "PERISAI AKTIF · KLAIM AMAN";
    }, 1800);
  }

  function setMode(mode: "shield" | "graph" | "pulse") {
    activeMode = mode;
    if (mode === "pulse") {
      triggerVerificationPulse();
    }
  }

  onMount(() => {
    if (!containerEl || !canvasEl) return;

    const width = containerEl.clientWidth || 500;
    const height = containerEl.clientHeight || 500;

    // 1. Scene setup
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x17241d, 0.035);

    // 2. Camera setup
    camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 7.5);

    // 3. WebGL Renderer
    renderer = new THREE.WebGLRenderer({
      canvas: canvasEl,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance"
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;

    // 4. Lighting using 5-color palette
    // Dust Grey: #dad7cd, Dry Sage: #a3b18a, Fern: #588157, Hunter Green: #3a5a40, Pine Teal: #344e41
    const ambientLight = new THREE.AmbientLight(0x17241d, 2.4);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0x588157, 4.0);
    keyLight.position.set(5, 6, 6);
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0xa3b18a, 2.6);
    rimLight.position.set(-6, -4, -3);
    scene.add(rimLight);

    const pointLight = new THREE.PointLight(0xdad7cd, 3.2, 10);
    pointLight.position.set(0, 0, 2);
    scene.add(pointLight);

    // Master group
    mainGroup = new THREE.Group();
    scene.add(mainGroup);

    // 5. Shield Construction (Aegis Hex-Kite Shape)
    shieldGroup = new THREE.Group();
    mainGroup.add(shieldGroup);

    const shieldShape = new THREE.Shape();
    shieldShape.moveTo(0, 2.1);
    shieldShape.lineTo(1.4, 1.5);
    shieldShape.lineTo(1.6, 0.2);
    shieldShape.lineTo(0.9, -1.3);
    shieldShape.lineTo(0, -2.4);
    shieldShape.lineTo(-0.9, -1.3);
    shieldShape.lineTo(-1.6, 0.2);
    shieldShape.lineTo(-1.4, 1.5);
    shieldShape.closePath();

    const extrudeSettings: THREE.ExtrudeGeometryOptions = {
      depth: 0.22,
      bevelEnabled: true,
      bevelSegments: 4,
      steps: 1,
      bevelSize: 0.08,
      bevelThickness: 0.08
    };

    const shieldGeo = new THREE.ExtrudeGeometry(shieldShape, extrudeSettings);
    shieldGeo.center();

    // Shield Body Material: Pine Teal #344e41
    const shieldMat = new THREE.MeshPhysicalMaterial({
      color: 0x344e41,
      metalness: 0.85,
      roughness: 0.26,
      clearcoat: 0.9,
      clearcoatRoughness: 0.12,
      reflectivity: 0.92,
      transmission: 0.08,
      transparent: true,
      opacity: 0.98
    });

    const shieldMesh = new THREE.Mesh(shieldGeo, shieldMat);
    shieldGroup.add(shieldMesh);

    // Beveled Wireframe Overlay: Dry Sage #a3b18a
    const wireMat = new THREE.MeshBasicMaterial({
      color: 0xa3b18a,
      wireframe: true,
      transparent: true,
      opacity: 0.4
    });
    const wireMesh = new THREE.Mesh(shieldGeo, wireMat);
    wireMesh.scale.set(1.002, 1.002, 1.002);
    shieldGroup.add(wireMesh);

    // Central Medical Cross / Caduceus Emblem: Dust Grey #dad7cd with Fern #588157 glow
    const crossGroup = new THREE.Group();
    const crossHorizGeo = new THREE.BoxGeometry(0.85, 0.28, 0.18);
    const crossVertGeo = new THREE.BoxGeometry(0.28, 0.85, 0.18);
    const crossMat = new THREE.MeshStandardMaterial({
      color: 0xdad7cd,
      emissive: 0x588157,
      emissiveIntensity: 2.2,
      metalness: 0.25,
      roughness: 0.15
    });

    const horizMesh = new THREE.Mesh(crossHorizGeo, crossMat);
    const vertMesh = new THREE.Mesh(crossVertGeo, crossMat);
    crossGroup.add(horizMesh, vertMesh);
    crossGroup.position.z = 0.22;
    shieldGroup.add(crossGroup);
    crossEmblem = horizMesh;

    // Glowing Inner Ring: Hunter Green #3a5a40
    const innerRingGeo = new THREE.RingGeometry(0.95, 1.08, 48);
    const innerRingMat = new THREE.MeshBasicMaterial({
      color: 0x3a5a40,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.8
    });
    const innerRingMesh = new THREE.Mesh(innerRingGeo, innerRingMat);
    innerRingMesh.position.z = 0.18;
    shieldGroup.add(innerRingMesh);

    // 6. Concentric Holographic Orbital Rings
    ringsGroup = new THREE.Group();
    mainGroup.add(ringsGroup);

    const ring1Geo = new THREE.TorusGeometry(2.6, 0.02, 16, 100);
    const ring1Mat = new THREE.MeshStandardMaterial({
      color: 0xdad7cd,
      emissive: 0xa3b18a,
      emissiveIntensity: 1.6,
      metalness: 0.8,
      roughness: 0.2
    });
    const ring1 = new THREE.Mesh(ring1Geo, ring1Mat);
    ring1.rotation.x = Math.PI / 3;
    ringsGroup.add(ring1);

    const ring2Geo = new THREE.TorusGeometry(3.1, 0.018, 16, 120);
    const ring2Mat = new THREE.MeshStandardMaterial({
      color: 0x588157,
      emissive: 0x3a5a40,
      emissiveIntensity: 1.5,
      metalness: 0.8,
      roughness: 0.2
    });
    const ring2 = new THREE.Mesh(ring2Geo, ring2Mat);
    ring2.rotation.y = Math.PI / 4;
    ring2.rotation.x = -Math.PI / 6;
    ringsGroup.add(ring2);

    const ring3Geo = new THREE.TorusGeometry(3.5, 0.015, 16, 140);
    const ring3Mat = new THREE.MeshStandardMaterial({
      color: 0xa3b18a,
      emissive: 0x588157,
      emissiveIntensity: 1.2,
      metalness: 0.7,
      roughness: 0.3
    });
    const ring3 = new THREE.Mesh(ring3Geo, ring3Mat);
    ring3.rotation.z = Math.PI / 5;
    ringsGroup.add(ring3);

    // 7. Graphiti & MHGSL GNN Node Constellation
    networkGroup = new THREE.Group();
    mainGroup.add(networkGroup);

    const nodeCount = 55;
    const nodeCoords: THREE.Vector3[] = [];
    const sphereGeo = new THREE.SphereGeometry(0.045, 12, 12);
    const sphereMat = new THREE.MeshStandardMaterial({
      color: 0xdad7cd,
      emissive: 0xa3b18a,
      emissiveIntensity: 2.2
    });

    for (let i = 0; i < nodeCount; i++) {
      const u = Math.random();
      const v = Math.random();
      const theta = u * 2.0 * Math.PI;
      const phi = Math.acos(2.0 * v - 1.0);
      const r = 2.4 + Math.random() * 1.5;

      const x = r * Math.sin(phi) * Math.cos(theta);
      const y = r * Math.sin(phi) * Math.sin(theta);
      const z = r * Math.cos(phi);

      const nodeMesh = new THREE.Mesh(sphereGeo, sphereMat);
      nodeMesh.position.set(x, y, z);
      networkGroup.add(nodeMesh);
      nodeCoords.push(new THREE.Vector3(x, y, z));
    }

    // Connect nearest nodes with dynamic lines: Fern #588157
    const lineIndices: number[] = [];
    for (let i = 0; i < nodeCount; i++) {
      for (let j = i + 1; j < nodeCount; j++) {
        const dist = nodeCoords[i].distanceTo(nodeCoords[j]);
        if (dist < 1.35) {
          lineIndices.push(i, j);
        }
      }
    }

    const linePositions = new Float32Array(lineIndices.length * 3);
    for (let i = 0; i < lineIndices.length; i++) {
      const pt = nodeCoords[lineIndices[i]];
      linePositions[i * 3] = pt.x;
      linePositions[i * 3 + 1] = pt.y;
      linePositions[i * 3 + 2] = pt.z;
    }

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute("position", new THREE.BufferAttribute(linePositions, 3));
    const lineMat = new THREE.LineBasicMaterial({
      color: 0x588157,
      transparent: true,
      opacity: 0.35
    });
    const networkLines = new THREE.LineSegments(lineGeo, lineMat);
    networkGroup.add(networkLines);

    // 8. Shockwave Pulse Mesh: Dry Sage #a3b18a
    const pulseGeo = new THREE.RingGeometry(0.2, 0.45, 64);
    const pulseMat = new THREE.MeshBasicMaterial({
      color: 0xa3b18a,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.0
    });
    pulseWaveMesh = new THREE.Mesh(pulseGeo, pulseMat);
    pulseWaveMesh.position.z = 0.35;
    mainGroup.add(pulseWaveMesh);

    // 9. Interaction listeners
    function onPointerMove(e: MouseEvent | TouchEvent) {
      const clientX = "touches" in e ? e.touches[0].clientX : e.clientX;
      const clientY = "touches" in e ? e.touches[0].clientY : e.clientY;

      if (!containerEl) return;
      const rect = containerEl.getBoundingClientRect();
      const normX = ((clientX - rect.left) / rect.width) * 2 - 1;
      const normY = -(((clientY - rect.top) / rect.height) * 2 - 1);

      if (isDragging) {
        const deltaX = clientX - prevPointerX;
        const deltaY = clientY - prevPointerY;
        targetRotationY += deltaX * 0.012;
        targetRotationX += deltaY * 0.012;
      } else {
        targetRotationY = normX * 0.45;
        targetRotationX = -normY * 0.35;
      }

      prevPointerX = clientX;
      prevPointerY = clientY;
    }

    function onPointerDown(e: MouseEvent | TouchEvent) {
      isDragging = true;
      const clientX = "touches" in e ? e.touches[0].clientX : e.clientX;
      const clientY = "touches" in e ? e.touches[0].clientY : e.clientY;
      prevPointerX = clientX;
      prevPointerY = clientY;
    }

    function onPointerUp() {
      isDragging = false;
    }

    const hostEl = containerEl;
    hostEl.addEventListener("mousemove", onPointerMove);
    hostEl.addEventListener("mousedown", onPointerDown);
    window.addEventListener("mouseup", onPointerUp);
    hostEl.addEventListener("touchmove", onPointerMove, { passive: true });
    hostEl.addEventListener("touchstart", onPointerDown, { passive: true });
    window.addEventListener("touchend", onPointerUp);

    // 10. Resize Observer
    resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const w = entry.contentRect.width;
        const h = entry.contentRect.height;
        if (w > 0 && h > 0 && camera && renderer) {
          camera.aspect = w / h;
          camera.updateProjectionMatrix();
          renderer.setSize(w, h);
        }
      }
    });
    resizeObserver.observe(containerEl);

    // 11. Render Loop
    let clock = new THREE.Clock();

    function animate() {
      animFrameId = requestAnimationFrame(animate);
      const delta = clock.getDelta();
      const elapsed = clock.getElapsedTime();

      // Smooth inertia rotation
      currentRotationX += (targetRotationX - currentRotationX) * 0.08;
      currentRotationY += (targetRotationY - currentRotationY) * 0.08;

      if (mainGroup) {
        mainGroup.rotation.x = currentRotationX;
        mainGroup.rotation.y = currentRotationY;
      }

      // Continuous gentle hover float
      if (shieldGroup) {
        shieldGroup.position.y = Math.sin(elapsed * 1.6) * 0.12;
        const scaleTarget = isHovered ? 1.05 : 1.0;
        shieldGroup.scale.lerp(new THREE.Vector3(scaleTarget, scaleTarget, scaleTarget), 0.08);
      }

      // Rotate rings at harmonic orbital speeds
      if (ringsGroup) {
        ringsGroup.children[0].rotation.z += delta * 0.35;
        ringsGroup.children[1].rotation.x += delta * 0.25;
        ringsGroup.children[2].rotation.y += delta * 0.18;
      }

      // Rotate network constellation
      if (networkGroup) {
        networkGroup.rotation.y += delta * 0.12;
        networkGroup.rotation.x += delta * 0.05;
      }

      // Emissive pulse on medical cross
      if (crossEmblem && crossEmblem.material instanceof THREE.MeshStandardMaterial) {
        const baseIntensity = 1.8 + Math.sin(elapsed * 3.0) * 0.6;
        crossEmblem.material.emissiveIntensity = baseIntensity + pulseIntensity * 4.0;
      }

      // Expand shockwave wave when pulseIntensity > 0
      if (pulseWaveMesh && pulseWaveMesh.material instanceof THREE.MeshBasicMaterial) {
        if (pulseIntensity > 0.01) {
          pulseIntensity = Math.max(0, pulseIntensity - delta * 0.85);
          const currentScale = (1.0 - pulseIntensity) * 6.0 + 0.5;
          pulseWaveMesh.scale.set(currentScale, currentScale, 1);
          pulseWaveMesh.material.opacity = pulseIntensity * 0.8;
          pulseWaveMesh.visible = true;
        } else {
          pulseWaveMesh.visible = false;
        }
      }

      // Mode-specific visual emphasis
      if (activeMode === "graph" && networkGroup) {
        networkGroup.scale.lerp(new THREE.Vector3(1.18, 1.18, 1.18), 0.05);
      } else if (networkGroup) {
        networkGroup.scale.lerp(new THREE.Vector3(1.0, 1.0, 1.0), 0.05);
      }

      if (renderer && scene && camera) {
        renderer.render(scene, camera);
      }
    }

    animate();

    return () => {
      if (animFrameId) cancelAnimationFrame(animFrameId);
      hostEl.removeEventListener("mousemove", onPointerMove);
      hostEl.removeEventListener("mousedown", onPointerDown);
      window.removeEventListener("mouseup", onPointerUp);
      hostEl.removeEventListener("touchmove", onPointerMove);
      hostEl.removeEventListener("touchstart", onPointerDown);
      window.removeEventListener("touchend", onPointerUp);
      if (resizeObserver) resizeObserver.disconnect();
      if (renderer) {
        renderer.dispose();
      }
    };
  });

  onDestroy(() => {
    if (animFrameId) cancelAnimationFrame(animFrameId);
    if (renderer) renderer.dispose();
  });
</script>

<div
  bind:this={containerEl}
  data-testid="landing-3d-canvas"
  class="relative w-full h-[420px] sm:h-[480px] lg:h-[540px] flex items-center justify-center select-none overflow-hidden rounded-3xl border border-[#a3b18a]/30 bg-gradient-to-b from-[#203127]/50 via-card/60 to-background/90 shadow-2xl backdrop-blur-xl group cursor-grab active:cursor-grabbing"
  role="region"
  aria-label="3D Interactive Aegis-JKN Model"
  onmouseenter={() => (isHovered = true)}
  onmouseleave={() => (isHovered = false)}
>
  <!-- Background Glow & Grid Accents using Pine Teal / Dry Sage -->
  <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(88,129,87,0.18),transparent_70%)]"></div>
  <div class="pointer-events-none absolute -inset-px rounded-3xl border border-[#a3b18a]/20 opacity-50 group-hover:opacity-100 transition-opacity duration-300"></div>

  <!-- Three.js Canvas -->
  <canvas bind:this={canvasEl} class="w-full h-full block z-10"></canvas>

  <!-- Top Floating Status Pill -->
  <div class="absolute top-4 left-4 right-4 z-20 flex items-center justify-between gap-2 pointer-events-none">
    <div class="inline-flex items-center gap-2 rounded-full border border-[#a3b18a]/40 bg-background/85 px-3 py-1 text-[11px] font-mono font-semibold text-[#3a5a40] dark:text-[#a3b18a] shadow-sm backdrop-blur-md">
      <span class="relative flex h-2 w-2">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#a3b18a] opacity-75"></span>
        <span class="relative inline-flex rounded-full h-2 w-2 bg-[#588157]"></span>
      </span>
      <span>{verificationStatus}</span>
    </div>

    <div class="hidden sm:inline-flex items-center gap-1.5 rounded-full border border-border/80 bg-background/70 px-2.5 py-1 text-[10px] font-mono text-muted-foreground backdrop-blur-md">
      <span>60 FPS</span>
      <span class="text-border">•</span>
      <span>Three.js PBR</span>
    </div>
  </div>

  <!-- Bottom Floating Interactive Mode Switcher -->
  <div class="absolute bottom-4 inset-x-4 z-20 flex flex-col sm:flex-row items-center justify-between gap-3 bg-background/85 border border-[#dad7cd]/40 dark:border-[#a3b18a]/20 p-2 sm:px-3 sm:py-2 rounded-2xl backdrop-blur-md shadow-lg">
    <div class="flex items-center gap-1 text-[11px] text-muted-foreground font-medium hidden md:flex">
      <svg class="w-3.5 h-3.5 text-[#588157] animate-spin-slow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" stroke-opacity="0.25"/>
        <path d="M12 2a10 10 0 0 1 10 10" />
      </svg>
      <span>Geser kursor untuk memutar atau klik tombol mode:</span>
    </div>

    <!-- Mode Selector Buttons -->
    <div class="flex items-center gap-1.5 w-full sm:w-auto justify-center">
      <button
        type="button"
        data-testid="landing-mode-shield"
        onclick={() => setMode("shield")}
        class="inline-flex items-center gap-1.5 rounded-xl px-2.5 py-1.5 text-xs font-semibold transition-all duration-150 {activeMode === 'shield'
          ? 'bg-[#3a5a40] text-white shadow-xs shadow-[#3a5a40]/30'
          : 'bg-muted/60 text-muted-foreground hover:text-foreground hover:bg-muted'}"
      >
        <span>🛡️</span>
        <span>Perisai</span>
      </button>

      <button
        type="button"
        data-testid="landing-mode-graph"
        onclick={() => setMode("graph")}
        class="inline-flex items-center gap-1.5 rounded-xl px-2.5 py-1.5 text-xs font-semibold transition-all duration-150 {activeMode === 'graph'
          ? 'bg-[#3a5a40] text-white shadow-xs shadow-[#3a5a40]/30'
          : 'bg-muted/60 text-muted-foreground hover:text-foreground hover:bg-muted'}"
      >
        <span>🕸️</span>
        <span>GNN Graf</span>
      </button>

      <button
        type="button"
        data-testid="landing-mode-pulse"
        onclick={() => triggerVerificationPulse()}
        class="inline-flex items-center gap-1.5 rounded-xl px-3 py-1.5 text-xs font-bold transition-all duration-150 bg-gradient-to-r from-[#3a5a40] via-[#588157] to-[#a3b18a] text-white shadow-xs shadow-[#588157]/25 hover:brightness-110 active:scale-95"
      >
        <span class="animate-bounce">⚡</span>
        <span>Audit Live</span>
      </button>
    </div>
  </div>
</div>

<style>
  @keyframes spin-slow {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  .animate-spin-slow {
    animation: spin-slow 8s linear infinite;
  }
</style>

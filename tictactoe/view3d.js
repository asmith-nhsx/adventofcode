// 3D view of the 3x3x3 board using three.js (global THREE + OrbitControls).
// Drag to rotate, scroll to zoom, click an empty cell to play.
//
// createView3D(container, onPick) returns an object the game uses to keep
// the view in sync: reset, setMark, setTurn, showLines, setGameOver,
// setInteractive.

function createView3D(container, onPick) {
  const SPACING = 1.6;
  const COLORS = { X: 0xdd3333, O: 0x2266cc };
  const EMPTY_COLOR = 0x8899aa;

  // Cell index = layer * 9 + row * 3 + col. Layer 0 (top) is highest.
  function cellPosition(i) {
    const col = i % 3, row = Math.floor(i / 3) % 3, layer = Math.floor(i / 9);
    return new THREE.Vector3((col - 1) * SPACING, (1 - layer) * SPACING, (row - 1) * SPACING);
  }

  // --- Scene setup --------------------------------------------------------
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
  camera.position.set(6, 5, 8);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minDistance = 6;
  controls.maxDistance = 18;

  scene.add(new THREE.AmbientLight(0xffffff, 0.65));
  const sun = new THREE.DirectionalLight(0xffffff, 0.8);
  sun.position.set(5, 10, 7);
  scene.add(sun);

  // --- Dividing planes ------------------------------------------------------
  // The 3D version of the # grid: two planes across each axis, sitting
  // halfway between cells, so they split the cube into 27 spaces.
  const EXTENT = 3 * SPACING;
  const planeGeo = new THREE.PlaneGeometry(EXTENT, EXTENT);
  const planeEdgesGeo = new THREE.EdgesGeometry(planeGeo);
  const planeMat = new THREE.MeshBasicMaterial({
    color: 0x8a94a6, transparent: true, opacity: 0.14, side: THREE.DoubleSide, depthWrite: false,
  });
  const planeEdgeMat = new THREE.LineBasicMaterial({ color: 0x6b7385, transparent: true, opacity: 0.45 });
  const PLANE_OPACITY = 0.14, PLANE_EDGE_OPACITY = 0.45;
  for (const offset of [-SPACING / 2, SPACING / 2]) {
    // PlaneGeometry lies in the XY plane (facing z); rotate for the other two axes.
    const orientations = [
      { pos: [offset, 0, 0], rot: [0, Math.PI / 2, 0] },  // splits columns (x)
      { pos: [0, offset, 0], rot: [Math.PI / 2, 0, 0] },  // splits layers (y)
      { pos: [0, 0, offset], rot: [0, 0, 0] },            // splits rows (z)
    ];
    for (const { pos, rot } of orientations) {
      const plane = new THREE.Mesh(planeGeo, planeMat);
      plane.add(new THREE.LineSegments(planeEdgesGeo, planeEdgeMat));
      plane.position.set(...pos);
      plane.rotation.set(...rot);
      scene.add(plane);
    }
  }

  // --- Cells ---------------------------------------------------------------
  // Each space has an invisible box used only for clicking. It is shown,
  // tinted in the current player's colour, while the mouse hovers over it.
  const boxGeo = new THREE.BoxGeometry(0.9, 0.9, 0.9);
  const cells = [];
  for (let i = 0; i < 27; i++) {
    const mat = new THREE.MeshBasicMaterial({
      color: EMPTY_COLOR, transparent: true, opacity: 0.35, depthWrite: false, visible: false,
    });
    const box = new THREE.Mesh(boxGeo, mat);  // still hit by raycasts when not visible
    box.position.copy(cellPosition(i));
    box.userData.index = i;
    scene.add(box);
    cells.push({ box, mat, marker: null, state: null });
  }

  const markersGroup = new THREE.Group();
  const linesGroup = new THREE.Group();
  scene.add(markersGroup, linesGroup);

  // X is a red tetrahedron, O is a blue sphere. Both are true 3D shapes, so
  // they read correctly from any angle without turning to face the camera.
  function makeMarker(player) {
    const group = new THREE.Group();
    let mat;
    if (player === 'X') {
      // Flat shading gives each face its own shade, so the edges stay crisp.
      mat = new THREE.MeshStandardMaterial({
        color: COLORS.X, roughness: 0.45, metalness: 0.1, flatShading: true, transparent: true,
      });
      const tetra = new THREE.Mesh(new THREE.TetrahedronGeometry(0.5), mat);
      // Tilt so the (1,1,1) vertex points straight up and the opposite face
      // sits flat on the bottom: turn 45° about z, then -35.26° about x.
      tetra.rotation.set(-Math.atan(Math.SQRT1_2), 0, Math.PI / 4);
      group.add(tetra);
    } else {
      mat = new THREE.MeshStandardMaterial({
        color: COLORS.O, roughness: 0.3, metalness: 0.1, transparent: true,
      });
      group.add(new THREE.Mesh(new THREE.SphereGeometry(0.36, 32, 16), mat));
    }
    return { group, mat };
  }

  function disposeGroup(group) {
    group.traverse(o => {
      if (o.geometry) o.geometry.dispose();
      if (o.material) o.material.dispose();
    });
    group.clear();
  }

  // --- State ---------------------------------------------------------------
  let turn = 'X';
  let interactive = true;
  let gameOver = false;
  let hovered = null;

  function setHover(i) {
    if (hovered === i) return;
    if (hovered !== null && !cells[hovered].state) {
      cells[hovered].mat.visible = false;
    }
    hovered = i;
    if (i !== null) {
      cells[i].mat.color.setHex(COLORS[turn]);
      cells[i].mat.opacity = 0.35;
      cells[i].mat.visible = true;
    }
    renderer.domElement.style.cursor = i !== null ? 'pointer' : '';
  }

  // --- Picking: click (not drag) on the nearest empty cell under the mouse --
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();

  function pickCell(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointer, camera);
    // Only empty cells are targets, so you can click "through" filled ones.
    const targets = cells.filter(c => !c.state).map(c => c.box);
    const hit = raycaster.intersectObjects(targets, false)[0];
    return hit ? hit.object.userData.index : null;
  }

  let downX = 0, downY = 0, dragging = false;
  const el = renderer.domElement;
  el.addEventListener('pointerdown', e => {
    downX = e.clientX; downY = e.clientY; dragging = true;
  });
  el.addEventListener('pointermove', e => {
    if (dragging && Math.hypot(e.clientX - downX, e.clientY - downY) > 5) {
      setHover(null);
      return;
    }
    setHover(interactive && !gameOver && e.pointerType === 'mouse' ? pickCell(e) : null);
  });
  el.addEventListener('pointerleave', () => setHover(null));
  el.addEventListener('pointerup', e => {
    dragging = false;
    const moved = Math.hypot(e.clientX - downX, e.clientY - downY);
    if (moved > 5 || !interactive || gameOver) return;
    const i = pickCell(e);
    if (i !== null) {
      setHover(null);
      onPick(i);
    }
  });

  // --- Sizing and render loop ---------------------------------------------
  function resize() {
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(container);
  resize();

  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }
  animate();

  // --- API used by the game -------------------------------------------------
  return {
    reset(bannedIndex) {
      disposeGroup(markersGroup);
      disposeGroup(linesGroup);
      gameOver = false;
      hovered = null;
      cells.forEach(c => {
        c.state = null;
        c.marker = null;
        c.box.visible = true;
        c.mat.visible = false;
      });
      planeMat.opacity = PLANE_OPACITY;
      planeEdgeMat.opacity = PLANE_EDGE_OPACITY;
      // Banned centre: a grey block filling the whole space between the
      // planes (scaled up from the 0.9 hit box to the full cell size).
      const banned = cells[bannedIndex];
      banned.state = '#';
      banned.box.scale.setScalar(SPACING / 0.9);
      banned.mat.color.setHex(0x999999);
      banned.mat.opacity = 0.45;
      banned.mat.visible = true;
    },

    setTurn(player) {
      turn = player;
    },

    setInteractive(on) {
      interactive = on;
      if (!on) setHover(null);
    },

    setMark(i, player) {
      const c = cells[i];
      c.state = player;
      c.box.visible = false;
      c.marker = makeMarker(player);
      c.marker.group.position.copy(cellPosition(i));
      markersGroup.add(c.marker.group);
    },

    // done = { X: [lines], O: [lines] }: draw a rod through each completed
    // line and make its markers glow in the player's colour.
    showLines(done) {
      disposeGroup(linesGroup);
      for (const player of ['X', 'O']) {
        for (const line of done[player]) {
          const start = cellPosition(line[0]);
          const end = cellPosition(line[2]);
          const rod = new THREE.Mesh(
            new THREE.CylinderGeometry(0.07, 0.07, start.distanceTo(end) + 0.9, 12),
            new THREE.MeshStandardMaterial({ color: COLORS[player], emissive: COLORS[player], emissiveIntensity: 0.4 })
          );
          rod.position.copy(start).add(end).multiplyScalar(0.5);
          rod.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), end.clone().sub(start).normalize());
          linesGroup.add(rod);
          for (const i of line) {
            const m = cells[i].marker;
            m.mat.emissive.setHex(COLORS[player]);
            m.mat.emissiveIntensity = 0.5;
            m.group.scale.setScalar(1.15);
          }
        }
      }
    },

    // Fade everything except completed lines so the result stands out.
    setGameOver(done) {
      gameOver = true;
      setHover(null);
      const inLine = new Set([...done.X, ...done.O].flat());
      cells.forEach((c, i) => {
        if (c.marker && !inLine.has(i)) c.marker.mat.opacity = 0.2;
      });
      planeMat.opacity = PLANE_OPACITY / 2;
      planeEdgeMat.opacity = PLANE_EDGE_OPACITY / 3;
    },
  };
}

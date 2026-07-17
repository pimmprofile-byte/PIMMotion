// PIMMotion 프런트 — 서버 API만 호출 (Claude 직접호출 없음, 키는 서버 보관)
const $ = (s) => document.querySelector(s);
const api = async (path, opts = {}) => {
  const r = await fetch(path, opts);
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).detail || r.statusText);
  return r.json();
};

const STATES = ["미착수", "진행", "검수대기", "완료", "보류"];

async function boot() {
  try {
    const h = await api("/api/health");
    $("#status").textContent = `model ${h.model} · claude ${h.claude ? "on" : "off"} · storage ${h.storage}`;
  } catch { $("#status").textContent = "서버 연결 실패"; }

  const cats = await api("/api/categories");
  $("#category").innerHTML = cats
    .map((c) => `<option value="${c.key}">${c.label} · ${c.steps}단계 (${c.kind})</option>`)
    .join("");

  $("#create").onclick = createBoard;
  await refreshList();
}

async function refreshList() {
  const boards = await api("/api/boards");
  $("#board-list").innerHTML = boards
    .map((b) => `<li data-id="${b.id}">${b.title}<br><span class="cat">${b.category}</span></li>`)
    .join("") || '<li class="cat">아직 없음</li>';
  $("#board-list").querySelectorAll("li[data-id]").forEach((li) => {
    li.onclick = () => openBoard(li.dataset.id);
  });
}

async function createBoard() {
  const category = $("#category").value;
  const title = $("#title").value.trim();
  if (!title) return alert("프로젝트명을 입력하세요");
  const board = await api("/api/boards", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category, title }),
  });
  $("#title").value = "";
  await refreshList();
  renderBoard(board);
}

async function openBoard(id) {
  renderBoard(await api(`/api/boards/${id}`));
}

function renderBoard(b) {
  const el = $("#board");
  let phase = "";
  const steps = b.steps.map((s) => {
    const ph = s.phase && s.phase !== phase ? ((phase = s.phase), `<div class="phase">${s.phase}</div>`) : "";
    const gateOpen = gateIsOpen(s.gate);
    const check = Object.entries(s.gate.checklist || {});
    return `${ph}
    <div class="step" data-key="${s.key}">
      <div class="step-top" onclick="this.parentElement.classList.toggle('open')">
        <span class="step-title">${s.title}</span>
        <span class="badge s-${s.status}">${s.status}</span>
      </div>
      ${s.guide ? `<p class="guide">${s.guide}</p>` : ""}
      <div class="step-body">
        <div class="gate-row"><b>3-Gate</b> <span class="hint">체크리스트 + 산출물 + PD승인</span></div>
        ${check.length ? check.map(([k, v]) => `
          <label class="gate-row"><input type="checkbox" data-chk="${k}" ${v ? "checked" : ""}/> ${k}</label>`).join("")
          : `<div class="gate-row hint">체크리스트 항목 없음 (브리프에서 정의)</div>`}
        <label class="gate-row"><input type="checkbox" data-pd ${s.gate.pd_approved ? "checked" : ""}/> PD 승인</label>
        <div class="assets">
          ${(s.gate.asset_ids || []).map((aid) => {
            const a = b.assets.find((x) => x.id === aid);
            return a ? `<div class="a">📄 ${a.filename} ${a.reviewed ? '<span class="ok">✓검수</span>' : `<button class="ghost" data-review="${a.id}" style="width:auto;padding:2px 8px;margin:0">검수</button>`}</div>` : "";
          }).join("")}
        </div>
        <div class="gate-row"><input type="file" data-upload style="width:auto;margin:0"/></div>
        <div class="status-btns">
          ${STATES.map((st) => `<button class="ghost" data-status="${st}" ${st === "완료" && !gateOpen ? "disabled title='3-Gate 미충족'" : ""}>${st}</button>`).join("")}
        </div>
      </div>
    </div>`;
  }).join("");

  const forge = b.category === "murdermystery"
    ? `<button id="forge" style="width:auto;margin-top:10px">⚙ Forge — 초안 생성</button>` : "";

  el.innerHTML = `
    <div class="board-head">
      <h2>${b.title}</h2><span class="cat">${b.category} · ${b.id}</span>
    </div>${steps}${forge}`;

  // 핸들러 배선
  el.querySelectorAll(".step").forEach((stepEl) => {
    const key = stepEl.dataset.key;
    stepEl.querySelectorAll("[data-status]").forEach((btn) => {
      btn.onclick = (e) => { e.stopPropagation(); patchStep(b.id, key, { status: btn.dataset.status }); };
    });
    const chks = {};
    stepEl.querySelectorAll("[data-chk]").forEach((c) => { chks[c.dataset.chk] = c; });
    const pd = stepEl.querySelector("[data-pd]");
    const saveGate = () => {
      const checklist = Object.fromEntries(Object.entries(chks).map(([k, c]) => [k, c.checked]));
      patchStep(b.id, key, { checklist: Object.keys(checklist).length ? checklist : undefined, pd_approved: pd.checked });
    };
    Object.values(chks).forEach((c) => (c.onchange = saveGate));
    if (pd) pd.onchange = saveGate;
    const up = stepEl.querySelector("[data-upload]");
    if (up) up.onchange = () => uploadAsset(b.id, key, up.files[0]);
    stepEl.querySelectorAll("[data-review]").forEach((btn) => {
      btn.onclick = (e) => { e.stopPropagation(); reviewAsset(b.id, btn.dataset.review); };
    });
  });
  const fbtn = el.querySelector("#forge");
  if (fbtn) fbtn.onclick = () => runForge(b.id);
}

function gateIsOpen(g) {
  const c = Object.values(g.checklist || {});
  const checklistOk = c.length > 0 && c.every(Boolean);
  return checklistOk && (g.asset_ids || []).length > 0 && g.pd_approved;
}

async function patchStep(id, key, body) {
  try {
    renderBoard(await api(`/api/boards/${id}/steps/${key}`, {
      method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    }));
  } catch (e) { alert(e.message); await openBoard(id); }
}

async function uploadAsset(id, key, file) {
  if (!file) return;
  const fd = new FormData();
  fd.append("file", file);
  renderBoard(await api(`/api/boards/${id}/steps/${key}/assets`, { method: "POST", body: fd }));
}

async function reviewAsset(id, assetId) {
  const criteria = prompt("검수 루브릭 (비우면 일반 품질검수):", "") || "";
  try {
    const r = await api(`/api/boards/${id}/assets/${assetId}/review?criteria=${encodeURIComponent(criteria)}`, { method: "POST" });
    alert(`${r.pass ? "통과 ✓" : "반려 ✗"} (${r.score})\n\n${r.note}\n\n${(r.issues || []).join("\n")}`);
    await openBoard(id);
  } catch (e) { alert(e.message); }
}

async function runForge(id) {
  const instruction = prompt("Forge 지시 (비우면 초안 생성):", "") || "";
  try {
    const r = await api("/api/forge", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board_id: id, instruction }),
    });
    alert(`[초안]\n${r.draft}\n\n${r.notes || ""}`);
  } catch (e) { alert(e.message); }
}

boot();

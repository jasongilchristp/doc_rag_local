const fileInput   = document.getElementById("file");
const fileName    = document.getElementById("fileName");
const uploadBtn   = document.getElementById("uploadBtn");
const uploadNote  = document.getElementById("uploadNote");
const messages    = document.getElementById("messages");
const empty       = document.getElementById("empty");
const question    = document.getElementById("question");
const sendBtn     = document.getElementById("sendBtn");
const modelSelect = document.getElementById("modelSelect");

let hasDoc = typeof HAS_DOCUMENT !== "undefined" ? HAS_DOCUMENT : false;
if (hasDoc) enableChat();

async function loadModels() {
  try {
    const res = await fetch("/api/models");
    const data = await res.json();
    const models = data.models || [];
    if (models.length === 0) {
      modelSelect.innerHTML = "<option>no models found</option>";
      modelSelect.disabled = true;
      return;
    }
    modelSelect.innerHTML = "";
    for (const name of models) {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name;
      modelSelect.appendChild(opt);
    }
    const base = (n) => n.split(":")[0];
    const match = models.find((n) => n === data.default || base(n) === base(data.default || ""));
    if (match) modelSelect.value = match;
  } catch (err) {
    modelSelect.innerHTML = "<option>no models found</option>";
    modelSelect.disabled = true;
  }
}
loadModels();

fileInput.addEventListener("change", () => {
  const f = fileInput.files[0];
  fileName.textContent = f ? f.name : "No file chosen";
  uploadBtn.disabled = !f;
  uploadNote.textContent = "";
});

uploadBtn.addEventListener("click", async () => {
  const f = fileInput.files[0];
  if (!f) return;

  const body = new FormData();
  body.append("file", f);

  uploadBtn.disabled = true;
  setNote("Reading, chunking, embedding…", "");

  try {
    const res = await fetch("/upload", { method: "POST", body });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Upload failed.");
    setNote(`Indexed ${data.chunks} chunks from ${data.filename}. Ask away.`, "ok");
    enableChat();
  } catch (err) {
    setNote(err.message, "err");
    uploadBtn.disabled = false;
  }
});

function setNote(text, kind) {
  uploadNote.textContent = text;
  uploadNote.className = "upload-note" + (kind ? " " + kind : "");
}

function enableChat() {
  hasDoc = true;
  question.disabled = false;
  sendBtn.disabled = false;
  if (empty) empty.remove();
}

sendBtn.addEventListener("click", ask);
question.addEventListener("keydown", (e) => { if (e.key === "Enter") ask(); });

async function ask() {
  const q = question.value.trim();
  if (!q || !hasDoc) return;

  addMsg(q, "user");
  question.value = "";
  sendBtn.disabled = true;
  const thinking = addMsg("flipping to the right page…", "bot thinking");

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q, model: modelSelect.value }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    thinking.textContent = data.answer;
    thinking.className = "msg bot";
  } catch (err) {
    thinking.textContent = err.message;
    thinking.className = "msg bot";
  } finally {
    sendBtn.disabled = false;
    question.focus();
  }
}

function addMsg(text, cls) {
  const el = document.createElement("div");
  el.className = "msg " + cls;
  el.textContent = text;
  messages.appendChild(el);
  el.scrollIntoView({ behavior: "smooth", block: "end" });
  return el;
}
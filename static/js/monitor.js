async function updateStatus() {
    try {
        const response = await fetch('/getinfo');
        const data = await response.json();

        updateElement("google", data.google);
        updateElement("github", data.github);

    } catch (err) {
        console.error("更新エラー:", err);
    }
}

function updateElement(name, info) {
    if (!info) return;

    const card = document.getElementById(`card-${name}`);
    const statusText = document.getElementById(`status-${name}`);
    const latencyText = document.getElementById(`latency-${name}`);
    const iconImg = document.getElementById(`icon-${name}`);

    statusText.innerText = info.status === 'ok' ? "正常" : (info.status === 'slow' ? "遅延" : "停止中");
    latencyText.innerText = info.latency;
    card.className = `card status-${info.status}`;
    iconImg.src = `/static/icons/${info.status}.svg`;
}

setInterval(updateStatus, 10000);
updateStatus();
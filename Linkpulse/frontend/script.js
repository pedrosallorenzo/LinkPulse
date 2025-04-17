async function fetchLinks() {
    const res = await fetch("/status");
    const links = await res.json();
    const list = document.getElementById("list");
    list.innerHTML = "";
    links.forEach(link => {
      const li = document.createElement("li");
      li.textContent = `${link.url} - ${link.status}`;
      list.appendChild(li);
    });
  }
  async function addUrl() {
    const url = document.getElementById("urlInput").value;
    await fetch(`/add?url=${encodeURIComponent(url)}`, { method: "POST" });
    fetchLinks();
  }
  fetchLinks();
  setInterval(fetchLinks, 10000);

const addBtn = document.getElementById("addBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const tableBody = document.querySelector("#portfolioTable tbody");

addBtn.addEventListener("click", () => {
  const symbol = document.getElementById("symbolInput").value.trim();
  const quantity = document.getElementById("quantityInput").value.trim();

  if (!symbol || !quantity) {
    alert("Please enter both symbol and quantity");
    return;
  }

  // Add row to table
  const row = document.createElement("tr");
  row.innerHTML = `
<td>${symbol}</td>
<td>${quantity}</td>
  `;
  tableBody.appendChild(row);

  // Clear inputs
  document.getElementById("symbolInput").value = "";
  document.getElementById("quantityInput").value = "";
});

analyzeBtn.addEventListener("click", async () => {
  document.getElementById("loading").style.display = "block";
  document.getElementById("portfolioResults").innerHTML = "";

  // Collect portfolio rows
  const rows = tableBody.querySelectorAll("tr");
  const portfolio = [];
  rows.forEach(row => {
    const symbol = row.cells[0].innerText;
    const quantity = parseInt(row.cells[1].innerText);
    portfolio.push({ symbol, quantity });
  });

  // Collect risk
  const risk = document.getElementById("riskSelect").value;

  const payload = { portfolio, risk };

  try {
    const response = await fetch("/portfolio-analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    document.getElementById("loading").style.display = "none";

    let html = `<h3>Portfolio Analysis Results</h3>`;

    // Chart + Breakdown side by side
    if (data.sector_chart_base64 || data.sector_breakdown) {
      html += `<div class="chart-breakdown">`;

      // Chart first
      if (data.sector_chart_base64) {
        html += `
<div class="chart">
<h4>Sector Chart</h4>
<img src="data:image/png;base64,${data.sector_chart_base64}"
                 alt="Sector Chart" style="max-width:100%;">
</div>
        `;
      }

      // Breakdown table beside chart
      if (data.sector_breakdown) {
        html += `
<div class="breakdown">
<h4>Sector Breakdown</h4>
<table border="1" cellpadding="8" cellspacing="0">
<thead><tr><th>Sector</th><th>Weight</th></tr></thead>
<tbody>
        `;
        for (const [sector, weight] of Object.entries(data.sector_breakdown)) {
          html += `<tr><td>${sector}</td><td>${weight}</td></tr>`;
        }
        html += `</tbody></table></div>`;
      }

      html += `</div>`; // close chart-breakdown flex container
    }

    // Insights & Recommendations below
    html += `
<h4>AI Insights</h4>
<div class="markdown">${marked.parse(data.ai_insights || "")}</div>
<h4>Recommendations</h4>
<div class="markdown">${marked.parse(data.recommendations || "")}</div>
    `;

    document.getElementById("portfolioResults").innerHTML = html;

  } catch (error) {
    document.getElementById("loading").style.display = "none";
    document.getElementById("portfolioResults").innerHTML =
      `<p style="color:red;">Error: ${error.message}</p>`;
  }
});
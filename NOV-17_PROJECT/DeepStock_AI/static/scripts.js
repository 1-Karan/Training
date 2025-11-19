import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

document.getElementById("queryForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const query = document.getElementById("userQuery").value;
  document.getElementById("loading").style.display = "block";
  document.getElementById("results").innerHTML = "";

  try {
    const response = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_query: query })
    });

    const data = await response.json();
    document.getElementById("loading").style.display = "none";

    let html = `
      <h3>Results</h3>
      <p><strong>Query:</strong> ${data.query}</p>
      <p><strong>Stock Symbol:</strong> ${data.stock_symbol}</p>
    `;

    // Chart first
    if (data.chart_base64) {
      html += `<h4>Stock Chart</h4>
      <img src="data:image/png;base64,${data.chart_base64}" alt="Stock Chart" style="max-width:100%;">`;
    }

    // Then Stock Data Table
    if (data.stock_data && data.stock_data.length > 0) {
      html += `<h4>Last 7 days Stock Data</h4>
      <table border="1" cellpadding="8" cellspacing="0">
      <thead>
        <tr>
          <th>Open</th><th>Close</th><th>High</th><th>Low</th><th>Volume</th>
        </tr>
      </thead>
      <tbody>`;
      data.stock_data.forEach(row => {
        html += `<tr>
          <td>${row.Open.toFixed(2)}</td>
          <td>${row.Close.toFixed(2)}</td>
          <td>${row.High.toFixed(2)}</td>
          <td>${row.Low.toFixed(2)}</td>
          <td>${row.Volume}</td>
        </tr>`;
      });
      html += `</tbody></table>`;
    }

    // Then News Summary
    if (data.news_summary) {
      html += `<h4>News Summary</h4>
      <div class="markdown">${marked.parse(data.news_summary)}</div>`;
    }

    // Then Insights
    if (data.insights) {
      html += `<h4>Insights</h4>
      <div class="markdown">${marked.parse(data.insights)}</div>`;
    }

    // Finally Sentiment Results
    if (data.sentiment_results && data.sentiment_results.length > 0) {
      html += `<h4>Sentiment Results</h4>
      <table border="1" cellpadding="8" cellspacing="0">
      <thead>
        <tr>
          <th>Title</th><th>Snippet</th><th>URL</th><th>Sentiment</th><th>Score</th>
        </tr>
      </thead>
      <tbody>`;
      data.sentiment_results.forEach(row => {
        html += `<tr>
          <td>${row.title}</td>
          <td>${row.snippet}</td>
          <td><a href="${row.url}" target="_blank">Read Article</a></td>
          <td>${row.sentiment}</td>
          <td>${row.score}</td>
        </tr>`;
      });
      html += `</tbody></table>`;
    }

    document.getElementById("results").innerHTML = html;

  } catch (error) {
    document.getElementById("loading").style.display = "none";
    document.getElementById("results").innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
});




document.getElementById("health-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    revenue: Number(form.revenue.value),
    expenses: Number(form.expenses.value),
    debt: Number(form.debt.value),
    assets: Number(form.assets.value),
    cash: Number(form.cash.value),
    receivables: Number(form.receivables.value),
    payables: Number(form.payables.value),
    years: Number(form.years.value),
  };

  const res = await fetch("https://financial-health-tool.onrender.com/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const result = await res.json();
  const resultDiv = document.getElementById("result");
  resultDiv.classList.remove("hidden");
  resultDiv.innerHTML = `
    <h2>Your Score: ${result.score}/100</h2>
    <p>Assessment: ${result.assessment}</p>
    <h3>${result.cta}</h3>
    <a href="${result.link}" target="_blank">
      <button>Book a Free Call</button>
    </a>
  `;
});
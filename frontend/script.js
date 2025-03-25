document.getElementById("health-form").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const errorMsg = document.getElementById("error-msg");
  errorMsg.textContent = "";
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

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.error || "An error occurred.");
    }

    const result = await res.json();
    document.getElementById("result").classList.remove("hidden");
    document.getElementById("assessment").textContent = "Assessment: " + result.assessment;
    document.getElementById("cta-text").textContent = result.cta;
    document.getElementById("cta-link").href = result.link;

    animateScore(result.score);

    const ctx = document.getElementById("breakdownChart").getContext("2d");
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: Object.keys(result.breakdown),
        datasets: [{
          label: 'Score Breakdown',
          data: Object.values(result.breakdown),
          backgroundColor: '#0a2e57'
        }]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                const label = context.label;
                return label + ': ' + result.suggestions[label];
              }
            }
          }
        },
        scales: {
          y: { beginAtZero: true, max: 25 }
        }
      }
    });

    const suggestionDiv = document.getElementById("suggestions");
    suggestionDiv.innerHTML = "<h4>Suggestions:</h4><ul>" + Object.entries(result.suggestions).map(([k, v]) => `<li><strong>${k}:</strong> ${v}</li>`).join('') + "</ul>";

  } catch (err) {
    errorMsg.textContent = err.message;
  }
});

function animateScore(finalScore) {
  const el = document.getElementById("animated-score");
  let current = 0;
  const interval = setInterval(() => {
    current++;
    el.textContent = current;
    if (current >= finalScore) clearInterval(interval);
  }, 15);
}
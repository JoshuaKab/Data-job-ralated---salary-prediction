const form = document.querySelector("#salary-form");
const resultContent = document.querySelector("#result-content");
const submitButton = form.querySelector("button[type='submit']");
const buttonLabel = submitButton.querySelector(".button-label");
const currencyFormatter = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 0,
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  submitButton.disabled = true;
  buttonLabel.textContent = "Finding your estimate...";
  resultContent.innerHTML = `
    <p class="result-placeholder">Crunching the numbers...</p>
    <p class="result-helper">Matching your profile with the salary model.</p>
  `;

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      throw new Error("We couldn't calculate your estimate right now. Please try again.");
    }

    const { predicted_salary_usd: salary } = await response.json();
    if (!Number.isFinite(salary)) {
      throw new Error("The salary model returned an invalid estimate. Please try again.");
    }

    resultContent.innerHTML = `
      <p class="result-value">$${currencyFormatter.format(salary)}</p>
      <p class="result-caption">Estimated annual salary based on the profile you shared.</p>
    `;
  } catch (error) {
    resultContent.innerHTML = `
      <p class="result-placeholder result-error">Estimate unavailable</p>
      <p class="result-caption">${escapeHtml(error.message)}</p>
    `;
  } finally {
    submitButton.disabled = false;
    buttonLabel.textContent = "Calculate my estimate";
  }
});

function escapeHtml(value) {
  const element = document.createElement("span");
  element.textContent = value;
  return element.innerHTML;
}

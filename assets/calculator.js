(() => {
  const form = document.getElementById('scenario-form');
  if (!form) return;

  const resultNodes = {
    live: document.getElementById('result-live'),
    rent: document.getElementById('result-rent'),
    sale: document.getElementById('result-sale'),
    message: document.getElementById('result-message')
  };
  const money = new Intl.NumberFormat('en-US', {
    style: 'currency', currency: 'USD', maximumFractionDigits: 0
  });

  function valueOf(name) {
    const field = form.elements.namedItem(name);
    if (!field || field.value.trim() === '') return null;
    const value = Number(field.value);
    return Number.isFinite(value) ? value : null;
  }

  function show(node, value, note) {
    node.innerHTML = `<strong class="result-value">${money.format(value)}</strong><p>${note}</p>`;
  }

  function resetResults() {
    resultNodes.live.innerHTML = '<strong class="result-value">Not calculated</strong><p>Enter both live-in inputs to show this scenario.</p>';
    resultNodes.rent.innerHTML = '<strong class="result-value">Not calculated</strong><p>Enter both rental inputs to show this scenario.</p>';
    resultNodes.sale.innerHTML = '<strong class="result-value">Not calculated</strong><p>Enter all sale and investment assumptions to show this scenario.</p>';
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const homeB = valueOf('homeB-net');
    const liveCost = valueOf('live-cost');
    const housingAvoided = valueOf('housing-avoided');
    const rent = valueOf('homeA-rent');
    const rentalCosts = valueOf('rental-costs');
    const salePrice = valueOf('sale-price');
    const saleCosts = valueOf('sale-costs');
    const payoff = valueOf('loan-payoff');
    const saleTax = valueOf('sale-tax');
    const years = valueOf('investment-years');
    const annualReturn = valueOf('annual-return');
    let completed = 0;

    resetResults();

    if (liveCost !== null && housingAvoided !== null) {
      const total = (homeB ?? 0) + housingAvoided - liveCost;
      show(
        resultNodes.live,
        total,
        `Annual combined cash-flow proxy before income tax; ${homeB === null ? 'Home B excluded because its field was blank' : 'includes your Home B net-cash-flow input'}.`
      );
      completed++;
    }

    if (rent !== null && rentalCosts !== null) {
      const total = (homeB ?? 0) + rent - rentalCosts;
      show(
        resultNodes.rent,
        total,
        `Annual combined rental cash-flow proxy before income tax; ${homeB === null ? 'Home B excluded because its field was blank' : 'includes your Home B net-cash-flow input'}.`
      );
      completed++;
    }

    if (
      salePrice !== null && saleCosts !== null && payoff !== null &&
      saleTax !== null && years !== null && annualReturn !== null
    ) {
      const proceeds = salePrice - saleCosts - payoff - saleTax;
      const futureValue = proceeds * Math.pow(1 + annualReturn / 100, years);
      show(
        resultNodes.sale,
        futureValue,
        `Illustrative terminal value after ${years} year${years === 1 ? '' : 's'} using your ${annualReturn}% annual-return assumption. Starting proceeds: ${money.format(proceeds)}. Home B and any unentered costs or taxes are excluded.`
      );
      completed++;
    }

    resultNodes.message.textContent = completed
      ? 'Illustration only. Inputs stay in this browser session and are not saved or transmitted. The worksheet does not calculate taxes, property values, rents, or expected investment returns.'
      : 'Enter the required blank assumptions for at least one scenario. A blank field is never treated as zero.';
  });

  form.addEventListener('reset', () => {
    window.setTimeout(() => {
      resetResults();
      resultNodes.message.textContent = 'All inputs start blank. No values are saved or sent anywhere.';
    }, 0);
  });
})();

/*
 * Privacy-safe, browser-only calculators for Property Plan.
 * No network calls, cookies, storage, analytics, or form submission.
 */
(() => {
  'use strict';

  const PROP19_CAP_ADJUSTMENT = 1_044_586;
  const money = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 2
  });
  const number = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });
  const byId = (id) => document.getElementById(id);
  const allForms = Array.from(document.querySelectorAll('form[data-calculator]'));

  function readNumber(input) {
    if (!input || input.value.trim() === '') return { valid: false, reason: 'blank' };
    const parsed = Number(input.value);
    if (!Number.isFinite(parsed)) return { valid: false, reason: 'invalid' };
    if (parsed < 0) return { valid: false, reason: 'negative' };
    return { valid: true, value: parsed };
  }

  function showResult(container, title, detail, isError = false) {
    if (!container) return;
    container.replaceChildren();
    container.classList.toggle('calc-error', isError);
    const heading = document.createElement('h4');
    heading.textContent = title;
    const paragraph = document.createElement('p');
    paragraph.textContent = detail;
    container.append(heading, paragraph);
    container.hidden = false;
  }

  function hideResult(id) {
    const result = byId(id);
    if (!result) return;
    result.hidden = true;
    result.classList.remove('calc-error');
    result.replaceChildren();
  }

  function validationMessage(label, parsed) {
    if (parsed.reason === 'blank') return `Enter ${label} before running the estimate.`;
    if (parsed.reason === 'negative') return `${label[0].toUpperCase()}${label.slice(1)} must be zero or greater.`;
    return `Check the ${label} value and try again.`;
  }

  function requireInputs(container, fields) {
    const missing = fields.find((field) => !field.parsed.valid);
    if (!missing) return true;
    showResult(container, 'A value is needed', validationMessage(missing.label, missing.parsed), true);
    missing.input?.focus();
    return false;
  }

  function addCalculatorHandler(formId, resultId, handler) {
    const form = byId(formId);
    if (!form) return;
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const result = byId(resultId);
      if (result) {
        result.hidden = true;
        result.classList.remove('calc-error');
      }
      handler(form, result);
    });
    form.addEventListener('reset', () => {
      window.setTimeout(() => hideResult(resultId), 0);
    });
  }

  // Tabs are ordinary in-page controls; selecting one never changes the URL or stores state.
  const tabs = Array.from(document.querySelectorAll('[data-tool-tab]'));
  const panels = Array.from(document.querySelectorAll('[data-tool-panel]'));
  function selectTool(name, focusTab = false) {
    for (const tab of tabs) {
      const selected = tab.dataset.toolTab === name;
      tab.classList.toggle('is-selected', selected);
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (selected && focusTab) tab.focus();
    }
    for (const panel of panels) panel.hidden = panel.dataset.toolPanel !== name;
  }
  for (const tab of tabs) {
    tab.addEventListener('click', () => selectTool(tab.dataset.toolTab));
    tab.addEventListener('keydown', (event) => {
      const current = tabs.indexOf(tab);
      let next = current;
      if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (current + 1) % tabs.length;
      else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (current - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      selectTool(tabs[next].dataset.toolTab, true);
    });
  }

  const waterPlan = byId('water-plan');
  const waterUnitsField = byId('water-units-field');
  function updateWaterUnitsVisibility() {
    if (waterUnitsField && waterPlan) waterUnitsField.hidden = waterPlan.value !== 'sf-multi';
  }
  waterPlan?.addEventListener('change', () => {
    updateWaterUnitsVisibility();
    if (waterPlan.value !== 'sf-multi' && byId('water-units')) byId('water-units').value = '';
  });

  // SFPUC source citations inside collapsed groups remain reachable by their links.
  function expandSourceTarget() {
    if (!window.location.hash) return;
    let id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); }
    catch { id = window.location.hash.slice(1); }
    const target = byId(id);
    const details = target?.closest('details');
    if (details) {
      details.open = true;
      window.requestAnimationFrame(() => target?.scrollIntoView({ block: 'center' }));
    }
  }
  window.addEventListener('hashchange', expandSourceTarget);
  expandSourceTarget();

  addCalculatorHandler('prop19-form', 'prop19-result', (form, result) => {
    const baseInput = form.elements.namedItem('base');
    const marketInput = form.elements.namedItem('market');
    const base = readNumber(baseInput);
    const market = readNumber(marketInput);
    if (!requireInputs(result, [
      { input: baseInput, parsed: base, label: 'the factored base-year value' },
      { input: marketInput, parsed: market, label: 'the transfer-date full cash value' }
    ])) return;

    const taxableValue = base.value + Math.max(0, market.value - base.value - PROP19_CAP_ADJUSTMENT);
    const excludedIncrease = Math.max(0, market.value - taxableValue);
    showResult(
      result,
      `Screened taxable value: ${money.format(taxableValue)}`,
      `Simple full-interest arithmetic for the 16 Feb 2025–15 Feb 2027 value-cap window. This screens only the value formula; it does not establish family relationship, home or unit eligibility, occupancy, ownership share, claim timing, or the assessor’s enrolled value. The estimate excludes ${money.format(excludedIncrease)} of the transfer-date value under this formula.`
    );
  });

  addCalculatorHandler('tax-form', 'tax-result', (form, result) => {
    const assessedInput = form.elements.namedItem('assessed');
    const rateInput = form.elements.namedItem('rate');
    const assessed = readNumber(assessedInput);
    const rate = readNumber(rateInput);
    if (!requireInputs(result, [
      { input: assessedInput, parsed: assessed, label: 'the taxable assessed value' },
      { input: rateInput, parsed: rate, label: 'the combined tax rate' }
    ])) return;
    if (rate.value > 100) {
      showResult(result, 'Check the rate', 'Enter the rate as a percentage from 0 to 100, for example 1.18 for 1.18%.', true);
      rateInput.focus();
      return;
    }
    const annualTax = assessed.value * rate.value / 100;
    showResult(
      result,
      `Illustrative annual ad valorem amount: ${money.format(annualTax)}`,
      `Calculation: ${money.format(assessed.value)} assessed value × ${number.format(rate.value)}%. This excludes parcel taxes, direct charges, special assessments, supplemental or escape bills, exemptions, and installment timing.`
    );
  });

  function tieredCharge(ccf, tiers) {
    let remaining = ccf;
    let total = 0;
    for (const tier of tiers) {
      const volume = Math.max(0, Math.min(remaining, tier.limit));
      total += volume * tier.rate;
      remaining -= volume;
      if (remaining <= 0) break;
    }
    if (remaining > 0 && tiers.length) total += remaining * tiers[tiers.length - 1].rate;
    return total;
  }

  const waterPlans = {
    sjw: {
      label: 'San Jose Water residential 5/8-inch service',
      service: 79.67,
      tiers: [
        { limit: 6, rate: 5.0355 },
        { limit: 6, rate: 7.5156 },
        { limit: Infinity, rate: 14.3548 }
      ],
      citation: 'AL 629-A, effective 1 Jul 2026.'
    },
    calwater: {
      label: 'Cal Water Los Altos Tariff Area, single-family residential 5/8-inch service',
      service: 48.86,
      tiers: [
        { limit: 6, rate: 2.8466 },
        { limit: 14, rate: 11.3542 },
        { limit: 10, rate: 14.2607 },
        { limit: Infinity, rate: 17.0381 }
      ],
      citation: 'Residential tariff effective 1 Oct 2026.'
    }
  };

  addCalculatorHandler('water-form', 'water-result', (form, result) => {
    const planInput = form.elements.namedItem('plan');
    const ccfInput = form.elements.namedItem('ccf');
    const unitsInput = form.elements.namedItem('units');
    const plan = planInput.value;
    if (!['sjw', 'calwater', 'sf-single', 'sf-multi'].includes(plan)) {
      showResult(result, 'Choose a tariff', 'Select the verified provider and account class shown on the actual utility bill.', true);
      planInput.focus();
      return;
    }
    const ccf = readNumber(ccfInput);
    if (!requireInputs(result, [{ input: ccfInput, parsed: ccf, label: 'monthly water use in CCF' }])) return;

    if (plan === 'sf-multi') {
      const unitCount = readNumber(unitsInput);
      if (!requireInputs(result, [{ input: unitsInput, parsed: unitCount, label: 'the dwelling-unit count' }])) return;
      if (!Number.isInteger(unitCount.value) || unitCount.value < 1) {
        showResult(result, 'Check the unit count', 'Enter a whole number of one or more dwelling units for the SFPUC multi-family tariff.', true);
        unitsInput.focus();
        return;
      }
    }

    if (plan === 'sjw' || plan === 'calwater') {
      const selected = waterPlans[plan];
      const usageCharge = tieredCharge(ccf.value, selected.tiers);
      const total = selected.service + usageCharge;
      showResult(
        result,
        `Illustrative monthly water-service charge: ${money.format(total)}`,
        `${selected.label}: ${money.format(selected.service)} monthly service charge plus ${money.format(usageCharge)} for ${number.format(ccf.value)} CCF. ${selected.citation} Excludes separate surcharges/surcredits, taxes, and non-water charges; confirm service territory, meter, and account.`
      );
      return;
    }

    const isMulti = plan === 'sf-multi';
    const waterRate = isMulti ? 12.03 : 12.20;
    const waterFirstTier = isMulti ? 3 * Number(unitsInput.value) : 4;
    const waterAdditionalRate = isMulti ? 12.91 : 13.55;
    const waterVolumeCharge = Math.min(ccf.value, waterFirstTier) * waterRate
      + Math.max(0, ccf.value - waterFirstTier) * waterAdditionalRate;
    const sewerFlowFactor = isMulti ? 0.95 : 0.90;
    const sewerCharge = 6.62 + (ccf.value * sewerFlowFactor * 20.74);
    const sfWaterService = 19.65;
    const total = sfWaterService + waterVolumeCharge + sewerCharge;
    const classLabel = isMulti ? `multi-family, ${Number(unitsInput.value)} dwelling unit(s)` : 'single-family';
    showResult(
      result,
      `Illustrative monthly SFPUC water + sewer: ${money.format(total)}`,
      `FY 2026–27 ${classLabel}, 5/8-inch meter: ${money.format(sfWaterService)} water service + ${money.format(waterVolumeCharge)} water use + ${money.format(sewerCharge)} residential sewer, using the default ${number.format(sewerFlowFactor * 100)}% flow factor. Excludes stormwater, drought surcharge, parcel-based charges, account-specific adjustments, and other fees; actual meter, account class, and flow factor control.`
    );
  });

  addCalculatorHandler('rent-form', 'rent-result', (form, result) => {
    const ruleInput = form.elements.namedItem('rule');
    const baseInput = form.elements.namedItem('base');
    const rule = ruleInput.value;
    if (!rule) {
      showResult(result, 'Choose a verified coverage category', 'Select a published percentage only after checking which law applies to the unit.', true);
      ruleInput.focus();
      return;
    }
    const base = readNumber(baseInput);
    if (!requireInputs(result, [{ input: baseInput, parsed: base, label: 'the current lawful base rent' }])) return;
    const rate = rule === 'local' ? 0.016 : 0.088;
    const rateLabel = rule === 'local' ? '1.6% SF Rent Ordinance reference' : '8.8% AB 1482 reference';
    const increase = base.value * rate;
    showResult(
      result,
      `Arithmetic only: ${money.format(increase)} at ${number.format(rate * 100)}%`,
      `Applying the ${rateLabel} to the entered base rent gives ${money.format(base.value + increase)} before rounding. This is not authorization to raise rent and does not account for coverage, a different effective date, unit exemptions, banked increases, prior increases, notices, or local protections.`
    );
  });

  addCalculatorHandler('holding-form', 'holding-result', (form, result) => {
    const fields = Array.from(form.querySelectorAll('input[type="number"]'));
    const entered = fields
      .map((input) => ({ input, parsed: readNumber(input), label: input.closest('label')?.querySelector('span')?.textContent?.trim() || 'cost' }))
      .filter((field) => field.parsed.valid);
    const firstInvalid = fields.map((input) => ({ input, parsed: readNumber(input) })).find(({ parsed }) => parsed.reason === 'negative' || parsed.reason === 'invalid');
    if (firstInvalid) {
      showResult(result, 'Check the entered amounts', 'Enter zero or a positive annual amount for each cost, or leave a field blank.', true);
      firstInvalid.input.focus();
      return;
    }
    if (entered.length === 0) {
      showResult(result, 'No amounts entered', 'Enter at least one known annual amount from a bill or quote. Blank fields are not treated as zero.', true);
      fields[0]?.focus();
      return;
    }
    const total = entered.reduce((sum, field) => sum + field.parsed.value, 0);
    const included = entered.map((field) => `${field.label}: ${money.format(field.parsed.value)}`).join(' · ');
    showResult(
      result,
      `Entered annual total: ${money.format(total)}`,
      `${included}. Monthly equivalent: ${money.format(total / 12)}. Only the amounts entered are included; this is not a forecast or complete ownership-cost analysis.`
    );
  });

  function clearAllInputs() {
    for (const form of allForms) form.reset();
    for (const result of document.querySelectorAll('.calc-result')) {
      result.hidden = true;
      result.classList.remove('calc-error');
      result.replaceChildren();
    }
    updateWaterUnitsVisibility();
  }

  document.querySelector('[data-clear-all]')?.addEventListener('click', clearAllInputs);

  // Remove transient entries before a document is cached or restored in the same tab.
  window.addEventListener('pagehide', clearAllInputs);
  window.addEventListener('pageshow', (event) => {
    if (event.persisted) clearAllInputs();
  });

  updateWaterUnitsVisibility();
})();

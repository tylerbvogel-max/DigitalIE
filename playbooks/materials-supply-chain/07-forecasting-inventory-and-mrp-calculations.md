# Forecasting, inventory, and MRP calculations

## Question answered

Given a declared demand history and planning policy, what reproducible forecast, error measures, replenishment quantities, reorder point, and time-phased material plan follow?

## Forecast calculations

For a trailing window of (n) observations:

\[
F_{t+1}=\frac{1}{n}\sum_{i=t-n+1}^{t}A_i
\]

Simple exponential smoothing uses:

\[
F_{t+1}=\alpha A_t+(1-\alpha)F_t,\qquad 0<\alpha\leq1
\]

The functions preserve fitted-forecast alignment so actual period (t) is never used to forecast itself. They do not choose the window, alpha, history boundary, treatment of outliers, causal drivers, or seasonal model.

With error defined as (e_t=A_t-F_t):

\[
ME=\frac{\sum e_t}{n},\quad MAD=\frac{\sum|e_t|}{n},\quad
MSE=\frac{\sum e_t^2}{n},\quad RMSE=\sqrt{MSE}
\]

\[
MAPE=\frac{100}{m}\sum_{A_t\ne0}\left|\frac{e_t}{A_t}\right|,qquad
TrackingSignal=\frac{\sum e_t}{MAD}
\]

The receipt identifies zero actuals excluded from MAPE. MAPE can be misleading for intermittent and near-zero demand; do not silently substitute it for a fit-for-purpose metric.

## Economic order quantity

Under constant demand, instantaneous replenishment, no shortages, no quantity discounts, and constant ordering and holding costs:

\[
EOQ=\sqrt{\frac{2DS}{H}}
\]

where (D) is annual demand, (S) is cost per order, and (H) is annual holding cost per unit. Cycle stock is (Q/2), ordering cost is ((D/Q)S), and cycle-stock holding cost is ((Q/2)H). The classical optimum balances those two relevant costs. Aerospace shelf life, minimum buys, test lot constraints, obsolescence, traceability, long lead items, and quantity breaks commonly violate the model.

## Reorder point and safety stock

For constant lead time (L), independent period demand with mean (d) and standard deviation \(\sigma_d\), and a supplied service factor (z):

\[
\mu_L=dL,\qquad \sigma_L=\sigma_d\sqrt{L},\qquad
SS=z\sigma_L,\qquad ROP=\mu_L+SS
\]

The calculator does not convert a desired service level to (z); that choice and the service definition remain visible. Correlated demand, uncertain lead time, order crossover, repairables, multi-echelon inventory, and non-normal demand require another model.

## Single-item MRP netting

For each period, projected available before a new plan is:

\[
PAB_t^{pre}=PAB_{t-1}+ScheduledReceipts_t-GrossRequirements_t
\]

If this falls below safety stock:

\[
NetRequirements_t=SafetyStock-PAB_t^{pre}
\]

Lot-for-lot receipts equal net requirements. With a fixed order quantity (Q), the receipt is \(Q\lceil NR_t/Q\rceil\). Planned releases are offset by the declared integer lead time. A required release before the horizon is returned as past due rather than placed invisibly into period zero.

This is transparent single-item netting, not a complete MRP engine. Gross requirements must already reflect the approved BOM quantity, yield/scrap policy, parent releases, effectivity, unit of measure, and low-level coding. It does not perform BOM explosion, capacity checks, pegging, alternates, reschedule messages, or configuration effectivity.

## Worked example

With annual demand 10,000 units, order cost $50, and annual holding cost $2 per unit:

```text
EOQ = sqrt(2 × 10,000 × 50 / 2) = 707.107 units
orders/year = 10,000 / 707.107 = 14.142
cycle stock = 353.553 units
annual ordering cost = annual cycle-stock holding cost = $707.107
```

With mean demand 100 per period, four-period lead time, period standard deviation 10, and supplied (z=1.645): expected lead-time demand is 400, lead-time standard deviation is 20, safety stock is 32.9, and reorder point is 432.9.

## Output

Record item/configuration identity, site, planning horizon, bucket and unit definitions, source dates, demand treatment, policy assumptions, raw inputs, results, exceptions, sensitivity cases, and planner disposition.

Primary public orientation: [MIT Logistics Systems inventory notes](https://ocw.mit.edu/courses/esd-260j-logistics-systems-fall-2006/resources/lect11/) and [MIT Operations Management inventory case formulation](https://ocw.mit.edu/courses/15-761-introduction-to-operations-management-spring-2013/pages/case-preparation-questions/). Approved ERP logic, planning procedures, contractual priorities, and controlled master data govern actual use.

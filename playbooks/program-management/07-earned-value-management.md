# Earned value management

## Question answered

At a declared status date and baseline scope, what work was planned, what budgeted work was objectively accomplished, what cost was incurred, what performance does that imply, and what assumptions produce each completion forecast?

EVM integrates scope, schedule, technical accomplishment, resources, and cost. It is not a financial variance dashboard and the equations do not establish that the underlying EVMS is compliant.

## Input contract

Before calculating, record:

- status/data date and accounting period;
- baseline identifier/version and approval state;
- WBS, control account, work package, and organizational scope;
- value units and whether values are current-period or cumulative;
- Planned Value (`PV`/`BCWS`), Earned Value (`EV`/`BCWP`), Actual Cost (`AC`/`ACWP`), and Budget at Completion (`BAC`);
- earned-value technique and objective completion evidence;
- actual-cost source, estimated actuals, accruals, and reconciliation state;
- management Estimate to Complete (`ETC`) and its resource/risk assumptions where available;
- Level of Effort (`LOE`), material, subcontract, undistributed-budget, management-reserve, and over-target treatment.

Do not combine values across different status dates, baseline versions, scopes, currencies, or unit bases. Performance Measurement Baseline, Management Reserve, Contract Budget Base, and Total Allocated Budget are not interchangeable.

## Performance snapshot

For cumulative values at the same status date:

\[
CV=EV-AC, \qquad SV=EV-PV
\]

\[
CV\%=100\frac{CV}{EV}, \qquad SV\%=100\frac{SV}{PV}
\]

\[
CPI=\frac{EV}{AC}, \qquad SPI=\frac{EV}{PV}
\]

\[
\%Scheduled=100\frac{PV}{BAC}, \quad
\%Complete=100\frac{EV}{BAC}, \quad
\%Spent=100\frac{AC}{BAC}
\]

\[
WR=BAC-EV, \qquad EAC_{management}=AC+ETC, \qquad VAC=BAC-EAC
\]

Positive CV/SV and CPI/SPI above 1 conventionally indicate favorable arithmetic performance. Apply program-approved thresholds and investigate drivers; the calculator does not declare health. Percentage conventions can differ, so reports must name their denominator. This pack uses `CV/EV` and `SV/PV`.

Schedule variance is expressed in budget units or hours. It is not calendar delay. SPI can return to 1.0 at completion and cannot identify the critical-path effect. Always pair material schedule conclusions with IMS analysis.

## Forecast alternatives

Calculated EACs are scenarios, not substitutes for a resource-loaded bottom-up ETC:

\[
EAC_{CPI}=AC+\frac{BAC-EV}{CPI}
\]

This assumes cumulative cost efficiency continues.

\[
EAC_{composite}=AC+\frac{BAC-EV}{CPI\times SPI}
\]

This assumes cost and schedule efficiency both affect remaining cost. It becomes less informative when SPI loses sensitivity near completion.

For a declared recent window:

\[
CPI_{recent}=\frac{\sum EV_{period}}{\sum AC_{period}}, \qquad
EAC_{recent}=AC+\frac{BAC-EV}{CPI_{recent}}
\]

Do not average monthly CPI values; aggregate their numerators and denominators. A management forecast is:

\[
EAC_{management}=AC+ETC_{bottom-up}
\]

Compare rather than blend the alternatives. Large separation is a prompt to challenge remaining scope, rates, quantities, productivity, schedule, risk, and opportunity.

Required future efficiency is:

\[
TCPI_{BAC}=\frac{BAC-EV}{BAC-AC}, \qquad
TCPI_{EAC}=\frac{BAC-EV}{EAC-AC}
\]

Compare TCPI with demonstrated CPI and explain why the target is credible. An undefined denominator is reported as undefined, not zero.

## Period reconciliation

For each metric \(M\in\{PV,EV,AC\}\):

\[
M_{calculated,cum}=\sum_{t=1}^{T}M_t
\]

\[
\Delta_M=M_{reported,cum}-M_{calculated,cum}
\]

Investigate deltas outside the declared numeric tolerance before using derived metrics. A zero reconciliation delta does not validate scope alignment or source accounting.

## Schedule execution indicators

\[
BEI=\frac{\text{baseline tasks completed}}{\text{baseline tasks with baseline finish on/before status period}}
\]

\[
Hit/Miss\%=100\frac{\text{period tasks completed on/before baseline finish}}{\text{tasks baselined to finish in period}}
\]

These count-based indicators supplement, but do not replace, logic, constraint, float, driving-path, and critical-path analysis. Define task inclusion, LOE, summary tasks, baseline changes, and completion criteria before comparing periods.

## Labor and material variance decomposition

For labor:

\[
RateVar=(BudgetRate-ActualRate)\times ActualHours
\]

\[
VolumeVar=(EarnedHours-ActualHours)\times BudgetRate
\]

\[
LaborCV=RateVar+VolumeVar
\]

For material:

\[
PriceVar=(BudgetUnitPrice-ActualUnitPrice)\times ActualQuantity
\]

\[
UsageVar=(EarnedQuantity-ActualQuantity)\times BudgetUnitPrice
\]

\[
MaterialCV=PriceVar+UsageVar
\]

Reconcile each decomposition to earned budget minus actual cost for the same element of cost and scope. Timing, accruals, indirect rates, scrap, substitutions, and purchase/usage recognition may require further analysis.

## Worked snapshot

For a fictional control account at one status date:

```text
PV = 1,000; EV = 900; AC = 950; BAC = 5,000; management ETC = 4,200
CV = 900 - 950 = -50
SV = 900 - 1,000 = -100
CPI = 900 / 950 = 0.947368
SPI = 900 / 1,000 = 0.900000
% complete = 100(900 / 5,000) = 18.0%
% spent = 100(950 / 5,000) = 19.0%
WR = 5,000 - 900 = 4,100
EAC management = 950 + 4,200 = 5,150
VAC management = 5,000 - 5,150 = -150
EAC CPI = 950 + 4,100 / 0.947368 = 5,277.778
EAC composite = 950 + 4,100 / ((900 / 950) × (900 / 1,000)) = 5,758.642
TCPI BAC = 4,100 / (5,000 - 950) = 1.012346
TCPI management EAC = 4,100 / 4,200 = 0.976190
```

The arithmetic indicates unfavorable cumulative cost and schedule efficiency and separates two forecast assumptions. It does not establish root cause, calendar slip, corrective action, or an approved forecast.

## Calculator operations

| Operation | Purpose |
|---|---|
| `program_evm_snapshot` | cumulative performance, status percentages, management EAC/VAC |
| `program_evm_forecast` | CPI/composite/recent-CPI EACs, VACs, and TCPI |
| `program_evm_period_reconciliation` | period-to-cumulative control totals |
| `program_evm_schedule_execution` | BEI and hit/miss percentage |
| `program_evm_labor_variance` | rate/volume labor-cost decomposition |
| `program_evm_material_variance` | price/usage material-cost decomposition |

Use the [EVM calculation record](../../templates/evm-calculation-record.md). Preserve the returned receipt without changing its numbers.

## Output

Status/baseline/scope identity, source evidence, reconciliation, raw PV/EV/AC/BAC/ETC, formula version, calculated metrics, undefined values, forecast assumptions, thresholds, IMS implications, variance drivers, corrective actions, owner, and human-approved conclusion.

Primary public orientation: [DOE EVMS Gold Card](https://www.energy.gov/projectmanagement/articles/earned-value-management-system-evms-gold-card), [NASA EVM reference card](https://www.nasa.gov/wp-content/uploads/2018/06/nasa-evm-reference-card.pdf), and [DoD EVM definitions](https://www.acq.osd.mil/asda/dpc/api/ipm/evm-definitions.html). Applicable contracts, approved system descriptions, current controlled procedures, and EIA-748 requirements govern actual program use.

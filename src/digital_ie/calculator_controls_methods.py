"""Calculation MCP contracts for schedule, reliability, and economics."""

from __future__ import annotations

from . import engineering_economics, reliability, schedule_risk
from .calculator_pack_helpers import array, integer, method, number, object_schema, string


ASSUMPTIONS = (
    "common scope, configuration, status date, units, and time basis",
    "source-data completeness and estimate/model fitness",
    "independence, correlation, stationarity, and distribution assumptions not mechanically tested",
    "constraints, risks, failure definitions, and lifecycle effects not represented in inputs",
    "organizational ability and authority to execute the indicated alternative",
)
AUTHORITY = (
    "Calculation only; no schedule baseline, official forecast, reliability qualification, "
    "investment, make-buy, product acceptance, or program decision is approved."
)
N = number()
NN = number(0)
P = number(0, 1)
I = integer()
I0 = integer(0)
I1 = integer(1)
NA = array(N)
NNA = array(NN)
SA = array(string(), 0)
CPM_ACTIVITY = object_schema(
    {"id": string(), "duration": NN, "predecessors": SA}, ("id", "duration")
)
SIM_ACTIVITY = object_schema(
    {
        "id": string(), "optimistic": NN, "most_likely": NN,
        "pessimistic": NN, "predecessors": SA,
    },
    ("id", "optimistic", "most_likely", "pessimistic"),
)
COST_ELEMENT = object_schema(
    {
        "id": string(), "minimum": NN, "most_likely": NN, "maximum": NN,
        "risk_probability": P, "risk_impact": NN,
    },
    ("id", "minimum", "most_likely", "maximum"),
)


METHODS = (
    method("program.critical_path", "Critical-path calculation", "Run CPM forward/backward passes for finish-to-start, zero-lag logic.",
           ("ES=max(EF_predecessors)", "EF=ES+duration", "TF=LS-ES", "FF=min(ES_successors)-EF"),
           {"activities": array(CPM_ACTIVITY)}, ("activities",), schedule_risk.critical_path,
           ("activities",), ASSUMPTIONS, AUTHORITY),
    method("program.pert", "PERT three-point estimate", "Calculate classic PERT expected duration and variance.",
           ("mean=(optimistic+4*most_likely+pessimistic)/6", "sigma=(pessimistic-optimistic)/6"),
           {"optimistic": NN, "most_likely": NN, "pessimistic": NN},
           ("optimistic", "most_likely", "pessimistic"), schedule_risk.pert_estimate,
           ("optimistic", "most_likely", "pessimistic"), ASSUMPTIONS, AUTHORITY),
    method("program.schedule_simulation", "Seeded schedule simulation", "Sample triangular durations and rerun the bounded CPM network.",
           ("duration_i~Triangular(o_i,m_i,p_i)", "project_duration=CPM(sampled_durations)"),
           {"activities": array(SIM_ACTIVITY), "iterations": integer(1, 100000), "seed": I},
           ("activities", "iterations", "seed"), schedule_risk.simulate_schedule,
           ("activities", "iterations", "seed"), ASSUMPTIONS, AUTHORITY),
    method("program.cost_simulation", "Seeded cost simulation", "Sample triangular base costs and optional independent discrete risks.",
           ("base_i~Triangular(min_i,mode_i,max_i)", "risk_i=impact_i*Bernoulli(probability_i)"),
           {"cost_elements": array(COST_ELEMENT), "iterations": integer(1, 100000), "seed": I},
           ("cost_elements", "iterations", "seed"), schedule_risk.simulate_cost,
           ("cost_elements", "iterations", "seed"), ASSUMPTIONS, AUTHORITY),
    method("reliability.observed", "Observed reliability metrics", "Calculate observed repairable-item MTBF, MTTR, failure rate, and availability.",
           ("MTBF=operating_time/failures", "MTTR=repair_time/failures", "A=operating_time/(operating_time+repair_time)"),
           {"operating_time": NN, "failures": I0, "repair_time": NN},
           ("operating_time", "failures"), reliability.observed_metrics,
           ("operating_time", "failures", "repair_time"), ASSUMPTIONS, AUTHORITY),
    method("reliability.observed_mttf", "Observed MTTF", "Calculate time-on-test per observed nonrepairable failure.",
           ("MTTF=total_time_on_test/failures",), {"total_time_on_test": NN, "failures": I0},
           ("total_time_on_test", "failures"), reliability.observed_mttf,
           ("total_time_on_test", "failures"), ASSUMPTIONS, AUTHORITY, "mttf"),
    method("reliability.operational_availability", "Operational availability", "Calculate uptime divided by uptime plus included downtime.",
           ("Ao=uptime/(uptime+total_downtime)",), {"uptime": NN, "total_downtime": NN},
           ("uptime", "total_downtime"), reliability.operational_availability,
           ("uptime", "total_downtime"), ASSUMPTIONS, AUTHORITY, "operational_availability"),
    method("reliability.inherent_availability", "Inherent availability", "Calculate availability from MTBF and corrective MTTR.",
           ("Ai=MTBF/(MTBF+MTTR)",), {"mtbf": NN, "mttr": NN}, ("mtbf", "mttr"),
           reliability.inherent_availability, ("mtbf", "mttr"), ASSUMPTIONS, AUTHORITY, "inherent_availability"),
    method("reliability.exponential", "Exponential reliability model", "Evaluate a constant-hazard exponential life model.",
           ("R(t)=exp(-lambda*t)", "F(t)=1-R(t)", "MTTF=1/lambda"),
           {"time": NN, "failure_rate": NN, "mttf": NN}, ("time",), reliability.exponential_model,
           ("time", "failure_rate", "mttf"), ASSUMPTIONS, AUTHORITY),
    method("reliability.weibull", "Weibull reliability model", "Evaluate a two-parameter zero-location Weibull model.",
           ("R(t)=exp(-(t/eta)^beta)", "h(t)=(beta/eta)*(t/eta)^(beta-1)"),
           {"time": NN, "scale": NN, "shape": NN}, ("time", "scale", "shape"),
           reliability.weibull_model, ("time", "scale", "shape"), ASSUMPTIONS, AUTHORITY),
    method("reliability.series", "Series-system reliability", "Calculate independent series-system reliability.",
           ("R_system=product(R_i)",), {"component_reliabilities": array(P)},
           ("component_reliabilities",), reliability.series_reliability,
           ("component_reliabilities",), ASSUMPTIONS, AUTHORITY, "system_reliability"),
    method("reliability.parallel", "Parallel-system reliability", "Calculate independent active-parallel reliability.",
           ("R_system=1-product(1-R_i)",), {"component_reliabilities": array(P)},
           ("component_reliabilities",), reliability.parallel_reliability,
           ("component_reliabilities",), ASSUMPTIONS, AUTHORITY, "system_reliability"),
    method("reliability.k_out_of_n", "K-out-of-n reliability", "Calculate heterogeneous independent k-out-of-n reliability by convolution.",
           ("R=P(number_successful>=k)",), {"component_reliabilities": array(P), "required": I1},
           ("component_reliabilities", "required"), reliability.k_out_of_n_reliability,
           ("component_reliabilities", "required"), ASSUMPTIONS, AUTHORITY, "system_reliability"),
    method("reliability.zero_failure_binomial", "Zero-failure binomial demonstration", "Calculate fixed-mission units for a declared reliability/confidence target.",
           ("n=ceil(ln(1-confidence)/ln(reliability_requirement))",),
           {"reliability_requirement": P, "confidence": P}, ("reliability_requirement", "confidence"),
           reliability.zero_failure_binomial_sample_size,
           ("reliability_requirement", "confidence"), ASSUMPTIONS, AUTHORITY, "required_units"),
    method("reliability.zero_failure_exponential", "Zero-failure exponential demonstration", "Calculate accumulated test time for MTBF/confidence under constant hazard.",
           ("test_time=-MTBF_requirement*ln(1-confidence)",),
           {"mtbf_requirement": NN, "confidence": P}, ("mtbf_requirement", "confidence"),
           reliability.zero_failure_exponential_test_time,
           ("mtbf_requirement", "confidence"), ASSUMPTIONS, AUTHORITY, "required_test_time"),
    method("economics.future_value", "Future value", "Compound one present amount through equal periods.",
           ("FV=PV*(1+rate)^periods",), {"present_value": N, "rate": N, "periods": I0},
           ("present_value", "rate", "periods"), engineering_economics.future_value,
           ("present_value", "rate", "periods"), ASSUMPTIONS, AUTHORITY, "future_value"),
    method("economics.present_value", "Present value", "Discount one future amount to period zero.",
           ("PV=FV/(1+rate)^periods",), {"future_value_amount": N, "rate": N, "periods": I0},
           ("future_value_amount", "rate", "periods"), engineering_economics.present_value,
           ("future_value_amount", "rate", "periods"), ASSUMPTIONS, AUTHORITY, "present_value"),
    method("economics.npv", "Net present value", "Discount equally spaced cash flows with the first at period zero.",
           ("NPV=sum(CF_t/(1+rate)^t)",), {"cash_flows": NA, "rate": N},
           ("cash_flows", "rate"), engineering_economics.net_present_value,
           ("cash_flows", "rate"), ASSUMPTIONS, AUTHORITY, "net_present_value"),
    method("economics.equivalent_annual_value", "Equivalent annual value", "Convert a present amount to a uniform end-period series.",
           ("EAV=NPV*rate*(1+rate)^n/((1+rate)^n-1)",),
           {"net_present_amount": N, "rate": N, "periods": I1},
           ("net_present_amount", "rate", "periods"), engineering_economics.equivalent_annual_value,
           ("net_present_amount", "rate", "periods"), ASSUMPTIONS, AUTHORITY, "equivalent_annual_value"),
    method("economics.payback", "Payback period", "Calculate simple or discounted payback with within-period interpolation.",
           ("cumulative_t=sum(discounted_CF_0..t)",), {"cash_flows": array(N, 2), "rate": N},
           ("cash_flows",), engineering_economics.payback_period,
           ("cash_flows", "rate"), ASSUMPTIONS, AUTHORITY, "payback_period"),
    method("economics.irr", "Bracketed internal rate of return", "Find one explicitly bracketed periodic IRR by bounded bisection.",
           ("find rate where NPV(rate)=0 by bisection",),
           {"cash_flows": array(N, 2), "lower_rate": N, "upper_rate": N, "tolerance": NN, "max_iterations": integer(1, 10000)},
           ("cash_flows",), engineering_economics.internal_rate_of_return,
           ("cash_flows", "lower_rate", "upper_rate", "tolerance", "max_iterations"), ASSUMPTIONS, AUTHORITY, "internal_rate_of_return"),
    method("economics.break_even", "Break-even units", "Calculate units where revenue equals fixed plus variable cost.",
           ("Q_break_even=fixed_cost/(unit_price-unit_variable_cost)",),
           {"fixed_cost": NN, "unit_price": N, "unit_variable_cost": N},
           ("fixed_cost", "unit_price", "unit_variable_cost"), engineering_economics.break_even_units,
           ("fixed_cost", "unit_price", "unit_variable_cost"), ASSUMPTIONS, AUTHORITY, "break_even_units"),
    method("economics.make_buy", "Make-buy relevant-cost comparison", "Compare declared relevant make and buy costs at one volume.",
           ("make=fixed_make+quantity*unit_make", "buy=quantity*unit_buy"),
           {"quantity": NN, "make_fixed_cost": NN, "make_unit_cost": NN, "buy_unit_cost": NN},
           ("quantity", "make_fixed_cost", "make_unit_cost", "buy_unit_cost"), engineering_economics.make_buy_analysis,
           ("quantity", "make_fixed_cost", "make_unit_cost", "buy_unit_cost"), ASSUMPTIONS, AUTHORITY),
    method("economics.life_cycle_cost", "Discounted life-cycle cost", "Present-value a positive-outlay lifecycle cost stream.",
           ("LCC=sum(cost_t/(1+rate)^t)",), {"costs_by_period": NNA, "rate": N},
           ("costs_by_period", "rate"), engineering_economics.life_cycle_cost,
           ("costs_by_period", "rate"), ASSUMPTIONS, AUTHORITY, "life_cycle_cost"),
    method("economics.npv_sensitivity", "NPV rate sensitivity", "Calculate NPV across explicitly supplied discount rates.",
           ("NPV_r=sum(CF_t/(1+r)^t)",), {"cash_flows": NA, "rates": NA},
           ("cash_flows", "rates"), engineering_economics.npv_rate_sensitivity,
           ("cash_flows", "rates"), ASSUMPTIONS, AUTHORITY),
)

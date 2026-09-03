"""Calculation MCP contracts for production, supply, and operations research."""

from __future__ import annotations

from . import operations_research, production, supply
from .calculator_pack_helpers import array, integer, method, number, string


ASSUMPTIONS = (
    "common scope, units, time basis, configuration, and product mix",
    "source-data completeness and representative operating conditions",
    "stability, independence, and distribution assumptions of the selected model",
    "physical, policy, qualification, safety, and precedence constraints not encoded",
    "execution feasibility and downstream system effects",
)
AUTHORITY = (
    "Calculation only; no work release, staffing action, inventory policy, supplier commitment, "
    "facility decision, schedule priority, capital approval, or operational instruction is made."
)
N = number()
NN = number(0)
P = number(0, 1)
I = integer()
I0 = integer(0)
I1 = integer(1)
NA = array(N)
NNA = array(NN)
SA = array(string())
MATRIX = array(array(N))
NN_MATRIX = array(array(NN))


METHODS = (
    method("production.pace", "Production pace and resource need", "Calculate takt, resource requirement, and installed pace margin.",
           ("takt=available_time/demand", "resources=ceil(effective_cycle_time/takt)"),
           {"available_time": NN, "demand": NN, "effective_cycle_time": NN, "installed_parallel_resources": I1},
           ("available_time", "demand", "effective_cycle_time"), production.production_pace,
           ("available_time", "demand", "effective_cycle_time", "installed_parallel_resources"), ASSUMPTIONS, AUTHORITY),
    method("production.line_balance", "Line-balance metrics", "Calculate station loads, cycle time, balance efficiency, idle time, and output capacity.",
           ("cycle_time=max(station_loads)", "balance_efficiency=sum(task_time)/(stations*cycle_time)"),
           {"station_task_times": NN_MATRIX, "available_time": NN},
           ("station_task_times", "available_time"), production.line_balance,
           ("station_task_times", "available_time"), ASSUMPTIONS, AUTHORITY),
    method("production.oee", "Overall equipment effectiveness", "Calculate availability, performance, quality, OEE, and fully productive time.",
           ("A=run/planned", "P=ideal_cycle*total/run", "Q=good/total", "OEE=A*P*Q"),
           {"planned_production_time": NN, "run_time": NN, "ideal_cycle_time": NN, "total_count": NN, "good_count": NN},
           ("planned_production_time", "run_time", "ideal_cycle_time", "total_count", "good_count"),
           production.overall_equipment_effectiveness,
           ("planned_production_time", "run_time", "ideal_cycle_time", "total_count", "good_count"), ASSUMPTIONS, AUTHORITY),
    method("production.flow", "Flow and process-cycle efficiency", "Solve one Little's Law term from the other two and optionally calculate PCE.",
           ("WIP=throughput*lead_time", "PCE=value_added_time/lead_time"),
           {"wip": NN, "throughput": NN, "lead_time": NN, "value_added_time": NN}, (),
           production.flow_metrics, ("wip", "throughput", "lead_time", "value_added_time"), ASSUMPTIONS, AUTHORITY),
    method("production.rolled_yield", "Rolled throughput yield", "Calculate independent-step rolled first-pass yield.",
           ("RTY=product(FPY_i)",), {"step_yields": array(P)}, ("step_yields",),
           production.rolled_throughput_yield, ("step_yields",), ASSUMPTIONS, AUTHORITY),
    method("production.queue_mm1", "M/M/1 queue", "Calculate steady-state single-server queue measures.",
           ("rho=lambda/mu", "Lq=rho^2/(1-rho)", "Wq=Lq/lambda"),
           {"arrival_rate": NN, "service_rate": NN}, ("arrival_rate", "service_rate"),
           production.mm1_queue, ("arrival_rate", "service_rate"), ASSUMPTIONS, AUTHORITY),
    method("production.queue_mmc", "M/M/c queue", "Calculate steady-state identical-server Erlang-C measures.",
           ("rho=lambda/(c*mu)", "P_wait=Erlang_C(lambda/mu,c)", "Lq=P_wait*rho/(1-rho)"),
           {"arrival_rate": NN, "service_rate_per_server": NN, "servers": I1},
           ("arrival_rate", "service_rate_per_server", "servers"), production.mmc_queue,
           ("arrival_rate", "service_rate_per_server", "servers"), ASSUMPTIONS, AUTHORITY),
    method("production.learning_curve", "Unit learning curve", "Calculate Crawford unit-model values and cumulative total.",
           ("b=ln(learning_rate)/ln(2)", "Y_x=Y_1*x^b"),
           {"first_unit_value": NN, "learning_rate": P, "units": I1},
           ("first_unit_value", "learning_rate", "units"), production.unit_learning_curve,
           ("first_unit_value", "learning_rate", "units"), ASSUMPTIONS, AUTHORITY),
    method("supply.moving_average", "Moving-average forecast", "Calculate aligned trailing fits and the next forecast.",
           ("F_(t+1)=sum(last w observations)/w",), {"values": NA, "window": I1},
           ("values", "window"), supply.moving_average, ("values", "window"), ASSUMPTIONS, AUTHORITY),
    method("supply.exponential_smoothing", "Simple exponential smoothing", "Calculate aligned one-step forecasts and the next forecast.",
           ("F_(t+1)=alpha*A_t+(1-alpha)*F_t",),
           {"values": NA, "alpha": P, "initial_forecast": N}, ("values", "alpha"),
           supply.simple_exponential_smoothing, ("values", "alpha", "initial_forecast"), ASSUMPTIONS, AUTHORITY),
    method("supply.forecast_accuracy", "Forecast accuracy", "Calculate actual-minus-forecast errors, ME, MAD, MSE, RMSE, MAPE, and tracking signal.",
           ("e_t=A_t-F_t", "MAD=mean(|e|)", "RMSE=sqrt(mean(e^2))", "tracking_signal=sum(e)/MAD"),
           {"actuals": NA, "forecasts": NA}, ("actuals", "forecasts"), supply.forecast_accuracy,
           ("actuals", "forecasts"), ASSUMPTIONS, AUTHORITY),
    method("supply.eoq", "Economic order quantity", "Calculate classical EOQ and relevant annual cycle costs.",
           ("EOQ=sqrt(2*annual_demand*order_cost/annual_holding_cost_per_unit)",),
           {"annual_demand": NN, "order_cost": NN, "annual_holding_cost_per_unit": NN},
           ("annual_demand", "order_cost", "annual_holding_cost_per_unit"), supply.economic_order_quantity,
           ("annual_demand", "order_cost", "annual_holding_cost_per_unit"), ASSUMPTIONS, AUTHORITY),
    method("supply.reorder_point", "Reorder point", "Calculate expected lead-time demand, safety stock, and reorder point.",
           ("ROP=mean_demand*lead_time+z*sigma_demand*sqrt(lead_time)",),
           {"mean_demand_per_period": NN, "lead_time_periods": NN, "demand_standard_deviation_per_period": NN, "service_z": NN},
           ("mean_demand_per_period", "lead_time_periods"), supply.reorder_point,
           ("mean_demand_per_period", "lead_time_periods", "demand_standard_deviation_per_period", "service_z"), ASSUMPTIONS, AUTHORITY),
    method("supply.mrp_netting", "Time-phased MRP netting", "Calculate projected available, net requirements, and planned receipts/releases for one item.",
           ("projected_available=prior+scheduled+planned_receipt-gross", "net=max(0,safety_stock-before_plan)"),
           {"gross_requirements": NNA, "scheduled_receipts": NNA, "initial_available": NN, "lead_time_periods": I0, "safety_stock": NN, "fixed_order_quantity": NN},
           ("gross_requirements", "scheduled_receipts", "initial_available", "lead_time_periods"), supply.mrp_netting,
           ("gross_requirements", "scheduled_receipts", "initial_available", "lead_time_periods", "safety_stock", "fixed_order_quantity"), ASSUMPTIONS, AUTHORITY),
    method("operations.facility_center", "Facility center of gravity", "Calculate a weighted planar center for screening alternatives.",
           ("x=sum(w_i*x_i)/sum(w_i)", "y=sum(w_i*y_i)/sum(w_i)"),
           {"coordinates": MATRIX, "weights": NNA}, ("coordinates", "weights"),
           operations_research.facility_center_of_gravity, ("coordinates", "weights"), ASSUMPTIONS, AUTHORITY),
    method("operations.weighted_scores", "Weighted decision scores", "Normalize weights and rank alternatives on an already common scale.",
           ("score_j=sum(normalized_weight_i*rating_ji)",),
           {"alternative_names": SA, "scores": NN_MATRIX, "weights": NNA},
           ("alternative_names", "scores", "weights"), operations_research.weighted_decision_scores,
           ("alternative_names", "scores", "weights"), ASSUMPTIONS, AUTHORITY),
    method("operations.bounded_assignment", "Bounded assignment", "Find the minimum-cost rectangular assignment by complete enumeration up to eight rows.",
           ("minimize sum(cost[row,assigned_column])",), {"cost_matrix": MATRIX},
           ("cost_matrix",), operations_research.bounded_assignment, ("cost_matrix",), ASSUMPTIONS, AUTHORITY),
    method("operations.single_machine_sequence", "Single-machine sequence", "Evaluate FCFS, shortest-processing-time, or earliest-due-date dispatching.",
           ("completion_j=sum(processing_time through j)", "tardiness_j=max(0,completion_j-due_j)"),
           {"job_names": SA, "processing_times": NNA, "due_dates": NA, "rule": string()},
           ("job_names", "processing_times", "due_dates", "rule"), operations_research.single_machine_sequence,
           ("job_names", "processing_times", "due_dates", "rule"), ASSUMPTIONS, AUTHORITY),
)

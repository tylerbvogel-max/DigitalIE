"""Calculation MCP contracts for quantitative quality engineering."""

from __future__ import annotations

from . import quality
from .calculator_pack_helpers import array, integer, method, number, string


ASSUMPTIONS = (
    "measurement-system suitability and data integrity",
    "representative sampling and stable scope/configuration",
    "rational subgrouping, independence, and distribution assumptions",
    "applicability of supplied chart constants, specifications, and sampling plan",
    "practical significance, causal mechanism, and sustained process control",
)
AUTHORITY = (
    "Calculation only; no process-control declaration, product acceptance, sampling-plan "
    "approval, specification change, causal conclusion, or quality disposition is made."
)
N = number()
NN = number(0)
P = number(0, 1)
I0 = integer(0)
I1 = integer(1)
NA = array(N)
NNA = array(NN)
IA = array(I0)
MATRIX = array(array(N, 2), 2)
CUBE = array(array(array(N, 2), 2), 2)


METHODS = (
    method("quality.imr_chart", "Individuals and moving-range chart", "Calculate I-MR center lines, limits, ranges, and within-sigma estimate.",
           ("MR_i=|x_i-x_(i-1)|", "sigma_hat=MR_bar/d2", "I limits=x_bar+/-3*sigma_hat"),
           {"values": array(N, 2), "d2": NN, "mr_lower_factor": NN, "mr_upper_factor": NN},
           ("values",), quality.individuals_moving_range,
           ("values", "d2", "mr_lower_factor", "mr_upper_factor"), ASSUMPTIONS, AUTHORITY),
    method("quality.xbar_r_chart", "X-bar and R chart", "Calculate balanced-subgroup X-bar/R limits using declared constants.",
           ("Xbar limits=Xdoublebar+/-A2*Rbar", "R limits=D3*Rbar,D4*Rbar"),
           {"subgroups": MATRIX, "a2": NN, "d3": NN, "d4": NN, "d2": NN},
           ("subgroups", "a2", "d3", "d4"), quality.xbar_r_chart,
           ("subgroups", "a2", "d3", "d4", "d2"), ASSUMPTIONS, AUTHORITY),
    method("quality.xbar_s_chart", "X-bar and S chart", "Calculate balanced-subgroup X-bar/S limits using declared constants.",
           ("Xbar limits=Xdoublebar+/-A3*Sbar", "S limits=B3*Sbar,B4*Sbar"),
           {"subgroups": MATRIX, "a3": NN, "b3": NN, "b4": NN},
           ("subgroups", "a3", "b3", "b4"), quality.xbar_s_chart,
           ("subgroups", "a3", "b3", "b4"), ASSUMPTIONS, AUTHORITY),
    method("quality.p_chart", "p chart", "Calculate varying-sample fraction-nonconforming limits.",
           ("pbar=sum(d)/sum(n)", "limits=pbar+/-z*sqrt(pbar*(1-pbar)/n_i)"),
           {"nonconforming": IA, "sample_sizes": array(I1), "sigma_width": NN},
           ("nonconforming", "sample_sizes"), quality.p_chart,
           ("nonconforming", "sample_sizes", "sigma_width"), ASSUMPTIONS, AUTHORITY),
    method("quality.np_chart", "np chart", "Calculate constant-sample nonconforming-count limits.",
           ("npbar=n*pbar", "limits=npbar+/-z*sqrt(n*pbar*(1-pbar))"),
           {"nonconforming": IA, "sample_size": I1, "sigma_width": NN},
           ("nonconforming", "sample_size"), quality.np_chart,
           ("nonconforming", "sample_size", "sigma_width"), ASSUMPTIONS, AUTHORITY),
    method("quality.c_chart", "c chart", "Calculate equal-opportunity nonconformity-count limits.",
           ("cbar=mean(c_i)", "limits=cbar+/-z*sqrt(cbar)"),
           {"nonconformities": IA, "sigma_width": NN}, ("nonconformities",), quality.c_chart,
           ("nonconformities", "sigma_width"), ASSUMPTIONS, AUTHORITY),
    method("quality.u_chart", "u chart", "Calculate varying-exposure nonconformities-per-unit limits.",
           ("ubar=sum(c)/sum(n)", "limits=ubar+/-z*sqrt(ubar/n_i)"),
           {"nonconformities": IA, "inspection_units": NNA, "sigma_width": NN},
           ("nonconformities", "inspection_units"), quality.u_chart,
           ("nonconformities", "inspection_units", "sigma_width"), ASSUMPTIONS, AUTHORITY),
    method("quality.capability", "Process capability indices", "Calculate two-sided Cp/Cpk and Pp/Ppk from declared estimates.",
           ("Cp=(USL-LSL)/(6*sigma_within)", "Cpk=min((USL-mean),(mean-LSL))/(3*sigma_within)", "Pp/Ppk use sigma_overall"),
           {"mean_value": N, "within_sigma": NN, "overall_sigma": NN, "lsl": N, "usl": N},
           ("mean_value", "within_sigma", "overall_sigma", "lsl", "usl"), quality.capability_indices,
           ("mean_value", "within_sigma", "overall_sigma", "lsl", "usl"), ASSUMPTIONS, AUTHORITY),
    method("quality.yield", "Yield and defect metrics", "Calculate unit yield, DPU, DPO, DPMO, and rolled throughput yield.",
           ("DPU=defects/units", "DPO=defects/(units*opportunities)", "DPMO=1e6*DPO", "RTY=product(FPY_i)"),
           {"units": I1, "defects": I0, "opportunities_per_unit": I1, "step_yields": array(P), "conforming_units": I0},
           ("units", "defects", "opportunities_per_unit", "step_yields"), quality.yield_metrics,
           ("units", "defects", "opportunities_per_unit", "step_yields", "conforming_units"), ASSUMPTIONS, AUTHORITY),
    method("quality.gage_rr_crossed", "Crossed ANOVA Gage R&R", "Estimate balanced crossed part/operator/repeat variance components.",
           ("repeatability=MS_error", "operator=(MS_operator-MS_interaction)/(parts*repeats)", "interaction=(MS_interaction-MS_error)/repeats"),
           {"measurements": CUBE}, ("measurements",), quality.crossed_gage_rr_anova,
           ("measurements",), ASSUMPTIONS, AUTHORITY),
    method("quality.tolerance_stack", "Symmetric tolerance stack", "Calculate worst-case and root-sum-square tolerance magnitudes.",
           ("T_worst=sum(T_i)", "T_RSS=sqrt(sum(T_i^2))"),
           {"component_tolerances": NNA}, ("component_tolerances",), quality.tolerance_stack,
           ("component_tolerances",), ASSUMPTIONS, AUTHORITY),
    method("quality.sampling_oc", "Single-sampling OC point", "Calculate binomial acceptance/rejection probability for one declared plan and defect fraction.",
           ("P_accept=sum_(d=0)^c C(n,d)*p^d*(1-p)^(n-d)",),
           {"sample_size": I1, "acceptance_number": I0, "fraction_nonconforming": P},
           ("sample_size", "acceptance_number", "fraction_nonconforming"), quality.single_sampling_oc,
           ("sample_size", "acceptance_number", "fraction_nonconforming"), ASSUMPTIONS, AUTHORITY),
    method("quality.factorial_2k_effects", "Two-level full-factorial effects", "Calculate effects for a complete unreplicated coded 2^k design.",
           ("effect_S=sum(y_i*product(x_ij,j in S))/2^(k-1)",),
           {"design": array(array(integer(-1, 1))), "responses": NA, "factor_names": array(string())},
           ("design", "responses", "factor_names"), quality.two_level_full_factorial_effects,
           ("design", "responses", "factor_names"), ASSUMPTIONS, AUTHORITY),
)

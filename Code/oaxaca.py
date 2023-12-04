import pandas as pd
import numpy as np
import statsmodels.api as sm

def adjust_dummies(beta, dummies):
    # Assuming the first coefficient is on the intercept.

    out = beta.copy()

    c = np.sum(beta[dummies]) / (len(dummies) + 1)
    out[dummies] = beta[dummies] - c
    out[0] = beta[0] + c

    return out

def run_oaxaca_coef(data, formula_reg, formula_reg_collapse, formula_dummy, group_var, reg_fun, R, *args):
    out = {}
    n = len(data)
    d = data
    
    data_pooled = d[(d[group_var] == 0) | (d[group_var] == 1)]
    data_A = data_pooled[d[group_var] == 0]
    data_B = data_pooled[d[group_var] == 1]
    
    reg_object_A = reg_fun(formula=formula_reg, data=data_A, *args)
    reg_object_B = reg_fun(formula=formula_reg, data=data_B, *args)
    reg_object_pooled = reg_fun(formula=formula_reg, data=data_pooled, *args)
    reg_object_pooled_collapse = reg_fun(formula=formula_reg_collapse, data=data_pooled, *args)
    
    model_matrix_A = reg_object_A.model.formula.model.exog
    model_matrix_B = reg_object_B.model.formula.model.exog
    
    # difference in Y means
    used_y_A = reg_object_A.predict(data_A)
    used_y_B = reg_object_B.predict(data_B)
    used_y_pooled = reg_object_pooled.predict(data_pooled)

    y_mean_A = used_y_A.mean()
    y_mean_B = used_y_B.mean()
    y_diff = y_mean_A - y_mean_B
    
    # number of observations used
    n_A = len(used_y_A); n_B = len(used_y_B); n_pooled = len(used_y_pooled)
    proportion_A = n_A / n_pooled  # proportion of observations that have group.var = 0
    proportion_B = n_B / n_pooled  # proportion of observations that have group.var = 1

    # difference in coefficients
    beta_A = reg_object_A.params
    beta_B = reg_object_B.params
    beta_pooled = reg_object_pooled.params
    beta_pooled_collapse = reg_object_pooled_collapse.params
    
    # adjust coefficients for reference categories
    if formula_dummy is not None:
        for i in range(len(formula_dummy)):

            reg_object_dummy = sm.OLS(formula=formula_dummy[i], data=data_pooled).fit()
            included_dummy_names = list(reg_object_dummy.params[1:])

            beta_A_adj = adjust_dummies(beta_A, included_dummy_names)
            beta_B_adj = adjust_dummies(beta_B, included_dummy_names)
            beta_pooled_adj = adjust_dummies(beta_pooled, included_dummy_names)
            beta_pooled_collapse_adj = adjust_dummies(beta_pooled_collapse, included_dummy_names)

    # difference in mean endowments
    x_mean_A = pd.DataFrame(model_matrix_A).mean().values
    x_mean_B = pd.DataFrame(model_matrix_B).mean().values

    ###  three-fold decompositon
    out_vars = {}

    # overall
    E = np.dot(x_mean_A - x_mean_B, beta_B)              # endowment
    C = np.dot(x_mean_B, beta_A - beta_B)              # coefficients
    I = np.dot(x_mean_A - x_mean_B, beta_A - beta_B)   # interaction
    
    if formula_dummy is None:
        E_vars = (x_mean_A - x_mean_B) * beta_B
        C_vars = x_mean_B * (beta_A - beta_B)
        I_vars = (x_mean_A - x_mean_B) * (beta_A - beta_B)
    else:
        E_vars = (x_mean_A - x_mean_B) * beta_B_adj
        C_vars = x_mean_B * (beta_A_adj - beta_B_adj)
        I_vars = (x_mean_A - x_mean_B) * (beta_A_adj - beta_B_adj)
    
    out_threefold_overall = np.array([E, C, I])
    out_threefold_vars = np.column_stack((E_vars, C_vars, I_vars))

    if formula_dummy is not None:
        E_base = E - np.sum(E_vars, axis=0)
        C_base = C - np.sum(C_vars, axis=0)
        I_base = I - np.sum(I_vars, axis=0)
        base_line_threefold = np.array([E_base, C_base, I_base])
        out_threefold_vars = np.vstack((out_threefold_vars, base_line_threefold))
        out_threefold_vars[-1, :] = "(Base)"
    
    out_threefold_overall = dict(zip(["coef(endowments)", "coef(coefficients)", "coef(interaction)"], out_threefold_overall))
    out_threefold_vars = dict(zip(["coef(endowments)", "coef(coefficients)", "coef(interaction)"], out_threefold_vars))
    
   
    out_threefold = {"overall": out_threefold_overall, "variables": out_threefold_vars}

    out_n = {"n.A": n_A, "n.B": n_B, "n.pooled": n_pooled}
    
    out_y = {"y.A": y_mean_A, "y.B": y_mean_B, "y.diff": y_diff}
    
    out_x = {"x.mean.A": x_mean_A, "x.mean.B": x_mean_B, "x.mean.diff": x_mean_A - x_mean_B}
    
    out_beta = {"beta.A": beta_A_adj if formula_dummy is not None else beta_A, "beta.B": beta_B_adj if formula_dummy is not None else beta_B, "beta.diff": beta_A_adj - beta_B_adj if formula_dummy is not None else beta_A - beta_B, "beta.R": out_beta_star}
    
    out_reg = {"reg.A": reg_object_A, "reg.B": reg_object_B, "reg.pooled.1": reg_object_pooled, "reg.pooled.2": reg_object_pooled_collapse}
    out_reg["reg.A"].call = out_reg["reg.B"].call = out_reg["reg.pooled.1"].call = out_reg["reg.pooled.2"].call = None
    
    out = {"beta": out_beta, "n": out_n, "R": R, "reg": out_reg, "threefold": out_threefold, 
           "x": out_x, "y": out_y}
    
    return out


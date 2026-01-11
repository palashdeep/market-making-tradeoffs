import pandas as pd
import matplotlib.pyplot as plt

from optimizer import run_parameter_sweep, pareto_front, significant_params

def main():

    param_grid = [
        (k, alpha, hth, hsz)
        for k in [0.5, 1.0, 1.5]
        for alpha in [0.0, 0.01, 0.05]
        for hth in [20, 50, 100]
        for hsz in [10, 20, 50]
    ]

    seeds = range(1,51)
    oos_seeds = range(1001,1051)

    df = run_parameter_sweep(param_grid, seeds)
    df.to_csv("results.csv")

    significant = significant_params(df, threshold=2.0)
    print(f"Significant parameter sets (t >= 2.0): {len(significant)} / {len(df)}")

    oos_df = run_parameter_sweep(significant["params"].tolist(), oos_seeds)
    oos_df.to_csv("oos_result.csv")

    pareto_df = pareto_front(oos_df)

    fname = "figures/pareto_oos.png"

    plt.scatter(oos_df["mean_inv_vol"], 
                oos_df["mean_controlled_pnl"], 
                alpha=0.3, 
                label="OOS params"
    )
    
    plt.plot(pareto_df["mean_inv_vol"], 
                pareto_df["mean_controlled_pnl"], 
                color='red',
                linewidth=2,
                label="Pareto front (OOS)"
    )

    plt.xlabel("Inventory Risk")
    plt.ylabel("Mean Controlled PnL")
    plt.legend()
    plt.title("OOS Tradeoff: Controlled PnL vs Inventory Risk")
    if fname:
        plt.savefig(fname, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()

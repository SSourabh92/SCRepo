#!/usr/bin/env python3
"""Plot bin_def against StddevMultiple from a CDF CSV.

Pad-median rows are left out, the same filter the other scan plots use.
Dies are drawn in separate colors, each parameter gets its own panel when
a file has more than one, and hovering a point shows that row.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

REQUIRED_COLUMNS = ("bin_def", "StddevMultiple")
SIGMA_GUIDES = (
    (-5.0, "−5σ opens", "#c23b3b"),
    (5.0, "+5σ shorts", "#2c6bed"),
)


def load_cdf(path: str) -> tuple[pd.DataFrame, dict]:
    """Read a CDF CSV and keep rows that can be plotted."""
    raw = pd.read_csv(path, delimiter=",", header=0)
    missing = [name for name in REQUIRED_COLUMNS if name not in raw.columns]
    if missing:
        raise ValueError("CDF file is missing column(s): " + ", ".join(missing))

    frame = raw.copy()
    frame["bin_def"] = pd.to_numeric(frame["bin_def"], errors="coerce")
    frame["StddevMultiple"] = pd.to_numeric(frame["StddevMultiple"], errors="coerce")
    usable = frame["bin_def"].notna() & frame["StddevMultiple"].notna()
    dropped_blank = int((~usable).sum())
    frame = frame.loc[usable]

    dropped_pad = 0
    if "parameter" in frame.columns:
        pad = frame["parameter"].astype(str) == "padMedian"
        dropped_pad = int(pad.sum())
        frame = frame.loc[~pad]

    if frame.empty:
        raise ValueError("No rows left after dropping blank values and padMedian.")

    if "binCount" in frame.columns:
        frame["binCount"] = pd.to_numeric(frame["binCount"], errors="coerce")

    stats = {
        "source_rows": int(len(raw)),
        "plotted_rows": int(len(frame)),
        "dropped_blank": dropped_blank,
        "dropped_pad": dropped_pad,
    }
    return frame.reset_index(drop=True), stats


def _die_ids(frame: pd.DataFrame) -> list:
    if "dieIdx" not in frame.columns:
        return []
    values = frame["dieIdx"].dropna().unique().tolist()

    def sort_key(value):
        try:
            return (0, float(value))
        except (TypeError, ValueError):
            return (1, str(value))

    return sorted(values, key=sort_key)


def _colors_for(count: int) -> np.ndarray:
    if count <= 1:
        return np.array([[0.16, 0.39, 0.70, 1.0]])
    if count <= 10:
        return plt.get_cmap("tab10")(np.linspace(0, 0.9, count))
    if count <= 20:
        return plt.get_cmap("tab20")(np.linspace(0, 1, count))
    return plt.get_cmap("turbo")(np.linspace(0.08, 0.92, count))


def _marker_sizes(frame: pd.DataFrame) -> np.ndarray:
    if "binCount" not in frame.columns:
        return np.full(len(frame), 22.0)
    counts = pd.to_numeric(frame["binCount"], errors="coerce").to_numpy(dtype=float)
    positive = np.isfinite(counts) & (counts > 0)
    if not positive.any():
        return np.full(len(frame), 22.0)
    peak = counts[positive].max()
    scaled = np.sqrt(np.where(positive, counts, 0.0) / peak)
    return 8.0 + 64.0 * scaled


def _apply_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "#f4f6f8",
            "axes.edgecolor": "#d5dbe3",
            "axes.linewidth": 0.8,
            "axes.labelcolor": "#1c2833",
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "axes.grid": True,
            "grid.color": "white",
            "grid.linewidth": 1.15,
            "xtick.color": "#52606d",
            "ytick.color": "#52606d",
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "text.color": "#1c2833",
            "font.size": 10,
            "legend.frameon": False,
            "legend.fontsize": 8,
            "savefig.dpi": 160,
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",
        }
    )


def _visible_sigma_levels(y_values: np.ndarray) -> list[float]:
    """Return a ±5σ guide when the cloud reaches within 0.6 of that level."""
    y0 = float(np.min(y_values))
    y1 = float(np.max(y_values))
    return [level for level, _name, _color in SIGMA_GUIDES if y0 - 0.6 <= level <= y1 + 0.6]


def _sigma_lines(ax, levels: list[float], labeled: bool) -> None:
    for level, name, color in SIGMA_GUIDES:
        if level not in levels:
            continue
        ax.axhline(
            level,
            color=color,
            linestyle=(0, (4, 3)),
            linewidth=1.05,
            alpha=0.95,
            zorder=1,
        )
        if labeled:
            ax.text(
                0.012,
                level,
                "  " + name,
                transform=ax.get_yaxis_transform(),
                ha="left",
                va="bottom" if level < 0 else "top",
                fontsize=8,
                color=color,
            )


def _hover_text(row: pd.Series) -> str:
    lines = [
        f"bin_def    {row['bin_def']:g}",
        f"σ multiple {row['StddevMultiple']:.4g}",
    ]
    if "dieIdx" in row.index and pd.notna(row["dieIdx"]):
        lines.insert(0, f"dieIdx     {row['dieIdx']}")
    if "parameter" in row.index and pd.notna(row["parameter"]):
        lines.append(f"parameter  {row['parameter']}")
    if "binCount" in row.index and pd.notna(row["binCount"]):
        lines.append(f"binCount   {int(round(float(row['binCount']))):,}")
    return "\n".join(lines)


def _parameters(frame: pd.DataFrame) -> list:
    if "parameter" not in frame.columns:
        return []
    return [value for value in pd.unique(frame["parameter"]) if pd.notna(value)]


def plot_cdf(frame: pd.DataFrame, source_name: str, stats: dict):
    """Draw the CDF and return the figure."""
    _apply_style()
    dies = _die_ids(frame)
    die_index = {die: index for index, die in enumerate(dies)}
    palette = _colors_for(max(len(dies), 1))
    parameters = _parameters(frame)
    panels = parameters if 1 < len(parameters) <= 4 else [None]
    width = 7.2 if len(panels) == 1 else 5.4 * len(panels)

    fig, axes = plt.subplots(
        1,
        len(panels),
        figsize=(width, 6.2),
        sharex=True,
        sharey=True,
        squeeze=False,
        constrained_layout=True,
    )
    axes = list(axes[0])
    hover_items = []
    x_all = frame["bin_def"].to_numpy(dtype=float)
    y_all = frame["StddevMultiple"].to_numpy(dtype=float)
    sigma_levels = _visible_sigma_levels(y_all)

    for axis_number, (ax, parameter) in enumerate(zip(axes, panels)):
        subset = frame if parameter is None else frame.loc[frame["parameter"] == parameter]
        subset = subset.reset_index(drop=True)
        panel_sizes = pd.Series(_marker_sizes(subset), index=subset.index)
        if dies:
            groups = []
            parameter_values = _parameters(subset) or [None]
            for die in dies:
                for parameter_value in parameter_values:
                    group = subset.loc[subset["dieIdx"] == die]
                    if parameter_value is not None and "parameter" in group.columns:
                        group = group.loc[group["parameter"] == parameter_value]
                    groups.append((die, group))
        else:
            groups = [(None, subset)]

        for die, group in groups:
            if group.empty:
                continue
            color = palette[die_index[die]] if die is not None else palette[0]
            ordered = group.sort_values("bin_def")
            if len(ordered) > 1 and ordered["bin_def"].is_unique:
                ax.plot(
                    ordered["bin_def"],
                    ordered["StddevMultiple"],
                    color=color,
                    linewidth=1.2,
                    alpha=0.95,
                    zorder=2,
                    solid_capstyle="round",
                )
            ax.scatter(
                group["bin_def"],
                group["StddevMultiple"],
                s=panel_sizes.loc[group.index],
                color=color,
                alpha=0.9,
                linewidths=0,
                zorder=3,
            )

        ax.set_axisbelow(True)
        ax.set_xlabel("bin_def")
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6, min_n_ticks=4))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6, min_n_ticks=4))
        ax.tick_params(length=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        if parameter is not None:
            title = str(parameter)
        elif len(parameters) == 1:
            title = str(parameters[0])
        elif parameters:
            title = "All parameters"
        else:
            title = "CDF"
        ax.set_title(title)
        _sigma_lines(ax, sigma_levels, labeled=axis_number == len(axes) - 1)

        hover_items.append(
            {
                "ax": ax,
                "x": subset["bin_def"].to_numpy(dtype=float),
                "y": subset["StddevMultiple"].to_numpy(dtype=float),
                "labels": [_hover_text(row) for _, row in subset.iterrows()],
            }
        )

    x_pad = max((float(np.max(x_all)) - float(np.min(x_all))) * 0.04, 1.0)
    y_pad = max((float(np.max(y_all)) - float(np.min(y_all))) * 0.08, 0.4)
    y_low = float(np.min(y_all))
    y_high = float(np.max(y_all))
    if sigma_levels:
        y_low = min(y_low, min(sigma_levels))
        y_high = max(y_high, max(sigma_levels))
    axes[0].set_xlim(float(np.min(x_all)) - x_pad, float(np.max(x_all)) + x_pad)
    axes[0].set_ylim(y_low - y_pad, y_high + y_pad)
    axes[0].set_ylabel("Stddev multiple")

    if 1 < len(dies) <= 12:
        handles = [
            Line2D(
                [0],
                [0],
                color=palette[index],
                marker="o",
                linewidth=1.5,
                markersize=5.5,
                label=f"Die {die}",
            )
            for index, die in enumerate(dies)
        ]
        axes[-1].legend(
            handles=handles,
            title="dieIdx",
            loc="upper left",
            bbox_to_anchor=(1.02, 1.0),
            borderaxespad=0,
        )
    elif len(dies) > 12:
        color_map = ListedColormap(palette)
        norm = BoundaryNorm(np.arange(len(dies) + 1) - 0.5, len(dies))
        mappable = plt.cm.ScalarMappable(norm=norm, cmap=color_map)
        mappable.set_array([])
        colorbar = fig.colorbar(mappable, ax=axes, pad=0.012, fraction=0.04)
        step = 1 if len(dies) <= 24 else max(len(dies) // 12, 1)
        ticks = np.arange(0, len(dies), step)
        colorbar.set_ticks(ticks)
        colorbar.ax.set_yticklabels([str(dies[int(tick)]) for tick in ticks])
        colorbar.set_label("dieIdx")
        colorbar.outline.set_visible(False)
        colorbar.ax.tick_params(length=0)

    die_note = f"{len(dies)} dies" if dies else "no dieIdx"
    if not parameters:
        parameter_note = "no parameter column"
    elif len(parameters) == 1:
        parameter_note = str(parameters[0])
    else:
        parameter_note = f"{len(parameters)} parameters"
    size_note = "  ·  marker area follows binCount" if "binCount" in frame.columns else ""
    fig.suptitle(source_name, fontsize=14)
    fig.supxlabel(
        (
            f"{stats['plotted_rows']:,} points from {stats['source_rows']:,} rows"
            f"  ·  {die_note}  ·  {parameter_note}"
            f"  ·  {stats['dropped_blank']:,} blank and {stats['dropped_pad']:,} padMedian left out"
            f"{size_note}  ·  hover a point for its values"
        ),
        fontsize=8,
        color="#52606d",
    )
    manager = getattr(fig.canvas, "manager", None)
    if manager is not None and hasattr(manager, "set_window_title"):
        manager.set_window_title(f"CDF — {source_name}")
    _attach_hover(fig, hover_items)
    return fig


def _attach_hover(fig, items) -> None:
    annotations = {}
    for item in items:
        ax = item["ax"]
        if ax in annotations:
            continue
        note = ax.annotate(
            "",
            xy=(0, 0),
            xytext=(14, 14),
            textcoords="offset points",
            ha="left",
            va="bottom",
            fontsize=8,
            color="#1c2833",
            bbox={
                "boxstyle": "round,pad=0.45",
                "facecolor": "white",
                "edgecolor": "#d5dbe3",
                "alpha": 0.97,
            },
            arrowprops={"arrowstyle": "-", "color": "#9aa5b1", "lw": 0.8},
            zorder=5,
        )
        note.set_visible(False)
        annotations[ax] = note

    def on_move(event):
        hit = None
        best = 14.0
        if event.inaxes is not None and event.x is not None:
            for item in items:
                if event.inaxes is not item["ax"] or len(item["x"]) == 0:
                    continue
                pixels = item["ax"].transData.transform(np.column_stack([item["x"], item["y"]]))
                distance = np.hypot(pixels[:, 0] - event.x, pixels[:, 1] - event.y)
                index = int(np.argmin(distance))
                if distance[index] < best:
                    best = float(distance[index])
                    hit = (item, index)
        for note in annotations.values():
            note.set_visible(False)
        if hit is not None:
            item, index = hit
            note = annotations[item["ax"]]
            note.xy = (float(item["x"][index]), float(item["y"][index]))
            note.set_text(item["labels"][index])
            note.set_visible(True)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_move)


def _choose_file() -> str:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    try:
        return filedialog.askopenfilename(
            title="Choose the CDF file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
    finally:
        root.destroy()


def _report_error(message: str, interactive: bool) -> None:
    print(message, file=sys.stderr)
    if not interactive:
        return
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        try:
            messagebox.showerror("CDF Plotter", message)
        finally:
            root.destroy()
    except Exception:
        return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plot bin_def against StddevMultiple from a CDF CSV."
    )
    parser.add_argument("csv", nargs="?", help="CDF CSV. If omitted, a file dialog opens.")
    parser.add_argument(
        "--save",
        metavar="PATH",
        help="Save the figure to this image path instead of opening a window.",
    )
    args = parser.parse_args(argv)

    interactive = args.csv is None
    path = args.csv or _choose_file()
    if not path:
        print("No file selected.")
        return 0

    try:
        frame, stats = load_cdf(path)
    except Exception as exc:
        _report_error(f"Could not plot {path}\n\n{exc}", interactive)
        return 1

    print(
        f"Plotting {stats['plotted_rows']} of {stats['source_rows']} rows "
        f"({stats['dropped_blank']} blank or non-numeric, {stats['dropped_pad']} padMedian)."
    )
    print(
        f"bin_def {frame['bin_def'].min():g} … {frame['bin_def'].max():g}    "
        f"StddevMultiple {frame['StddevMultiple'].min():.4g} … {frame['StddevMultiple'].max():.4g}"
    )
    figure = plot_cdf(frame, Path(path).name, stats)
    if args.save:
        figure.savefig(args.save)
        print(f"Saved {args.save}")
        plt.close(figure)
        return 0

    plt.show()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

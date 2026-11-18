"""Expert, objective, and learned weight schemes for IMS criteria (SPEC §3.4)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np
import pandas as pd
import yaml
from pymcdm import weights as pymcdm_weights

from imsfe.config import VariablesConfig, config_dir, load_variables

logger = logging.getLogger(__name__)

WeightSchemeId = Literal["expert_mean", "equal", "entropy", "critic", "learned"]

# Conceptual bridge from new factors to legacy expert-factor labels in
# weights_expert.yaml (COST/LOGI/…). Factors without a mapping receive equal
# residual mass among themselves after mapped factors take their expert means.
LEGACY_FACTOR_MAP: dict[str, str] = {
    "cost_access": "COST",
    "logistics": "LOGI",
    "competition": "COMM",
    "macro_risk": "ECON",
    "institutional": "POLI",
    "product_fit": "CULT",
}


@dataclass(frozen=True)
class Weights:
    """Validated hierarchical weights: factors sum to 1; within each factor vars sum to 1."""

    factors: pd.Series
    variables_within: dict[str, pd.Series]
    scheme: str
    notes: tuple[str, ...] = field(default_factory=tuple)

    def flat(self, variable_ids: list[str] | None = None) -> pd.Series:
        """Global variable weights = factor_w × within_factor_w (sums to 1)."""
        parts: dict[str, float] = {}
        for factor, fw in self.factors.items():
            vw = self.variables_within[str(factor)]
            for vid, w in vw.items():
                parts[str(vid)] = float(fw) * float(w)
        s = pd.Series(parts, dtype=float)
        if variable_ids is not None:
            s = s.reindex(variable_ids).fillna(0.0)
            total = float(s.sum())
            if total > 0:
                s = s / total
        return s

    def restrict(self, available: list[str]) -> Weights:
        """Drop missing variables and renormalise within factors / across factors."""
        notes = list(self.notes)
        new_within: dict[str, pd.Series] = {}
        factor_mass: dict[str, float] = {}
        for factor, fw in self.factors.items():
            vw = self.variables_within[str(factor)]
            keep = [v for v in vw.index if v in available]
            if not keep:
                notes.append(f"factor {factor} dropped (no available variables)")
                continue
            sub = vw.loc[keep].astype(float)
            sub = sub / sub.sum()
            new_within[str(factor)] = sub
            factor_mass[str(factor)] = float(fw)
        if not factor_mass:
            raise ValueError("No variables left after restricting weights")
        factors = pd.Series(factor_mass, dtype=float)
        factors = factors / factors.sum()
        return Weights(
            factors=factors,
            variables_within=new_within,
            scheme=self.scheme,
            notes=tuple(notes),
        )


def _validate_weights(weights: Weights) -> Weights:
    if (weights.factors < 0).any():
        raise ValueError("factor weights must be non-negative")
    if not np.isclose(weights.factors.sum(), 1.0, atol=1e-8):
        raise ValueError(f"factor weights must sum to 1; got {weights.factors.sum()}")
    for factor, vw in weights.variables_within.items():
        if (vw < 0).any():
            raise ValueError(f"variable weights in {factor} must be non-negative")
        if not np.isclose(vw.sum(), 1.0, atol=1e-8):
            raise ValueError(
                f"variable weights in {factor} must sum to 1; got {vw.sum()}"
            )
    return weights


def load_expert_yaml(path: Path | None = None) -> dict[str, Any]:
    p = path or (config_dir() / "weights_expert.yaml")
    with p.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Invalid expert weights file: {p}")
    return data


def _equal_within_factors(variables: VariablesConfig) -> tuple[pd.Series, dict[str, pd.Series]]:
    factors = sorted({v.factor for v in variables.variables})
    fw = pd.Series(1.0 / len(factors), index=factors, dtype=float)
    within: dict[str, pd.Series] = {}
    for factor in factors:
        vids = [v.id for v in variables.variables if v.factor == factor]
        within[factor] = pd.Series(1.0 / len(vids), index=vids, dtype=float)
    return fw, within


def weights_equal(variables: VariablesConfig | None = None) -> Weights:
    variables = variables or load_variables()
    fw, within = _equal_within_factors(variables)
    return _validate_weights(Weights(factors=fw, variables_within=within, scheme="equal"))


def weights_expert_mean(
    variables: VariablesConfig | None = None,
    expert_path: Path | None = None,
) -> Weights:
    """Expert means with equal share for unmapped new variables (logged)."""
    variables = variables or load_variables()
    expert = load_expert_yaml(expert_path)
    notes: list[str] = []
    legacy_factors: dict[str, float] = {
        k: float(v["mean"]) for k, v in expert.get("factors", {}).items()
    }
    legacy_vars: dict[str, float] = {
        k: float(v["mean"]) for k, v in expert.get("variables", {}).items()
    }

    # Factor weights via LEGACY_FACTOR_MAP; unmapped factors share residual equally.
    mapped = {
        f: legacy_factors[LEGACY_FACTOR_MAP[f]]
        for f in {v.factor for v in variables.variables}
        if f in LEGACY_FACTOR_MAP and LEGACY_FACTOR_MAP[f] in legacy_factors
    }
    unmapped = sorted(
        {v.factor for v in variables.variables if v.factor not in mapped}
    )
    if mapped:
        mapped_series = pd.Series(mapped, dtype=float)
        mapped_series = mapped_series / mapped_series.sum()
        # Keep mapped mass proportional to expert means; give unmapped equal slice
        # of a residual share equal to n_unmapped / n_factors.
        n_all = len(mapped) + len(unmapped)
        mapped_mass = len(mapped) / n_all
        unmapped_mass = 1.0 - mapped_mass
        fw_parts = (mapped_series * mapped_mass).to_dict()
        if unmapped:
            share = unmapped_mass / len(unmapped)
            for f in unmapped:
                fw_parts[f] = share
                notes.append(
                    f"factor {f}: no legacy expert mapping; equal residual share={share:.4f}"
                )
        fw = pd.Series(fw_parts, dtype=float)
    else:
        fw, _ = _equal_within_factors(variables)
        notes.append("no legacy factor mapping available; using equal factor weights")

    fw = fw / fw.sum()

    within: dict[str, pd.Series] = {}
    for factor in fw.index:
        vids = [v.id for v in variables.variables if v.factor == factor]
        known = {vid: legacy_vars[vid] for vid in vids if vid in legacy_vars}
        unknown = [vid for vid in vids if vid not in legacy_vars]
        if known and unknown:
            known_s = pd.Series(known, dtype=float)
            known_s = known_s / known_s.sum()
            # Split mass: known keep relative expert means over |known|/|vids|;
            # unknown share the rest equally.
            known_mass = len(known) / len(vids)
            unknown_mass = 1.0 - known_mass
            parts = (known_s * known_mass).to_dict()
            u_share = unknown_mass / len(unknown)
            for vid in unknown:
                parts[vid] = u_share
                notes.append(
                    f"{vid}: no expert weight; equal share inside {factor} ({u_share:.4f})"
                )
            within[str(factor)] = pd.Series(parts, dtype=float)
        elif known:
            s = pd.Series(known, dtype=float)
            within[str(factor)] = s / s.sum()
        else:
            within[str(factor)] = pd.Series(1.0 / len(vids), index=vids, dtype=float)
            for vid in vids:
                notes.append(
                    f"{vid}: no expert weight; equal share inside {factor} ({1.0 / len(vids):.4f})"
                )

    for msg in notes:
        logger.debug("expert_mean: %s", msg)
    return _validate_weights(
        Weights(
            factors=fw,
            variables_within=within,
            scheme="expert_mean",
            notes=tuple(notes),
        )
    )


def _shift_nonnegative(matrix: pd.DataFrame) -> pd.DataFrame:
    """Column-wise shift to strictly positive values (entropy requirement)."""
    out = matrix.astype(float).copy()
    for col in out.columns:
        col_min = float(out[col].min())
        out[col] = out[col] - col_min + 1e-12
    return out


def weights_entropy(matrix: pd.DataFrame) -> pd.Series:
    """Entropy weights over columns of a complete numeric matrix (flat).

    Columns are shifted to be strictly positive before calling pymcdm, so
    zero/negative feature values (e.g. GRW, UVGAP) do not abort the scheme.
    """
    arr = _shift_nonnegative(matrix).to_numpy(dtype=float)
    w = pymcdm_weights.entropy_weights(arr)
    return pd.Series(w, index=list(matrix.columns), dtype=float)


def weights_critic(matrix: pd.DataFrame, directions: dict[str, str]) -> pd.Series:
    """CRITIC weights; ``directions`` maps column -> benefit|cost."""
    # CRITIC uses correlation/std; allow any real values (no positivity needed).
    arr = matrix.to_numpy(dtype=float)
    types = np.array(
        [1 if directions[c] == "benefit" else -1 for c in matrix.columns],
        dtype=int,
    )
    w = pymcdm_weights.critic_weights(arr, types)
    return pd.Series(w, index=list(matrix.columns), dtype=float)


def flat_to_hierarchical(
    flat: pd.Series,
    variables: VariablesConfig,
    scheme: str,
) -> Weights:
    """Lift flat column weights into the factor hierarchy (renormalised)."""
    within: dict[str, pd.Series] = {}
    factor_mass: dict[str, float] = {}
    for factor in {v.factor for v in variables.variables}:
        vids = [v.id for v in variables.variables if v.factor == factor and v.id in flat.index]
        if not vids:
            continue
        sub = flat.loc[vids].astype(float).clip(lower=0.0)
        mass = float(sub.sum())
        if mass <= 0:
            sub = pd.Series(1.0 / len(vids), index=vids, dtype=float)
            mass = 0.0
        else:
            sub = sub / sub.sum()
        within[factor] = sub
        factor_mass[factor] = mass if mass > 0 else 1.0
    factors = pd.Series(factor_mass, dtype=float)
    factors = factors / factors.sum()
    return _validate_weights(
        Weights(factors=factors, variables_within=within, scheme=scheme)
    )


_LEARNED_CACHE: Weights | None = None


def set_learned_weights(weights: Weights) -> None:
    """Store fitted learned weights for ``get_weights('learned')``."""
    global _LEARNED_CACHE
    _LEARNED_CACHE = _validate_weights(weights)


def clear_learned_weights() -> None:
    global _LEARNED_CACHE
    _LEARNED_CACHE = None


def weights_learned(*_args: Any, **_kwargs: Any) -> Weights:
    """Return fitted learned weights (Phase 6). Raises if not yet fitted."""
    if _LEARNED_CACHE is None:
        raise RuntimeError(
            "learned weights are not fitted yet; call "
            "imsfe.validation.learned.fit_learned_weights(...) first"
        )
    return _LEARNED_CACHE


def get_weights(
    scheme: WeightSchemeId,
    variables: VariablesConfig | None = None,
    *,
    matrix: pd.DataFrame | None = None,
    directions: dict[str, str] | None = None,
) -> Weights:
    """Dispatch weight scheme. Entropy/CRITIC require a complete ``matrix``."""
    variables = variables or load_variables()
    if scheme == "equal":
        return weights_equal(variables)
    if scheme == "expert_mean":
        return weights_expert_mean(variables)
    if scheme == "learned":
        return weights_learned()
    if scheme in ("entropy", "critic"):
        if matrix is None or matrix.empty:
            raise ValueError(f"{scheme} weights require a non-empty matrix")
        if scheme == "entropy":
            flat = weights_entropy(matrix)
        else:
            if directions is None:
                raise ValueError("critic weights require directions")
            flat = weights_critic(matrix, directions)
        return flat_to_hierarchical(flat, variables, scheme)
    raise ValueError(f"Unknown weight scheme: {scheme}")

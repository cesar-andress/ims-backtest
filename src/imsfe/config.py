"""Load and validate YAML configuration for settings, variables, and experiments."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

FactorId = Literal[
    "demand",
    "cost_access",
    "logistics",
    "competition",
    "product_fit",
    "macro_risk",
    "institutional",
    "openness_legacy",
]

SPEC_FACTORS: tuple[FactorId, ...] = (
    "demand",
    "cost_access",
    "logistics",
    "competition",
    "product_fit",
    "macro_risk",
    "institutional",
    "openness_legacy",
)

Direction = Literal["benefit", "cost"]
Transform = Literal["none", "log", "log1p"]
NormalizationId = Literal["ratio_legacy", "minmax", "zscore", "rank", "log_minmax"]
McdmId = Literal["wsm", "topsis", "vikor", "promethee_ii"]
WeightSchemeId = Literal["expert_mean", "equal", "entropy", "critic", "learned"]


def project_root() -> Path:
    """Return the repository root (folder that contains config/)."""
    return Path(__file__).resolve().parents[2]


def config_dir() -> Path:
    """Return the path to config/."""
    return project_root() / "config"


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        raise ValueError(f"Config file is empty: {path}")
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a mapping: {path}")
    return data


class YearsSettings(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def _check_range(self) -> YearsSettings:
        if self.end < self.start:
            raise ValueError("years.end must be >= years.start")
        return self


class HsChaptersSettings(BaseModel):
    primary: str
    robustness: list[str] = Field(default_factory=list)


class SourceRefSettings(BaseModel):
    url: str = ""
    version: str = ""
    nomenclature: str | None = None


class WitsSettings(BaseModel):
    version: str = "trains-ahs"
    base_url: str = (
        "https://wits.worldbank.org/API/V1/SDMX/V21/rest/data/DF_WITS_TradeStats_Tariff"
    )
    indicator: str = "AHS-SMPL-AVRG"
    product: str = "Total"


class WorldBankSettings(BaseModel):
    wdi_source_id: int = 2
    wgi_source_id: int = 3


class SmaaSettings(BaseModel):
    n_samples: int = 10_000
    seed: int = 42


class BootstrapSettings(BaseModel):
    n_reps: int = 2_000
    seed: int = 42


class Settings(BaseModel):
    origins: list[str]
    n_destinations: int = 60
    hs_chapters: HsChaptersSettings
    years: YearsSettings
    horizons: list[int]
    entry_threshold_usd: float = 50_000
    seed: int = 42
    baci: SourceRefSettings = Field(default_factory=SourceRefSettings)
    cepii_gravity: SourceRefSettings = Field(default_factory=SourceRefSettings)
    wits: WitsSettings = Field(default_factory=WitsSettings)
    worldbank: WorldBankSettings = Field(default_factory=WorldBankSettings)
    smaa: SmaaSettings = Field(default_factory=SmaaSettings)
    bootstrap: BootstrapSettings = Field(default_factory=BootstrapSettings)

    def hs_chapter_codes(self) -> list[str]:
        """Unique HS chapter codes (primary + robustness), zero-padded to 2 digits."""
        codes = [self.hs_chapters.primary, *self.hs_chapters.robustness]
        return sorted({str(c).zfill(2) for c in codes})

    @field_validator("origins")
    @classmethod
    def _nonempty_origins(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("origins must not be empty")
        return value

    @field_validator("horizons")
    @classmethod
    def _positive_horizons(cls, value: list[int]) -> list[int]:
        if not value or any(h < 1 for h in value):
            raise ValueError("horizons must be a non-empty list of integers >= 1")
        return value


class VariableConfig(BaseModel):
    id: str
    name: str
    factor: FactorId
    direction: Direction
    source: str
    code: str
    transform: Transform
    origin_specific: bool
    unit: str = ""
    notes: str = ""


class VariablesConfig(BaseModel):
    factors: list[FactorId]
    variables: list[VariableConfig]

    @model_validator(mode="after")
    def _check_factors_and_ids(self) -> VariablesConfig:
        if tuple(self.factors) != SPEC_FACTORS:
            raise ValueError(
                f"factors must match SPEC exactly: {list(SPEC_FACTORS)}; got {self.factors}"
            )
        ids = [v.id for v in self.variables]
        if len(ids) != len(set(ids)):
            raise ValueError("variable ids must be unique")
        for var in self.variables:
            if var.factor not in self.factors:
                raise ValueError(f"variable {var.id} has unknown factor {var.factor}")
        return self


class ExperimentDefault(BaseModel):
    normalization: NormalizationId
    mcdm: McdmId
    weights: WeightSchemeId


class ExperimentsConfig(BaseModel):
    normalizations: list[NormalizationId]
    mcdm_methods: list[McdmId]
    weight_schemes: list[WeightSchemeId]
    default: ExperimentDefault
    baselines: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _default_in_grid(self) -> ExperimentsConfig:
        if self.default.normalization not in self.normalizations:
            raise ValueError("default.normalization must be listed in normalizations")
        if self.default.mcdm not in self.mcdm_methods:
            raise ValueError("default.mcdm must be listed in mcdm_methods")
        if self.default.weights not in self.weight_schemes:
            raise ValueError("default.weights must be listed in weight_schemes")
        return self


def load_settings(path: Path | None = None) -> Settings:
    """Load settings.yaml."""
    return Settings.model_validate(_load_yaml(path or config_dir() / "settings.yaml"))


def load_variables(path: Path | None = None) -> VariablesConfig:
    """Load variables.yaml."""
    return VariablesConfig.model_validate(_load_yaml(path or config_dir() / "variables.yaml"))


def load_experiments(path: Path | None = None) -> ExperimentsConfig:
    """Load experiments.yaml."""
    return ExperimentsConfig.model_validate(_load_yaml(path or config_dir() / "experiments.yaml"))

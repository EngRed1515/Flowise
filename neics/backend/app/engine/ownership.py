"""Enterprise Group & Ownership Intelligence Engine.

Walks the directed ownership graph (ownership_edge) to compute, for any entity:
  * effective government ownership / voting % (direct + indirect, across vehicles)
  * effective foreign ownership %
  * present control indicators
  * the Ultimate Controlling Institutional Unit (UCI)
  * the ownership chain (for explainability / visualisation)

This implements the substance-over-form control logic of framework Test 8 and the
aggregation rule from Case Study 02 (holdings summed across multiple state vehicles).
"""
from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enterprise import OwnershipEdge

# Strength order for choosing a representative control flag (strongest first).
CONTROL_PRIORITY = [
    "MAJ-VOTE",
    "GOLDEN",
    "BOARD",
    "KEY-PERS",
    "CONTRACT",
    "REGULATORY",
    "FINANCING",
    "DOMINANT",
    "BO-CHAIN",
]


class OwnershipEngine:
    def __init__(self, db: Session):
        self.db = db
        self._incoming: dict[str, list[OwnershipEdge]] = defaultdict(list)
        for edge in db.execute(select(OwnershipEdge)).scalars():
            self._incoming[edge.owned_id].append(edge)

    # --- recursive effective-share computation with cycle guard ---
    def _effective_share(self, node: str, predicate, use_voting: bool, _seen: frozenset) -> float:
        """Fraction (0..1) of `node` ultimately attributable to owners matching predicate."""
        if node in _seen:
            return 0.0
        seen = _seen | {node}
        total = 0.0
        for edge in self._incoming.get(node, []):
            pct = (edge.voting_pct if use_voting else edge.ownership_pct) or 0.0
            frac = pct / 100.0
            if predicate(edge):
                total += frac
            else:
                # propagate through intermediate owner that is itself an entity
                total += frac * self._effective_share(edge.owner_id, predicate, use_voting, seen)
        return min(total, 1.0)

    def government_ownership(self, entity_id: str) -> float:
        return round(100.0 * self._effective_share(entity_id, lambda e: e.owner_is_government, False, frozenset()), 2)

    def government_voting(self, entity_id: str) -> float:
        return round(100.0 * self._effective_share(entity_id, lambda e: e.owner_is_government, True, frozenset()), 2)

    def foreign_ownership(self, entity_id: str) -> float:
        return round(
            100.0 * self._effective_share(entity_id, lambda e: not e.owner_is_resident, False, frozenset()), 2
        )

    def direct_edges(self, entity_id: str) -> list[OwnershipEdge]:
        return self._incoming.get(entity_id, [])

    def max_single_foreign(self, entity_id: str) -> float:
        return round(
            max(
                (e.voting_pct or e.ownership_pct or 0.0)
                for e in self.direct_edges(entity_id)
                if not e.owner_is_resident
            )
            if any(not e.owner_is_resident for e in self.direct_edges(entity_id))
            else 0.0,
            2,
        )

    def control_indicators(self, entity_id: str) -> list[str]:
        inds: list[str] = []
        for e in self.direct_edges(entity_id):
            if e.control_indicator and e.control_indicator not in ("NONE", None):
                inds.append(e.control_indicator)
        return inds

    def max_direct_voting(self, entity_id: str) -> float:
        edges = self.direct_edges(entity_id)
        return round(max((e.voting_pct or e.ownership_pct or 0.0) for e in edges), 2) if edges else 0.0

    @staticmethod
    def strongest(indicators: list[str]) -> str | None:
        for cand in CONTROL_PRIORITY:
            if cand in indicators:
                return cand
        return None

    def government_control_indicators(self, entity_id: str) -> list[str]:
        return [
            e.control_indicator
            for e in self.direct_edges(entity_id)
            if e.owner_is_government and e.control_indicator and e.control_indicator not in ("NONE", None)
        ]

    def ultimate_controlling_unit(self, entity_id: str, _seen: frozenset = frozenset()) -> dict[str, Any] | None:
        """Find the top-of-chain controlling owner (>50% voting or marked is_ultimate)."""
        if entity_id in _seen:
            return None
        edges = self.direct_edges(entity_id)
        if not edges:
            return None
        # Prefer an explicitly flagged ultimate edge, else the largest voting holder.
        ultimate = next((e for e in edges if e.is_ultimate == "Y"), None)
        dominant = ultimate or max(edges, key=lambda e: (e.voting_pct or e.ownership_pct or 0.0))
        owner = dominant.owner_id
        # If the owner is itself an owned entity, recurse upward.
        parent = self.ultimate_controlling_unit(owner, _seen | {entity_id})
        if parent:
            return parent
        return {
            "uci_id": owner,
            "uci_name": dominant.owner_name,
            "is_government": dominant.owner_is_government,
            "is_resident": dominant.owner_is_resident,
            "country": dominant.owner_country,
        }

    def chain(self, entity_id: str, _seen: frozenset = frozenset()) -> list[dict[str, Any]]:
        """Flatten the upstream ownership chain for visualisation / explainability."""
        if entity_id in _seen:
            return []
        out: list[dict[str, Any]] = []
        for e in self.direct_edges(entity_id):
            out.append(
                {
                    "owner_id": e.owner_id,
                    "owner_name": e.owner_name,
                    "owned_id": e.owned_id,
                    "ownership_pct": e.ownership_pct,
                    "voting_pct": e.voting_pct,
                    "control_indicator": e.control_indicator,
                    "is_government": e.owner_is_government,
                    "is_resident": e.owner_is_resident,
                }
            )
            out.extend(self.chain(e.owner_id, _seen | {entity_id}))
        return out

    def facts(self, entity_id: str) -> dict[str, Any]:
        """Assemble the ownership-derived fact set consumed by the rules engine."""
        gov_own = self.government_ownership(entity_id)
        gov_vote = self.government_voting(entity_id)
        gov_inds = self.government_control_indicators(entity_id)
        all_inds = self.control_indicators(entity_id)
        foreign_own = self.foreign_ownership(entity_id)
        uci = self.ultimate_controlling_unit(entity_id)

        max_vote = self.max_direct_voting(entity_id)

        # Government control: majority effective voting OR any government control indicator.
        gov_control = gov_vote > 50.0 or len(gov_inds) > 0

        # Representative control flag — the mechanism by which the *controlling* unit
        # exercises effective control. When the entity is government-controlled the flag
        # reflects the government's control mechanism (e.g. a golden share or board
        # rights), even where a private block holds larger voting rights.
        if gov_control:
            rep_flag = self.strongest(gov_inds) or ("MAJ-VOTE" if gov_vote > 50.0 else "BO-CHAIN")
        elif max_vote > 50.0:
            rep_flag = "MAJ-VOTE"
        elif all_inds:
            rep_flag = self.strongest(all_inds) or "NONE"
        elif foreign_own > 50.0:
            rep_flag = "BO-CHAIN"
        else:
            rep_flag = "NONE"

        return {
            "government_ownership_pct": gov_own,
            "government_voting_pct": gov_vote,
            "foreign_ownership_pct": foreign_own,
            "max_single_foreign_pct": self.max_single_foreign(entity_id),
            "max_direct_voting": max_vote,
            "control_indicators": all_inds,
            "government_control_indicators": gov_inds,
            "has_control_indicator": len(all_inds) > 0,
            "has_government_control_indicator": len(gov_inds) > 0,
            "government_control": gov_control,
            "representative_control_flag": rep_flag,
            "uci_is_government": bool(uci and uci["is_government"]),
            "uci_is_foreign": bool(uci and not uci["is_resident"]),
            "uci": uci,
        }

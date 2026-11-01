import pandas as pd
import numpy as np
import random
import uuid
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class SynthConfig:
    fraud_prevalence: float = 0.05  # 3-12%
    noise_level: float = 0.02
    missing_data_rate: float = 0.01
    num_samples: int = 1000

class SyntheticFraudGenerator:
    """
    ML-09 (Data Synth) - Synthetic Data Generator v2.1
    Generates robust synthetic healthcare claims for fraud detection testing.
    """

    SCENARIOS = {
        "SYND-01": "Upcoding",           # Higher complexity code than actual service
        "SYND-02": "Phantom Billing",    # Billing for services not rendered
        "SYND-03": "Kickback",          # Unlawful payment for referrals
        "SYND-04": "Unbundling",        # Separate billing for components of a single procedure
        "SYND-05": "Churning",          # Unnecessary tests to increase billing
        "SYND-06": "Up-selling",        # Pushing more expensive treatments
        "SYND-07": "Double Billing",    # Billing multiple times for same service
        "SYND-08": "Identity Theft",    # Using patient ID for fake claims
        "SYND-09": "Provider Collusion" # Providers working together to inflate claims
    }

    def __init__(self, config: SynthConfig):
        self.config = config
        self.providers = [f"RS_{chr(65+i)}" for i in range(10)] # RS_A to RS_J
        self.patients = [f"P{i:02d}" for i in range(100)] # P01 to P100
        self.doctors = [f"D{i:02d}" for i in range(30)] # D01 to D30

    def _pseudonymize(self, category: str, index: int) -> str:
        if category == 'provider': return random.choice(self.providers)
        if category == 'patient': return random.choice(self.patients)
        if category == 'doctor': return random.choice(self.doctors)
        return "UNKNOWN"

    def _generate_base_claim(self) -> Dict[str, Any]:
        claim_id = str(uuid.uuid4())
        patient_id = self._pseudonymize('patient', 0)
        provider_id = self._pseudonymize('provider', 0)
        doctor_id = self._pseudonymize('doctor', 0)

        # Base values
        cost = random.uniform(100, 5000)
        date = datetime.now() - timedelta(days=random.randint(0, 365))

        return {
            "claim_id": claim_id,
            "patient_id": patient_id,
            "provider_id": provider_id,
            "doctor_id": doctor_id,
            "amount": round(cost, 2),
            "date": date.strftime("%Y-%m-%d"),
            "icd10": random.choice(["E11.9", "I10", "J45.909", "M17.11"]),
            "is_fraud": 0,
            "scenario": "NONE"
        }

    def _apply_fraud_scenario(self, claim: Dict[str, Any], scenario_id: str):
        scenario_name = self.SCENARIOS[scenario_id]
        claim["is_fraud"] = 1
        claim["scenario"] = scenario_id

        if scenario_id == "SYND-01": # Upcoding
            claim["amount"] *= 2.5
        elif scenario_id == "SYND-02": # Phantom Billing
            claim["amount"] = random.uniform(500, 2000)
        elif scenario_id == "SYND-04": # Unbundling
            # Simplified as cost inflation
            claim["amount"] *= 1.8
        elif scenario_id == "SYND-07": # Double Billing
            # Handled at generator level by duplicating row
            pass
        else:
            claim["amount"] *= 1.5

    def generate(self) -> pd.DataFrame:
        data = []
        for _ in range(self.config.num_samples):
            claim = self._generate_base_claim()

            if random.random() < self.config.fraud_prevalence:
                scenario_id = random.choice(list(self.SCENARIOS.keys()))
                self._apply_fraud_scenario(claim, scenario_id)

                if scenario_id == "SYND-07": # Double Billing: create a duplicate
                    duplicate = claim.copy()
                    duplicate["claim_id"] = str(uuid.uuid4())
                    data.append(duplicate)

            # Apply Noise
            if random.random() < self.config.noise_level:
                claim["amount"] += random.uniform(-50, 50)

            # Apply Missing Data
            if random.random() < self.config.missing_data_rate:
                key = random.choice(["icd10", "doctor_id", "patient_id"])
                claim[key] = None

            data.append(claim)

        return pd.DataFrame(data)

    def to_fhir_bundle(self, df: pd.DataFrame) -> str:
        bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": []
        }

        for _, row in df.iterrows():
            resource = {
                "resource": {
                    "resourceType": "Claim",
                    "id": row["claim_id"],
                    "status": "active",
                    "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/claim-type", "code": "institutional"}]},
                    "patient": {"reference": f"Patient/{row['patient_id']}"},
                    "provider": {"reference": f"Organization/{row['provider_id']}"},
                    "total": {"value": row["amount"], "currency": "IDR"},
                    "diagnosis": [{"condition": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": row["icd10"]}]}}] if row["icd10"] else []
                }
            }
            bundle["entry"].append(resource)

        return json.dumps(bundle, indent=2)

if __name__ == "__main__":
    config = SynthConfig(fraud_prevalence=0.08, num_samples=100)
    gen = SyntheticFraudGenerator(config)
    df = gen.generate()

    # Save CSV
    df.to_csv("synthetic_fraud_data.csv", index=False)

    # Save FHIR
    with open("synthetic_fhir_bundle.json", "w") as f:
        f.write(gen.to_fhir_bundle(df))

    print(f"Generated {len(df)} samples. Fraud rate: {df['is_fraud'].mean():.2%}")

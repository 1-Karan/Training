from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from pathlib import Path
import json
import uuid
import threading
import copy

# Constants
DATA_PATH = Path(__file__).with_name("data.json")

app = FastAPI(title="Healthcare Appointment Scheduler API", version="1.0.0")
_lock = threading.Lock()


# ---- Models ----
class Doctor(BaseModel):
    id: str
    name: str
    specialty: str


class AppointmentIn(BaseModel):
    doctor_id: str
    patient_name: str = Field(min_length=1)
    time: str  # e.g., "2025-11-05 10:00"


class Appointment(AppointmentIn):
    id: str


class Store(BaseModel):
    doctors: List[Doctor]
    slots: Dict[str, List[str]]
    appointments: List[Appointment]


# ---- Seed data ----
SEED = Store(
    doctors=[
        Doctor(id="dr_1", name="Dr. Aditi Mehra", specialty="General Medicine"),
        Doctor(id="dr_2", name="Dr. Rohan Iyer", specialty="Pediatrics"),
    ],
    slots={
        "dr_1": ["2025-11-05 10:00", "2025-11-05 11:00", "2025-11-05 14:00"],
        "dr_2": ["2025-11-05 09:00", "2025-11-05 12:00", "2025-11-05 15:00"],
    },
    appointments=[],
)


# ---- Helpers ----
def _read_store() -> Store:
    """Safely load the data store. If file missing, empty, or invalid — auto-reset."""
    if not DATA_PATH.exists():
        _write_store(SEED)
        return SEED

    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            raw_content = f.read().strip()
            if not raw_content:
                # empty file → reset
                _write_store(SEED)
                return SEED
            raw = json.loads(raw_content)
        return Store.model_validate(raw)

    except (json.JSONDecodeError, ValueError):
        # corrupt JSON → reset
        _write_store(SEED)
        return SEED



def _write_store(store: Store) -> None:
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(store.model_dump(), f, indent=2, ensure_ascii=False)


# ---- API Endpoints ----
@app.get("/doctors", response_model=List[Doctor])
def list_doctors():
    with _lock:
        store = _read_store()
        return store.doctors


@app.get("/available-slots/{doctor_id}")
def available_slots(doctor_id: str):
    with _lock:
        store = _read_store()
        if doctor_id not in {d.id for d in store.doctors}:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return {"doctor_id": doctor_id, "available_slots": store.slots.get(doctor_id, [])}


@app.get("/appointments", response_model=List[Appointment])
def list_appointments():
    with _lock:
        store = _read_store()
        return store.appointments


@app.post("/book-appointment")
def book_appointment(payload: AppointmentIn):
    with _lock:
        store = _read_store()
        if payload.doctor_id not in {d.id for d in store.doctors}:
            raise HTTPException(status_code=404, detail="Doctor not found")
        slots = store.slots.get(payload.doctor_id, [])
        if payload.time not in slots:
            raise HTTPException(status_code=409, detail="Slot not available")
        appt = Appointment(id=str(uuid.uuid4()), **payload.model_dump())
        store.appointments.append(appt)
        store.slots[payload.doctor_id] = [s for s in slots if s != payload.time]
        _write_store(store)
        return {"message": "Appointment booked", "appointment": appt.model_dump()}


@app.post("/reset")
def reset_store():
    """Reset data.json back to seed."""
    with _lock:
        _write_store(copy.deepcopy(SEED))
    return {"message": "Store reset to seed"}

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


@dataclass
class Job:
    id: str
    status: str = "queued"        # queued | running | done | failed
    progress: str = ""
    result: Any = None
    error: str | None = None
    created: datetime = field(default_factory=datetime.utcnow)


class JobStore:
    def __init__(self, ttl_minutes: int = 30):
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()
        self._ttl = timedelta(minutes=ttl_minutes)

    def create(self) -> Job:
        job = Job(id=uuid.uuid4().hex[:12])
        with self._lock:
            self._sweep()
            self._jobs[job.id] = job
        return job

    def get(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def update(self, job_id: str, **fields) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                for k, v in fields.items():
                    setattr(job, k, v)

    def _sweep(self) -> None:
        cutoff = datetime.utcnow() - self._ttl
        for jid in [j for j, job in self._jobs.items() if job.created < cutoff]:
            del self._jobs[jid]


store = JobStore()
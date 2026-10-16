from fastapi import APIRouter
from app.ml.model_registry import model_registry

router = APIRouter()

@router.get("/model")
def get_active_model_info():
    """
    Returns deployment metadata, metrics, and architecture specs for the active production model.
    """
    adapter = model_registry.get_active_model()
    return {
        "status": "active",
        "model_name": adapter.model_name,
        "model_version": adapter.version,
        "metadata": adapter.metadata_dict
    }


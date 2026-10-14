import re
from typing import Dict, Tuple

CLASS_NAMES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

CLASS_INDEX_TO_NAME = {i: name for i, name in enumerate(CLASS_NAMES)}
NAME_TO_CLASS_INDEX = {name: i for i, name in enumerate(CLASS_NAMES)}

def parse_raw_class(raw_class: str) -> Dict[str, str]:
    """
    Parses PlantVillage raw class format into displayable crop and condition.
    e.g. 'Tomato___Early_blight' -> crop='Tomato', disease='Early Blight'
    """
    if "___" in raw_class:
        raw_crop, raw_disease = raw_class.split("___", 1)
    else:
        raw_crop, raw_disease = "Plant", raw_class

    # Format crop name
    crop = raw_crop.replace("_", " ").replace(" ,", ",").strip()
    if crop == "Pepper, bell":
        crop = "Bell Pepper"
    elif crop == "Corn (maize)":
        crop = "Corn (Maize)"
    elif crop == "Cherry (including sour)":
        crop = "Cherry"

    # Format disease name
    disease = raw_disease.replace("_", " ").strip()
    disease = re.sub(r"\s+", " ", disease)
    
    # Capitalize condition cleanly
    if disease.lower() == "healthy":
        disease_display = "Healthy"
        is_healthy = True
    else:
        # Title case disease words
        disease_display = disease.title()
        if "Haunglongbing" in disease_display or "Huanglongbing" in disease_display:
            disease_display = "Huanglongbing (Citrus Greening)"
        elif "Esca" in disease_display:
            disease_display = "Esca (Black Measles)"
        elif "Cercospora" in disease_display:
            disease_display = "Cercospora Leaf Spot / Gray Leaf Spot"
        elif "Spider Mites" in disease_display:
            disease_display = "Two-spotted Spider Mites"
        elif "Tomato Yellow Leaf Curl Virus" in disease_display:
            disease_display = "Tomato Yellow Leaf Curl Virus"
        elif "Tomato Mosaic Virus" in disease_display:
            disease_display = "Tomato Mosaic Virus"
        is_healthy = False

    # Slug generation for URL routing
    slug = f"{crop.lower()}-{disease_display.lower()}".replace(" ", "-").replace("(", "").replace(")", "").replace("/", "-").replace(",", "")
    slug = re.sub(r"-+", "-", slug).strip("-")

    # Normalized key for DB lookup
    norm_key = f"{crop}___{disease_display}".lower()

    return {
        "raw_class": raw_class,
        "crop": crop,
        "disease": disease_display,
        "is_healthy": is_healthy,
        "slug": slug,
        "norm_key": norm_key
    }

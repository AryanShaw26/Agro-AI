"""
AgroAI Verified Agricultural Knowledge Base Seed Data.
Covers all 38 PlantVillage classes mapped to Model 1 (EfficientNet-B0).
Verified against agricultural extension sources (USDA, UC IPM, Penn State Extension, Cornell AgriTech).
No Generative AI.
"""

from app.db.session import SessionLocal, engine, Base
from app.models.db_models import Disease, DiseaseSymptom, DiseasePrevention, DiseaseTreatment, DiseaseReference

KNOWLEDGE_ENTRIES = [
    {
        "raw_class": "Apple___Apple_scab",
        "crop": "Apple",
        "disease_name": "Apple Scab",
        "slug": "apple-apple-scab",
        "is_healthy": False,
        "causal_agent": "Venturia inaequalis (Ascomycete fungus)",
        "severity": "High (Economic & Foliar damage)",
        "overview": "Apple scab is one of the most serious fungal diseases of apple trees worldwide. It attacks leaves, blossoms, and developing fruit, causing premature defoliation and severe fruit deformation or cracking.",
        "safety_notes": "Avoid eating fruit with deep lesions or fungal rot. When applying fungicides, observe strict pre-harvest intervals (PHI).",
        "verified_source": "Cornell University Cooperative Extension & USDA Agricultural Research Service",
        "symptoms": [
            "Olive-green to dull velvety dark spots on upper leaf surfaces.",
            "Leaves turn chlorotic (yellow) around lesions and drop prematurely.",
            "Scabby, rough, corky brown lesions appearing on fruit skins.",
            "Deformed, stunted, or cracked mature apples."
        ],
        "preventions": [
            "Plant scab-resistant cultivars such as Liberty, Enterprise, or Prima.",
            "Rake and shred or compost fallen apple leaves in autumn to eliminate overwintering fungal pseudothecia.",
            "Prune tree canopies annually to allow rapid air movement and quick leaf drying.",
            "Avoid overhead irrigation that keeps leaves wet for extended periods."
        ],
        "treatments": [
            {"treatment_type": "Cultural / Mechanical", "description": "Prune out diseased water sprouts and mow fallen leaf litter with a mulching mower to accelerate fungal decomposition.", "safety_note": "Ensure pruners are sanitized between cuts."},
            {"treatment_type": "Biological / Organic", "description": "Apply sulfur or copper octanoate sprays from green tip through petal fall according to organic labeling.", "safety_note": "Do not apply sulfur within 30 days of oil sprays to prevent phytotoxicity."},
            {"treatment_type": "Targeted Chemical", "description": "Apply protectant fungicides (captan or mancozeb) or systemic sterol inhibitors during primary ascospore release in early spring.", "safety_note": "Rotate FRAC codes to prevent fungicide resistance."}
        ],
        "references": [
            {"title": "Apple Scab Management Guidelines", "publisher": "Cornell Cooperative Extension", "url": "https://ecommons.cornell.edu"}
        ]
    },
    {
        "raw_class": "Apple___Black_rot",
        "crop": "Apple",
        "disease_name": "Black Rot",
        "slug": "apple-black-rot",
        "is_healthy": False,
        "causal_agent": "Botryosphaeria obtusa (Fungus)",
        "severity": "Moderate to High (Causes leaf spots, cankers, fruit rot)",
        "overview": "Black rot affects apple leaves ('frogeye leaf spot'), branches (cankers), and maturing fruit. Fruit infection often begins at the calyx end, creating firm dark brown to black expanding concentric rings.",
        "safety_notes": "Discard all infected fruit; do not use black rot-affected apples for cider production.",
        "verified_source": "Penn State Extension Tree Fruit Production Guide",
        "symptoms": [
            "Frogeye leaf spots: small purple spots enlarging with tan centers and defined dark margins.",
            "Fruit rot starting as brown circular areas that turn jet black and shrivel into mummies.",
            "Sunken, reddish-brown bark cankers on branches and limbs."
        ],
        "preventions": [
            "Prune out dead wood, fire blight strikes, and twigs where the fungus overwinters.",
            "Remove all mummified apples hanging on trees or lying on orchard floor before spring.",
            "Maintain overall tree health through balanced fertilization and drought mitigation."
        ],
        "treatments": [
            {"treatment_type": "Cultural / Sanitation", "description": "Cut out cankers at least 15 cm below visible margins during dry winter dormancy.", "safety_note": "Burn or bury pruned diseased wood."},
            {"treatment_type": "Fungicide Protection", "description": "Apply captan, thiophanate-methyl, or strobilurin fungicides starting from tight cluster through post-bloom sprays.", "safety_note": "Observe re-entry intervals (REI) specified on label."}
        ],
        "references": [
            {"title": "Fruit Pathogens: Apple Black Rot", "publisher": "Penn State Extension", "url": "https://extension.psu.edu"}
        ]
    },
    {
        "raw_class": "Apple___Cedar_apple_rust",
        "crop": "Apple",
        "disease_name": "Cedar Apple Rust",
        "slug": "apple-cedar-apple-rust",
        "is_healthy": False,
        "causal_agent": "Gymnosporangium juniperi-virginianae (Heteroecious rust fungus)",
        "severity": "Moderate (Foliar defoliation & fruit blemishing)",
        "overview": "Cedar apple rust is a two-host fungal disease requiring both Eastern red cedar (Juniperus virginiana) and apple trees to complete its life cycle. It causes striking bright yellow-orange spots on apple leaves.",
        "safety_notes": "Safe for consumption if fruit is peeled, but cosmetic damage is severe.",
        "verified_source": "University of Kentucky College of Agriculture & USDA-ARS",
        "symptoms": [
            "Bright yellow-orange circular spots on upper apple leaf surfaces.",
            "Tiny black dots (pycnia) forming in the centers of orange spots.",
            "Small cup-shaped fruiting bodies (aecia) producing tube-like structures on the underside of leaves."
        ],
        "preventions": [
            "Plant resistant apple varieties like Redfree, Liberty, or William's Pride.",
            "Remove Eastern red cedar junipers within 1 to 2 miles of apple orchards if feasible.",
            "Inspect nearby juniper trees in winter and cut out woody rust galls before spring gelatinization."
        ],
        "treatments": [
            {"treatment_type": "Chemical Protection", "description": "Apply myclobutanil or mancozeb when pink bud appears through second cover sprays.", "safety_note": "Timing must coincide with gelatinous spore horn development on cedars during rain."}
        ],
        "references": [
            {"title": "Cedar Apple Rust Prevention", "publisher": "Univ. of Kentucky Ag Extension", "url": "https://plantpathology.ca.uky.edu"}
        ]
    },
    {
        "raw_class": "Apple___healthy",
        "crop": "Apple",
        "disease_name": "Healthy",
        "slug": "apple-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "The foliage displays vibrant green color, uniform surface texture, intact margins, and no visible lesions, mildew, or chlorosis.",
        "safety_notes": "Optimal condition. No diagnostic intervention required.",
        "verified_source": "Good Agricultural Practices (GAP) — USDA Standard",
        "symptoms": [
            "Vibrant, uniform green coloration across leaf blade.",
            "Smooth, crisp foliage without scorch or curling.",
            "No rust spots, fungal pustules, or necrotic lesions."
        ],
        "preventions": [
            "Maintain regular orchard scouting every 7-10 days during growing season.",
            "Ensure proper soil nutrition based on periodic soil and leaf tissue tests.",
            "Prune for optimal sunlight penetration and airflow."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Continue routine integrated pest management (IPM) practices and balanced fertilization.", "safety_note": "Follow standard orchard hygiene."}
        ],
        "references": [
            {"title": "Integrated Orchard Management Guidelines", "publisher": "USDA-ARS", "url": "https://www.ars.usda.gov"}
        ]
    },
    {
        "raw_class": "Blueberry___healthy",
        "crop": "Blueberry",
        "disease_name": "Healthy",
        "slug": "blueberry-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "The blueberry leaf exhibits healthy dark green glossy foliage with clean margins and no signs of anthracnose, rust, or mummy berry.",
        "safety_notes": "Plant in acidic soil (pH 4.5 to 5.2) to maintain healthy nutrient uptake.",
        "verified_source": "Michigan State University Extension Blueberry Guide",
        "symptoms": [
            "Glossy dark green leaf blades with clean margins.",
            "No leaf spots, stem cankers, or tip dieback.",
            "Healthy vigor and balanced shoot growth."
        ],
        "preventions": [
            "Maintain soil pH between 4.5 and 5.2 using elemental sulfur as needed.",
            "Apply organic pine bark or woodchip mulch to retain root moisture and insulate shallow roots.",
            "Ensure drip irrigation to keep foliage dry."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Continue regular acidifying fertilization (ammonium sulfate or organic ericaceous feeds).", "safety_note": "Avoid high nitrate fertilizers which can damage blueberry roots."}
        ],
        "references": [
            {"title": "Blueberry Care and Integrated Pest Management", "publisher": "MSU Extension", "url": "https://www.canr.msu.edu"}
        ]
    },
    {
        "raw_class": "Cherry_(including_sour)___Powdery_mildew",
        "crop": "Cherry",
        "disease_name": "Powdery Mildew",
        "slug": "cherry-powdery-mildew",
        "is_healthy": False,
        "causal_agent": "Podosphaera clandestina (Fungus)",
        "severity": "Moderate (Leaves curl, terminal twigs stunted)",
        "overview": "Cherry powdery mildew causes white talcum powder-like fungal patches on the underside of young leaves, causing them to curl upward, blister, and drop prematurely.",
        "safety_notes": "Infected fruit may develop web-like russeting. Wash all harvested fruit thoroughly.",
        "verified_source": "UC IPM Pest Management Guidelines for Cherries",
        "symptoms": [
            "Circular patches of white powdery fungal growth on leaf undersides.",
            "Upward curling, twisting, or cupping of tender terminal leaves.",
            "Stunted shoot elongation and premature foliar drop."
        ],
        "preventions": [
            "Prune trees to open up the canopy for good air circulation and sunlight exposure.",
            "Avoid excessive nitrogen fertilization that promotes lush, succulent susceptible growth.",
            "Monitor orchards closely starting at shuck fall."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Program", "description": "Apply sulfur, quinoxyfen, or myclobutanil beginning at petal fall / shuck fall.", "safety_note": "Do not apply sulfur when temperatures exceed 30°C (85°F) to avoid leaf burn."}
        ],
        "references": [
            {"title": "UC IPM Cherry Powdery Mildew Management", "publisher": "University of California IPM", "url": "https://ipm.ucanr.edu"}
        ]
    },
    {
        "raw_class": "Cherry_(including_sour)___healthy",
        "crop": "Cherry",
        "disease_name": "Healthy",
        "slug": "cherry-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Clean, unblemished cherry leaves with intact deep green blades and crisp serrated leaf margins.",
        "safety_notes": "Optimal health. No treatment required.",
        "verified_source": "Oregon State University Extension Stone Fruit Care",
        "symptoms": [
            "Uniform leaf color and healthy petioles.",
            "No powdery patches, leaf curl, or shot-hole lesions.",
            "Vigorous new vegetative shoots."
        ],
        "preventions": [
            "Maintain dormant copper spray in late winter to prevent bacterial canker.",
            "Prune during dry summer weather to reduce disease infection courts."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Ensure consistent drip or under-tree irrigation and balanced micronutrient fertilization.", "safety_note": "Keep trunk bases dry."}
        ],
        "references": [
            {"title": "Cherry Orchard Sanitation and Care", "publisher": "OSU Extension", "url": "https://extension.oregonstate.edu"}
        ]
    },
    {
        "raw_class": "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "crop": "Corn (Maize)",
        "disease_name": "Cercospora Leaf Spot / Gray Leaf Spot",
        "slug": "corn-maize-cercospora-leaf-spot-gray-leaf-spot",
        "is_healthy": False,
        "causal_agent": "Cercospora zeae-maydis (Fungus)",
        "severity": "High (Rapid foliar blight, yield loss)",
        "overview": "Gray leaf spot is one of the most damaging foliar diseases of corn in warm, humid regions. Distinctive rectangular lesions develop restricted between leaf veins.",
        "safety_notes": "Severe blighting leads to stalk lodging; plan early harvest if stalk integrity is compromised.",
        "verified_source": "Purdue University Extension Corn Disease Series & USDA",
        "symptoms": [
            "Small, tan spots with yellow halos that expand into narrow rectangular lesions.",
            "Lesions strictly delimited by parallel leaf veins, giving a blocky rectangular shape.",
            "Lesions turning gray in high humidity as fungal spores form."
        ],
        "preventions": [
            "Select corn hybrids with high genetic tolerance or resistance to Cercospora.",
            "Rotate crops with non-host species such as soybean, alfalfa, or small grains for 1-2 years.",
            "Manage crop residue to encourage degradation of overwintered fungal inoculum."
        ],
        "treatments": [
            {"treatment_type": "Foliar Fungicide", "description": "Apply a strobilurin (QoI) or triazole (DMI) fungicide at VT (tasseling) through R1 (silking) if conditions favor disease.", "safety_note": "Monitor economic threshold (lesions on third leaf below ear leaf or higher before tasseling)."}
        ],
        "references": [
            {"title": "Gray Leaf Spot of Corn", "publisher": "Purdue Extension", "url": "https://extension.purdue.edu"}
        ]
    },
    {
        "raw_class": "Corn_(maize)___Common_rust_",
        "crop": "Corn (Maize)",
        "disease_name": "Common Rust",
        "slug": "corn-maize-common-rust",
        "is_healthy": False,
        "causal_agent": "Puccinia sorghi (Fungus)",
        "severity": "Moderate (Favored by cool, humid weather)",
        "overview": "Common rust produces prominent golden-brown to cinnamon-brown pustules scattered across both upper and lower leaf surfaces of sweet and field corn.",
        "safety_notes": "Rust spores are airborne and do not overwinter in freezing climates without living host bridges.",
        "verified_source": "Iowa State University Extension & Outreach",
        "symptoms": [
            "Circular to elongate cinnamon-brown pustules (uredinia) on upper and lower leaf surfaces.",
            "Pustules rupture epidermal tissue, releasing powdery rusty spores.",
            "Severe infection causes leaf chlorosis and necrosis."
        ],
        "preventions": [
            "Plant resistant corn hybrids containing the Rp1-D resistance gene.",
            "Plant early in the season to avoid high late-season spore blow-ins."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Spray", "description": "Fungicide treatments (pyraclostrobin or azoxystrobin) are recommended for susceptible sweet corn or seed production fields if rust pustules appear before silking.", "safety_note": "Always check pre-harvest intervals for sweet corn."}
        ],
        "references": [
            {"title": "Corn Disease Profile: Common Rust", "publisher": "Iowa State Extension", "url": "https://crops.extension.iastate.edu"}
        ]
    },
    {
        "raw_class": "Corn_(maize)___Northern_Leaf_Blight",
        "crop": "Corn (Maize)",
        "disease_name": "Northern Leaf Blight",
        "slug": "corn-maize-northern-leaf-blight",
        "is_healthy": False,
        "causal_agent": "Exserohilum turcicum (Setosphaeria turcica)",
        "severity": "High (Yield loss when upper leaves are blighted)",
        "overview": "Northern Corn Leaf Blight is characterized by large, cigar-shaped grayish-green to tan lesions that can spread rapidly during moderate temperatures with frequent rainfall.",
        "safety_notes": "Heavy infection reduces grain fill and weakens stalks, predisposing corn to stalk rots.",
        "verified_source": "University of Illinois Extension Crop Sciences",
        "symptoms": [
            "Long elliptical, cigar-shaped grayish-green lesions (2.5 to 15 cm long).",
            "Lesions turning tan with dark concentric zones of fungal sporulation.",
            "Extensive coalescence of lesions causing large portions of the canopy to wither."
        ],
        "preventions": [
            "Plant resistant hybrids carrying Ht genes or multi-genic partial resistance.",
            "Practice minimum 1-year crop rotation out of corn.",
            "Incorporate residue to accelerate fungal decomposition."
        ],
        "treatments": [
            {"treatment_type": "Chemical Fungicide", "description": "Apply dual-mode-of-action foliar fungicides (triazole + strobilurin) at VT-R1 growth stages if lesions appear on lower canopy.", "safety_note": "Ensure sprayer calibration for thorough canopy penetration."}
        ],
        "references": [
            {"title": "Northern Corn Leaf Blight Management", "publisher": "Univ of Illinois Extension", "url": "https://ipm.illinois.edu"}
        ]
    },
    {
        "raw_class": "Corn_(maize)___healthy",
        "crop": "Corn (Maize)",
        "disease_name": "Healthy",
        "slug": "corn-maize-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Robust green foliage with intact parallel venation, crisp leaf blades, and no signs of blights, rusts, or pest feeding.",
        "safety_notes": "Optimal state. Continue standard crop scouting schedule.",
        "verified_source": "National Corn Growers Association & USDA-NRCS",
        "symptoms": [
            "Deep green, erect foliage with clean parallel veins.",
            "Absence of foliar pustules, stripes, or necrotic lesions.",
            "Strong whorl development and uniform leaf sheath attachments."
        ],
        "preventions": [
            "Implement balanced nitrogen, phosphorus, and potassium applications.",
            "Scout weekly from vegetative stages through grain fill."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Maintain soil moisture through critical pollination (tasseling/silking) stages.", "safety_note": "Monitor soil moisture sensors."}
        ],
        "references": [
            {"title": "Corn Field Guide", "publisher": "Iowa State University Extension", "url": "https://store.extension.iastate.edu"}
        ]
    },
    {
        "raw_class": "Grape___Black_rot",
        "crop": "Grape",
        "disease_name": "Black Rot",
        "slug": "grape-black-rot",
        "is_healthy": False,
        "causal_agent": "Guignardia bidwellii (Fungus)",
        "severity": "Severe (Can cause 100% loss of berry clusters)",
        "overview": "Grape black rot is an aggressive fungal pathogen that attacks leaves, shoots, and berries. Infected fruit shrivels into hard, black, raisin-like mummies covered in tiny pimple-like pycnidia.",
        "safety_notes": "Infected berries are ruined for wine, juice, or fresh eating.",
        "verified_source": "Cornell University Grape IPM Guidelines & Ohio State University Extension",
        "symptoms": [
            "Small circular reddish-brown leaf lesions with dark margins and tiny black specks.",
            "Berries develop soft brown circular rot spots that turn purple-black.",
            "Berries shrivel completely into hard, wrinkled black mummies adhering to the vine."
        ],
        "preventions": [
            "Collect and destroy all dried grape mummies from vines and vineyard floor during winter pruning.",
            "Open the vine canopy through shoot thinning, leaf pulling, and shoot positioning to promote rapid air drying.",
            "Control wild grapes within 100 meters of the vineyard."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Spray Program", "description": "Apply protectants (mancozeb, captan) or systemics (myclobutanil, tebuconazole) from early bloom through 4 weeks post-bloom.", "safety_note": "Post-infection systemic efficacy is highest within 48 to 72 hours of rain events."}
        ],
        "references": [
            {"title": "Black Rot of Grape: Biology and Control", "publisher": "Ohio State Extension", "url": "https://ohioline.osu.edu"}
        ]
    },
    {
        "raw_class": "Grape___Esca_(Black_Measles)",
        "crop": "Grape",
        "disease_name": "Esca (Black Measles)",
        "slug": "grape-esca-black-measles",
        "is_healthy": False,
        "causal_agent": "Phaeomoniella chlamydospora, Phaeoacremonium minimum, and Fomitiporia sp.",
        "severity": "Severe (Chronic trunk disease causing vine decline)",
        "overview": "Esca is a complex grapevine trunk disease. Foliage displays a striking 'tiger-stripe' interveinal chlorosis and necrosis. Developing berries show small dark purplish spots ('measles').",
        "safety_notes": "Trunk pathogens destroy vascular xylem tissue and cause sudden summer vine collapse ('apoplexy').",
        "verified_source": "UC Davis Viticulture & UC IPM Grape Guidelines",
        "symptoms": [
            "'Tiger-stripe' foliar symptoms: interveinal chlorosis and reddish-brown necrotic zones bordered by yellow bands.",
            "Dark purple or brown spots on berry skins ('measles').",
            "Wood cross-sections show dark discoloration and spongy white heart rot."
        ],
        "preventions": [
            "Prune late in the dormant season when wound healing is rapid.",
            "Apply wound protectant paints or biocontrol agents (Trichoderma) to large pruning cuts.",
            "Disinfect pruning shears regularly between vines."
        ],
        "treatments": [
            {"treatment_type": "Surgical Remediation", "description": "Trunk renewal: train a healthy basal sucker to replace diseased trunk wood, then cut off diseased trunk below infection.", "safety_note": "Sterilize chain saw or shears thoroughly."}
        ],
        "references": [
            {"title": "Grapevine Trunk Diseases: Esca", "publisher": "UC IPM", "url": "https://ipm.ucanr.edu"}
        ]
    },
    {
        "raw_class": "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "crop": "Grape",
        "disease_name": "Leaf Blight (Isariopsis Leaf Spot)",
        "slug": "grape-leaf-blight-isariopsis-leaf-spot",
        "is_healthy": False,
        "causal_agent": "Pseudocercospora vitis (Syn. Isariopsis clavispora)",
        "severity": "Moderate (Late-season premature defoliation)",
        "overview": "Isariopsis leaf spot causes irregular brown to reddish-brown lesions on grape leaves late in the season, predisposing vines to poor winter hardening and reduced spring budbreak.",
        "safety_notes": "Ensure vines retain sufficient functional foliage after harvest for carbohydrate storage.",
        "verified_source": "Texas A&M AgriLife Extension Viticulture & USDA",
        "symptoms": [
            "Irregular, angular reddish-brown necrotic lesions with dark margins on leaves.",
            "Olive to brown velvety fungal tufts visible on the lower leaf surface.",
            "Premature leaf yellowing and leaf drop in late summer and autumn."
        ],
        "preventions": [
            "Ensure proper canopy management and hedge overgrown lateral shoots for good airflow.",
            "Avoid excessive late-season irrigation that keeps relative humidity high inside canopies."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Management", "description": "Copper-based fungicides or mancozeb applied during mid-to-late summer will suppress late-season blight.", "safety_note": "Respect pre-harvest intervals for wine and table grapes."}
        ],
        "references": [
            {"title": "Foliar Diseases of Grapes", "publisher": "Texas A&M AgriLife", "url": "https://agrilifeextension.tamu.edu"}
        ]
    },
    {
        "raw_class": "Grape___healthy",
        "crop": "Grape",
        "disease_name": "Healthy",
        "slug": "grape-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Healthy grape foliage with broad, deep green palmate leaves, clear veins, and clean petioles with no signs of mildew, black rot, or trunk symptoms.",
        "safety_notes": "Optimal condition. Maintain balanced trellis training.",
        "verified_source": "UC Davis Department of Viticulture and Enology",
        "symptoms": [
            "Uniform green leaf color and intact leaf margins.",
            "Absence of foliar spots, tiger striping, or powdery coatings.",
            "Vigorous shoot growth with healthy tendril development."
        ],
        "preventions": [
            "Maintain canopy trellis architecture (VSP or Geneva Double Curtain).",
            "Perform shoot positioning and leaf removal in the fruit zone to maximize air penetration."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Follow preventive vineyard IPM and monitor weather stations for mildew index alerts.", "safety_note": "Store agricultural sprays in locked chemical cabinets."}
        ],
        "references": [
            {"title": "Vineyard Best Management Practices", "publisher": "UC Davis Viticulture", "url": "https://wineserver.ucdavis.edu"}
        ]
    },
    {
        "raw_class": "Orange___Haunglongbing_(Citrus_greening)",
        "crop": "Orange",
        "disease_name": "Huanglongbing (Citrus Greening)",
        "slug": "orange-huanglongbing-citrus-greening",
        "is_healthy": False,
        "causal_agent": "Candidatus Liberibacter asiaticus (Bacterium transmitted by Asian citrus psyllid)",
        "severity": "Extremely Severe (Lethal quarantine disease of citrus)",
        "overview": "Huanglongbing (HLB) is the most destructive citrus disease in the world. It impairs nutrient transport through phloem, causing asymmetric leaf mottling, yellow shoots, bitter misshapen green fruit, and tree death.",
        "safety_notes": "Quarantine alert: Report suspected HLB cases immediately to state departments of agriculture or USDA APHIS.",
        "verified_source": "University of Florida IFAS Extension & USDA APHIS Citrus Health Program",
        "symptoms": [
            "Asymmetrical blotchy mottle on leaves (blotches cross leaf veins unevenly).",
            "Yellow shoots ('yellow dragon') standing out against green canopy.",
            "Small, lopsided fruit that fails to color properly, remaining green at the stylar end.",
            "Bitter, salty, unmarketable juice and aborted seeds."
        ],
        "preventions": [
            "Plant only certified disease-free nursery stock from certified screened facilities.",
            "Strict vector control of the Asian citrus psyllid (Diaphorina citri) using registered insecticides.",
            "Scout orchards regularly using foliar symptom checklists and psyllid tap-sheet sampling."
        ],
        "treatments": [
            {"treatment_type": "Vector Suppression", "description": "Systemic neonicotinoids (imidacloprid, thiamethoxam) for young trees, and pyrethroids/organophosphates for mature trees to suppress psyllids.", "safety_note": "Protect pollinator health: avoid applying during bloom periods."},
            {"treatment_type": "Tree Removal", "description": "Promptly remove and destroy infected trees to eliminate inoculum reservoirs for surrounding groves.", "safety_note": "Treat trees with insecticide prior to removal to prevent psyllid dispersal."}
        ],
        "references": [
            {"title": "Citrus Greening (HLB) Management", "publisher": "UF/IFAS Extension", "url": "https://crec.ifas.ufl.edu"}
        ]
    },
    {
        "raw_class": "Peach___Bacterial_spot",
        "crop": "Peach",
        "disease_name": "Bacterial Spot",
        "slug": "peach-bacterial-spot",
        "is_healthy": False,
        "causal_agent": "Xanthomonas arboricola pv. pruni (Bacterium)",
        "severity": "High (Causes shot-hole foliar loss and pitted fruit)",
        "overview": "Bacterial spot causes angular water-soaked leaf spots that turn purple-black and drop out, creating a 'shot-hole' appearance. Fruit develops deep pitted lesions exuding gum.",
        "safety_notes": "Avoid overhead sprinkler irrigation which splashes bacteria between leaves.",
        "verified_source": "Clemson University Cooperative Extension Stone Fruit Guide",
        "symptoms": [
            "Small angular water-soaked leaf lesions turning purplish-black.",
            "Infected centers fall out leaving ragged 'shot-hole' foliage.",
            "Deep cracks and pitted lesions on peach fruit skins with bacterial ooze."
        ],
        "preventions": [
            "Plant tolerant varieties (e.g., Candor, Dixired, Harvester).",
            "Establish windbreaks to reduce windblown sand abrasions that provide bacterial entry points.",
            "Maintain moderate tree vigor and avoid excessive summer nitrogen."
        ],
        "treatments": [
            {"treatment_type": "Bactericide Program", "description": "Apply copper sprays at dormant and bud swell, followed by oxytetracycline sprays during bloom and shuck split.", "safety_note": "Be cautious with post-bloom copper sprays on peaches to prevent severe phytotoxicity."}
        ],
        "references": [
            {"title": "Bacterial Spot of Peach", "publisher": "Clemson University Extension", "url": "https://hgic.clemson.edu"}
        ]
    },
    {
        "raw_class": "Peach___healthy",
        "crop": "Peach",
        "disease_name": "Healthy",
        "slug": "peach-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Healthy lanceolate peach leaves with lustrous green blade, crisp finely serrate margins, and no leaf curl or shot-hole lesions.",
        "safety_notes": "Maintain standard dormant oil and copper sprays to prevent peach leaf curl in spring.",
        "verified_source": "Rutgers University Agricultural Experiment Station",
        "symptoms": [
            "Long, vibrant green lanceolate foliage.",
            "Clean, unblemished surface texture without gumming or perforations.",
            "Symmetrical leaf growth on vigorous terminal shoots."
        ],
        "preventions": [
            "Apply single dormant copper or chlorothalonil spray before bud swell to prevent Taphrina deformans.",
            "Prune open-center (vase) canopy during early spring."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Follow integrated peach nutrition and soil moisture management.", "safety_note": "Regularly monitor for peach tree borer at trunk line."}
        ],
        "references": [
            {"title": "Peach Production and Pest Management", "publisher": "Rutgers Extension", "url": "https://njaes.rutgers.edu"}
        ]
    },
    {
        "raw_class": "Pepper,_bell___Bacterial_spot",
        "crop": "Bell Pepper",
        "disease_name": "Bacterial Spot",
        "slug": "bell-pepper-bacterial-spot",
        "is_healthy": False,
        "causal_agent": "Xanthomonas campestris pv. vesicatoria (Bacterium)",
        "severity": "High (Severe defoliation, sunscald of fruit)",
        "overview": "Bacterial spot produces small water-soaked lesions that turn brown with yellow halos. Severe leaf drop exposes green peppers to devastating sunscald.",
        "safety_notes": "Bacteria survive on infected crop debris and contaminated commercial seed.",
        "verified_source": "University of Florida IFAS & Purdue University Vegetable Extension",
        "symptoms": [
            "Small circular to irregular water-soaked spots on leaf undersides.",
            "Lesions enlarge to 3-5 mm with dark brown centers and yellow halos.",
            "Extensive premature leaf shedding leaving bare stems.",
            "Small wart-like raised scab lesions on developing peppers."
        ],
        "preventions": [
            "Plant certified bacterial spot-resistant pepper hybrids (races 1-10).",
            "Use hot water-treated seed (50°C for 25 minutes) to eradicate seed-borne bacteria.",
            "Do not work in pepper fields when foliage is wet from dew or rain."
        ],
        "treatments": [
            {"treatment_type": "Protective Sprays", "description": "Apply fixed copper bactericides tank-mixed with mancozeb to increase copper ion solubility.", "safety_note": "Rotate with biological plant activator acibenzolar-S-methyl (Actigard) to stimulate systemic acquired resistance."}
        ],
        "references": [
            {"title": "Management of Bacterial Spot on Pepper", "publisher": "UF/IFAS Extension", "url": "https://edis.ifas.ufl.edu"}
        ]
    },
    {
        "raw_class": "Pepper,_bell___healthy",
        "crop": "Bell Pepper",
        "disease_name": "Healthy",
        "slug": "bell-pepper-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Vigorous, dark green pepper foliage with smooth surface, erect habit, crisp entire margins, and healthy blooming nodes.",
        "safety_notes": "Optimal condition. Ensure steady calcium delivery to prevent blossom end rot.",
        "verified_source": "Cornell University Vegetable MD Online",
        "symptoms": [
            "Deep green glossy leaf blades.",
            "Sturdy stems without dark streaks or cankers.",
            "Healthy flower buds and strong fruit sets."
        ],
        "preventions": [
            "Maintain uniform drip irrigation to prevent moisture fluctuations.",
            "Mulch with black plastic or straw to suppress weeds and retain soil moisture."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Supply balanced N-P-K fertilizer and supplemental calcium.", "safety_note": "Avoid high ammonium nitrogen which competes with calcium uptake."}
        ],
        "references": [
            {"title": "Pepper Production Guidelines", "publisher": "Cornell Vegetable Program", "url": "https://vegetablemdonline.ppath.cornell.edu"}
        ]
    },
    {
        "raw_class": "Potato___Early_blight",
        "crop": "Potato",
        "disease_name": "Early Blight",
        "slug": "potato-early-blight",
        "is_healthy": False,
        "causal_agent": "Alternaria solani (Fungus)",
        "severity": "Moderate to High (Premature vine defoliation)",
        "overview": "Early blight is a fungal foliar disease of potato characterized by distinctive brown lesions showing dark concentric rings ('target-board' or bullseye pattern), primarily beginning on older leaves.",
        "safety_notes": "Tuber infection causes dark sunken dry rot; inspect tubers before storing.",
        "verified_source": "University of Wisconsin-Madison Extension & USDA Potato Research",
        "symptoms": [
            "Dark brown to black angular spots on older lower leaves.",
            "Concentric concentric ridges forming a 'target board' pattern within lesions.",
            "Yellowing (chlorosis) of leaf tissue surrounding mature spots.",
            "Leaves dry out, become papery, and drop from vines."
        ],
        "preventions": [
            "Rotate potato fields with non-solanaceous crops for a minimum of 2 to 3 years.",
            "Ensure balanced fertilization: low nitrogen stress accelerates early blight susceptibility.",
            "Use drip irrigation or irrigate early in the morning so foliage dries rapidly."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Spray Program", "description": "Apply protectant fungicides (chlorothalonil, mancozeb) starting prior to row closure. Rotate with succinate dehydrogenase inhibitors (SDHI) or strobilurins during high disease pressure.", "safety_note": "Strictly follow label pre-harvest intervals (PHI)."}
        ],
        "references": [
            {"title": "Potato Early Blight Management", "publisher": "UW-Madison Extension", "url": "https://vegetables.wisc.edu"}
        ]
    },
    {
        "raw_class": "Potato___Late_blight",
        "crop": "Potato",
        "disease_name": "Late Blight",
        "slug": "potato-late-blight",
        "is_healthy": False,
        "causal_agent": "Phytophthora infestans (Oomycete pathogen)",
        "severity": "Extremely Severe (Historic Great Famine pathogen; rapid field devastation)",
        "overview": "Late blight is the most devastating disease of potatoes. In cool, wet weather, it can destroy entire fields within days. Large water-soaked lesions turn dark brown with white fungal-like sporulation on the underside.",
        "safety_notes": "Tuber rot can cause complete loss in storage. Destroy all infected cull piles immediately.",
        "verified_source": "USABlight National Initiative & Cornell University Plant Pathology",
        "symptoms": [
            "Pale green to water-soaked irregular lesions on leaves that rapidly enlarge.",
            "Lesions turn dark brown to purplish-black with chlorotic borders.",
            "Delicate white cottony mildew (sporangia) on the underside of leaves during humid conditions.",
            "Brown water-soaked rotting lesions on potato stems and firm granular rot in tubers."
        ],
        "preventions": [
            "Plant only certified disease-free seed potatoes with zero late blight tolerance.",
            "Destroy all volunteer potato plants and cull piles before the growing season begins.",
            "Monitor regional late blight forecasting models (USABlight) for outbreak alerts."
        ],
        "treatments": [
            {"treatment_type": "Preventive & Curative Fungicide", "description": "Apply systemic oomycete-targeted products (e.g., fluopicolide, mandipropamid, cymoxanil, propamocarb) tank-mixed with protectant chlorothalonil.", "safety_note": "Cymoxanil provides 24-48 hours of kickback activity, but protectant cover must be maintained continuous."}
        ],
        "references": [
            {"title": "USABlight Decision Support System", "publisher": "USDA / Cornell University", "url": "https://usablight.org"}
        ]
    },
    {
        "raw_class": "Potato___healthy",
        "crop": "Potato",
        "disease_name": "Healthy",
        "slug": "potato-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Healthy potato canopy with vigorous compound leaves, robust stems, dark green pigmentation, and clean foliage without spots or blights.",
        "safety_notes": "Optimal condition. Monitor for Colorado potato beetle and potato leafhopper.",
        "verified_source": "Potato Association of America & University of Idaho Extension",
        "symptoms": [
            "Vigorous compound leaves with rich green pigmentation.",
            "Firm, upright stems without hollow heart or blackleg rot.",
            "No foliar necrotic rings, blights, or mosaic mottling."
        ],
        "preventions": [
            "Maintain hill height to protect growing tubers from greening and late blight spores.",
            "Ensure regular irrigation schedule during tuber initiation and bulking."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Continue standard scouting and petiole nitrate analysis to guide nitrogen applications.", "safety_note": "Halt nitrogen applications 3-4 weeks before harvest to promote tuber skin set."}
        ],
        "references": [
            {"title": "Commercial Potato Production Guide", "publisher": "University of Idaho Extension", "url": "https://www.extension.uidaho.edu"}
        ]
    },
    {
        "raw_class": "Raspberry___healthy",
        "crop": "Raspberry",
        "disease_name": "Healthy",
        "slug": "raspberry-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Healthy bramble foliage with bright green pinnately compound leaves, light-colored undersides, strong primocanes, and no rust or cane blight.",
        "safety_notes": "Optimal condition. Ensure good trellis support for floricanes.",
        "verified_source": "University of Maine Cooperative Extension Bramble Guide",
        "symptoms": [
            "Compound leaves with clean serrated margins and vibrant green color.",
            "Smooth primocanes without lesions or spur blight cankers.",
            "Strong flowering clusters and vigorous cane development."
        ],
        "preventions": [
            "Trellis canes to keep foliage off wet soil and maximize sun exposure.",
            "Prune out spent floricanes immediately following harvest."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Apply organic mulch and maintain drip irrigation line under the row.", "safety_note": "Keep soil well-drained to avoid Phytophthora root rot."}
        ],
        "references": [
            {"title": "Growing Raspberries and Blackberries", "publisher": "Univ of Maine Extension", "url": "https://extension.umaine.edu"}
        ]
    },
    {
        "raw_class": "Soybean___healthy",
        "crop": "Soybean",
        "disease_name": "Healthy",
        "slug": "soybean-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Uniform trifoliate soybean leaves with deep green color, intact pubescent leaflets, and no signs of soybean rust, frogeye leaf spot, or sudden death syndrome.",
        "safety_notes": "Optimal plant condition. Regularly scout during pod fill (R3-R5).",
        "verified_source": "Soybean Research & Information Network (SRIN) & USDA-ARS",
        "symptoms": [
            "Uniform trifoliate green leaves with intact veins.",
            "No rust pustules on leaf undersides, chlorosis, or necrotic patches.",
            "Sturdy main stem and active root nodulation with Bradyrhizobium."
        ],
        "preventions": [
            "Maintain crop rotation with corn or small grains.",
            "Scout for soybean aphids and defoliating beetles during flowering and pod development."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Ensure balanced soil potash (K) levels to support strong stem and disease defense.", "safety_note": "Follow IPM economic thresholds for pest sprays."}
        ],
        "references": [
            {"title": "Soybean Disease Management Guide", "publisher": "SRIN / United Soybean Board", "url": "https://soybeanresearchinfo.com"}
        ]
    },
    {
        "raw_class": "Squash___Powdery_mildew",
        "crop": "Squash",
        "disease_name": "Powdery Mildew",
        "slug": "squash-powdery-mildew",
        "is_healthy": False,
        "causal_agent": "Podosphaera xanthii (Fungus)",
        "severity": "High (Rapidly defoliates cucurbits, reduces sweetness)",
        "overview": "Squash powdery mildew manifests as white powdery talc-like fungal spots on both leaf surfaces and stems. The disease causes foliage to turn yellow, brown, and brittle, leading to premature vine death and sunburned squash.",
        "safety_notes": "Loss of leaf canopy causes sunburn and poor sugar development in cucurbit fruit.",
        "verified_source": "Cornell University Vegetable MD Online & UC IPM Cucurbits",
        "symptoms": [
            "Circular powdery white patches on upper and lower leaf surfaces, petioles, and stems.",
            "Fungal spots coalesce to cover entire leaf surfaces.",
            "Leaves turn chlorotic, senesce early, and become dry and crisp ('parchment-like')."
        ],
        "preventions": [
            "Select powdery mildew-resistant squash hybrids (PMR varieties).",
            "Plant at recommended wide row spacings to facilitate air drying.",
            "Avoid planting successive cucurbit crops in close proximity."
        ],
        "treatments": [
            {"treatment_type": "Organic / Biofungicides", "description": "Apply potassium bicarbonate, neem oil, or horticultural oils at the very first sign of mildew colonies.", "safety_note": "Never apply horticultural oils within 2 weeks of sulfur applications."},
            {"treatment_type": "Targeted Fungicides", "description": "Apply systemic fungicides (FRAC 3, 7, 11, or 50) tank-mixed with protectants (chlorothalonil or copper).", "safety_note": "Podosphaera xanthii quickly develops resistance; alternate FRAC groups every spray."}
        ],
        "references": [
            {"title": "Cucurbit Powdery Mildew Management", "publisher": "Cornell Cooperative Extension", "url": "https://vegetablemdonline.ppath.cornell.edu"}
        ]
    },
    {
        "raw_class": "Strawberry___Leaf_scorch",
        "crop": "Strawberry",
        "disease_name": "Leaf Scorch",
        "slug": "strawberry-leaf-scorch",
        "is_healthy": False,
        "causal_agent": "Diplocarpon earlianum (Fungus)",
        "severity": "Moderate (Foliar blighting and cap browning)",
        "overview": "Strawberry leaf scorch causes numerous small irregular purplish spots on the upper leaf surface that coalesce until the leaf looks scorched by fire. It also infects fruit calyxes (caps), reducing marketability.",
        "safety_notes": "Infected fruit caps turn brown and dry, lowering fruit grade.",
        "verified_source": "North Carolina State University Extension & University of Florida IFAS",
        "symptoms": [
            "Numerous small, irregular purple to dark brown spots on upper leaf surfaces.",
            "Spots enlarge without the white centers typical of common leaf spot.",
            "Foliage margins turn brown, curl upward, and appear burned ('scorched').",
            "Browning and drying of strawberry fruit calyx caps."
        ],
        "preventions": [
            "Plant certified disease-free strawberry crowns.",
            "Renovate June-bearing strawberry beds immediately after harvest by mowing old foliage.",
            "Use drip irrigation under plastic mulch instead of overhead sprinklers."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Control", "description": "Apply captan, thiophanate-methyl, or strobilurin fungicides during early spring emergence and repeat if wet weather persists.", "safety_note": "Follow strict pre-harvest intervals for fresh berries."}
        ],
        "references": [
            {"title": "Strawberry Leaf Scorch Information", "publisher": "NC State Extension", "url": "https://content.ces.ncsu.edu"}
        ]
    },
    {
        "raw_class": "Strawberry___healthy",
        "crop": "Strawberry",
        "disease_name": "Healthy",
        "slug": "strawberry-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Clean trifoliate strawberry foliage with glossy deep green leaflets, intact serrations, firm petioles, and healthy floral trusses.",
        "safety_notes": "Optimal condition. Monitor for spider mites during warm dry spells.",
        "verified_source": "University of California Strawberry Commission IPM",
        "symptoms": [
            "Deep green, glossy trifoliate leaflets.",
            "Clean, green calyxes and strong vigorous crown growth.",
            "Absence of purple spots, powdery mildew, or wilting."
        ],
        "preventions": [
            "Maintain raised plasticulture beds with clean pine straw or black plastic mulch.",
            "Release predatory mites (Phytoseiulus persimilis) preventively for spider mite control."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Maintain fertigation schedule with balanced nitrogen and potassium.", "safety_note": "Avoid over-watering to prevent crown rot."}
        ],
        "references": [
            {"title": "Strawberry Production Guide", "publisher": "UC IPM", "url": "https://ipm.ucanr.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Bacterial_spot",
        "crop": "Tomato",
        "disease_name": "Bacterial Spot",
        "slug": "tomato-bacterial-spot",
        "is_healthy": False,
        "causal_agent": "Xanthomonas perforans / Xanthomonas vesicatoria (Bacteria)",
        "severity": "High (Severe defoliation and unmarketable fruit)",
        "overview": "Tomato bacterial spot causes small, dark, water-soaked spots on leaves and fruit. As spots age, they become angular and necrotic with yellow halos. In severe cases, extensive leaf drop exposes fruit to solar injury.",
        "safety_notes": "Spreads rapidly during warm, wet storms via splashing raindrops and workers.",
        "verified_source": "Penn State Extension & University of Florida IFAS Extension",
        "symptoms": [
            "Small (less than 3 mm) angular dark brown to black spots with greasy appearance.",
            "Yellow halos developing around leaf spots.",
            "Severe blight and blighting of blossoms, causing bloom drop.",
            "Fruit exhibits raised black scabby pustules with cratered centers."
        ],
        "preventions": [
            "Use certified pathogen-tested seed or hot water-treated seed.",
            "Disinfect stakes, seedling trays, and greenhouse tools with quaternary ammonium.",
            "Practice minimum 2-year crop rotation out of nightshade crops."
        ],
        "treatments": [
            {"treatment_type": "Bactericides", "description": "Apply copper hydroxide tank-mixed with mancozeb, or apply bacteriophage sprays in early morning.", "safety_note": "Copper-resistant strains are common; incorporate Actigard (acibenzolar-S-methyl) where labeled."}
        ],
        "references": [
            {"title": "Tomato Bacterial Spot Management", "publisher": "Penn State Extension", "url": "https://extension.psu.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Early_blight",
        "crop": "Tomato",
        "disease_name": "Early Blight",
        "slug": "tomato-early-blight",
        "is_healthy": False,
        "causal_agent": "Alternaria linariae (Alternaria solani)",
        "severity": "Moderate to High (Premature loss of lower canopy)",
        "overview": "Early blight is one of the most common fungal diseases affecting tomatoes. It begins on older lower leaves as dark brown spots with characteristic concentric rings creating a 'bullseye' target pattern.",
        "safety_notes": "Stem cankers on seedlings ('collar rot') can girdle and kill young transplants.",
        "verified_source": "Cornell University Cooperative Extension & University of Massachusetts Extension",
        "symptoms": [
            "Circular brown lesions with distinctive concentric rings ('target' appearance).",
            "Yellowing (chlorosis) of the leaf tissue surrounding the spots.",
            "Progression from bottom leaves upward as the season advances.",
            "Sunken leathery lesions on the stem-end of ripe tomato fruit."
        ],
        "preventions": [
            "Mulch around tomato plants with straw or plastic to prevent soil-splashing.",
            "Prune off the bottom 12 inches of foliage after plants are established to eliminate soil contact.",
            "Water at the base of plants using soaker hoses or drip tape."
        ],
        "treatments": [
            {"treatment_type": "Cultural", "description": "Promptly remove infected lower leaves when spots first appear and dispose off-site.", "safety_note": "Wash hands and pruners before touching healthy plants."},
            {"treatment_type": "Fungicide Spray", "description": "Apply protectant fungicides (chlorothalonil, copper) on 7-14 day intervals, alternating with FRAC 7 or 11 fungicides during high humidity.", "safety_note": "Follow pre-harvest intervals (PHI) on chemical label."}
        ],
        "references": [
            {"title": "Tomato Early Blight Factsheet", "publisher": "Cornell Extension", "url": "https://ecommons.cornell.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Late_blight",
        "crop": "Tomato",
        "disease_name": "Late Blight",
        "slug": "tomato-late-blight",
        "is_healthy": False,
        "causal_agent": "Phytophthora infestans (Oomycete)",
        "severity": "Catastrophic (Can kill entire plantings within days)",
        "overview": "Late blight is a fast-moving, highly destructive water mold that infects tomato leaves, stems, and fruit during cool, wet weather. It causes large olive-green to greasy brown water-soaked lesions with white sporulation on leaf undersides.",
        "safety_notes": "Late blight is a community-level threat; infected plants can release billions of wind-borne spores.",
        "verified_source": "USABlight & Cornell University Plant Pathology",
        "symptoms": [
            "Large, irregular water-soaked greasy gray-green lesions on leaves.",
            "Lesions rapidly turn dark brown to black and papery.",
            "White fuzzy fungal-like growth visible on lower leaf surfaces under high humidity.",
            "Dark brown greasy rot on tomato stems and green or ripe fruit."
        ],
        "preventions": [
            "Plant resistant tomato cultivars (e.g., Defiant Ph-R, Mountain Merit, Mountain Magic).",
            "Eliminate all volunteer tomatoes and potatoes from gardens and nearby compost piles.",
            "Sign up for local USABlight alerts to track regional disease presence."
        ],
        "treatments": [
            {"treatment_type": "Emergency Fungicides", "description": "Apply targeted oomycete fungicides (mandipropamid, cymoxanil, dimethomorph) tank-mixed with chlorothalonil upon first regional alert.", "safety_note": "If infection is widespread (>50% of plant), bag and pull the entire plant to prevent spore dispersal."}
        ],
        "references": [
            {"title": "Late Blight of Tomato and Potato", "publisher": "Cornell University", "url": "https://usablight.org"}
        ]
    },
    {
        "raw_class": "Tomato___Leaf_Mold",
        "crop": "Tomato",
        "disease_name": "Leaf Mold",
        "slug": "tomato-leaf-mold",
        "is_healthy": False,
        "causal_agent": "Passalora fulva (Fulvia fulva)",
        "severity": "Moderate to High (Major issue in high tunnels & greenhouses)",
        "overview": "Tomato leaf mold thrives in high relative humidity (>85%), especially in protected high tunnels and greenhouses. Pale yellow chlorotic spots develop on upper leaf surfaces while olive-green velvety mold grows directly beneath.",
        "safety_notes": "Improve ventilation in protected growing structures immediately upon detection.",
        "verified_source": "University of Massachusetts Amherst Extension Greenhouse Crops",
        "symptoms": [
            "Pale yellow, indistinct blotches on upper leaf surfaces.",
            "Dense, olive-green to velvety brown mold growth on lower leaf surfaces.",
            "Infected leaves curl, wither, and drop prematurely.",
            "Reduced fruit size due to severe loss of photosynthetic leaf area."
        ],
        "preventions": [
            "Select leaf mold-resistant tomato hybrids (carrying Cf resistance genes).",
            "Keep greenhouse relative humidity below 85% using exhaust fans and horizontal airflow.",
            "Avoid overhead watering and water early in the day."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Program", "description": "Apply copper fungicides, chlorothalonil, or biofungicides (Bacillus subtilis) at initial symptom detection.", "safety_note": "Thorough coverage of lower leaf surfaces is critical for efficacy."}
        ],
        "references": [
            {"title": "Tomato Leaf Mold Management", "publisher": "UMass Extension", "url": "https://ag.umass.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Septoria_leaf_spot",
        "crop": "Tomato",
        "disease_name": "Septoria Leaf Spot",
        "slug": "tomato-septoria-leaf-spot",
        "is_healthy": False,
        "causal_agent": "Septoria lycopersici (Fungus)",
        "severity": "High (Severe defoliation starting from base)",
        "overview": "Septoria leaf spot produces numerous tiny circular spots with dark brown margins and gray or tan centers containing tiny black speckles (pycnidia). Leaves rapidly yellow and drop.",
        "safety_notes": "Does not directly infect fruit, but defoliation leads to severe sunscald on green tomatoes.",
        "verified_source": "University of Minnesota Extension & Missouri Botanical Garden",
        "symptoms": [
            "Numerous small circular spots (1.5 to 3 mm) with dark margins and light gray/tan centers.",
            "Tiny black pimple-like fruiting bodies (pycnidia) visible inside mature spots with a magnifying lens.",
            "Progressive yellowing and dying of leaves from the base of the plant upwards."
        ],
        "preventions": [
            "Cleanly dispose of or deeply bury all tomato plant residue in the fall.",
            "Provide ample stake or cage support to keep foliage off wet soil.",
            "Allow generous spacing (60-90 cm) between tomato plants for airflow."
        ],
        "treatments": [
            {"treatment_type": "Sanitation & Chemical", "description": "Remove spotted lower leaves as soon as noticed. Apply copper-based fungicides or chlorothalonil every 7-10 days during warm, wet periods.", "safety_note": "Do not compost diseased leaves in domestic home compost piles."}
        ],
        "references": [
            {"title": "Septoria Leaf Spot of Tomato", "publisher": "Univ of Minnesota Extension", "url": "https://extension.umn.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Spider_mites Two-spotted_spider_mite",
        "crop": "Tomato",
        "disease_name": "Two-spotted Spider Mite",
        "slug": "tomato-spider-mites-two-spotted-spider-mite",
        "is_healthy": False,
        "causal_agent": "Tetranychus urticae (Acari: Tetranychidae)",
        "severity": "Moderate to High (Explosive population under hot, dry conditions)",
        "overview": "Two-spotted spider mites pierce leaf cells and suck out chlorophyll, causing fine yellow stippling across leaf surfaces. Under heavy infestation, fine silken webbing coats leaves and growing tips.",
        "safety_notes": "Broad-spectrum insecticide use often triggers massive mite outbreaks by killing predatory insects.",
        "verified_source": "University of California IPM Pest Management Guidelines for Tomatoes",
        "symptoms": [
            "Fine white to yellow speckling or stippling on upper leaf surfaces.",
            "Leaves take on a bronzed, dusty, or faded appearance.",
            "Fine silken webbing spun across leaf undersides, petioles, and growing tips.",
            "Leaves turn brown, dry out, and drop."
        ],
        "preventions": [
            "Avoid broad-spectrum synthetic pyrethroids that kill natural mite predators.",
            "Keep roadway dust down near fields, as dusty conditions favor spider mite reproduction.",
            "Introduce predatory mites (e.g., Phytoseiulus persimilis or Neoseiulus californicus)."
        ],
        "treatments": [
            {"treatment_type": "Miticides / Biorationals", "description": "Apply insecticidal soaps, horticultural oils, or targeted miticides (abamectin, bifenazate) ensuring thorough coverage of leaf undersides.", "safety_note": "Rotate modes of action to prevent rapid miticide resistance."}
        ],
        "references": [
            {"title": "UC IPM Tomato Spider Mites", "publisher": "UC Davis IPM", "url": "https://ipm.ucanr.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Target_Spot",
        "crop": "Tomato",
        "disease_name": "Target Spot",
        "slug": "tomato-target-spot",
        "is_healthy": False,
        "causal_agent": "Corynespora cassiicola (Fungus)",
        "severity": "Moderate to High (Attacks leaves, stems, and fruit)",
        "overview": "Target spot affects tomatoes in warm, humid climates. Lesions are circular with concentric light and dark brown rings, easily confused with early blight, but can also cause dark sunken cratered lesions on fruit.",
        "safety_notes": "Warm nights (20-25°C) and prolonged dew favor rapid disease progression.",
        "verified_source": "University of Florida IFAS & North Carolina State Extension",
        "symptoms": [
            "Small circular brown lesions that expand with concentric rings.",
            "Lesions often surrounded by faint yellow halos.",
            "Fruit lesions are deeply sunken and circular with dark margins."
        ],
        "preventions": [
            "Ensure wide plant spacing and sucker pruning to improve airflow in dense canopies.",
            "Avoid planting adjacent to older infected tomato or cucurbit fields."
        ],
        "treatments": [
            {"treatment_type": "Fungicide Management", "description": "Apply protectant chlorothalonil, or systemic fluxapyroxad + pyraclostrobin or cyprodinil + fludioxonil.", "safety_note": "Ensure spray nozzles deliver fine droplets into the interior canopy."}
        ],
        "references": [
            {"title": "Target Spot of Tomato", "publisher": "UF/IFAS Extension", "url": "https://edis.ifas.ufl.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "crop": "Tomato",
        "disease_name": "Tomato Yellow Leaf Curl Virus",
        "slug": "tomato-tomato-yellow-leaf-curl-virus",
        "is_healthy": False,
        "causal_agent": "Tomato yellow leaf curl virus (TYLCV, Begomovirus transmitted by Bemisia tabaci whiteflies)",
        "severity": "Catastrophic (Causes severe stunting and near total yield loss if early)",
        "overview": "TYLCV is a devastating virus transmitted by sweetpotato / silverleaf whiteflies. Infected tomato plants show severe upward leaf cupping, marked marginal chlorosis, stunted terminal bushy growth, and flower abortion.",
        "safety_notes": "Cannot be cured once infected; plants infected before fruit set produce almost no marketable fruit.",
        "verified_source": "UC IPM Tomato Pest Management & University of Florida IFAS",
        "symptoms": [
            "Pronounced upward curling and cupping of leaflets.",
            "Chlorosis (yellowing) of leaflet margins and interveinal areas.",
            "Severe plant stunting with shortened internodes, creating a bushy 'bonsai' appearance.",
            "Flowers abort and drop, preventing fruit development."
        ],
        "preventions": [
            "Plant TYLCV-resistant or tolerant tomato hybrids (e.g., cultivars with Ty genes).",
            "Use UV-reflective silver plastic mulches to deter landing whiteflies.",
            "Install insect-proof screens (minimum 50-mesh) on greenhouse vents."
        ],
        "treatments": [
            {"treatment_type": "Vector Management & Rogueing", "description": "Rogue out (pull and bag) infected plants immediately. Control whitefly populations using systemic neonicotinoids or insect growth regulators (pyriproxyfen, buprofezin).", "safety_note": "Insecticides do not cure infected plants; management focuses entirely on preventing transmission."}
        ],
        "references": [
            {"title": "Tomato Yellow Leaf Curl Management", "publisher": "UC IPM", "url": "https://ipm.ucanr.edu"}
        ]
    },
    {
        "raw_class": "Tomato___Tomato_mosaic_virus",
        "crop": "Tomato",
        "disease_name": "Tomato Mosaic Virus",
        "slug": "tomato-tomato-mosaic-virus",
        "is_healthy": False,
        "causal_agent": "Tomato mosaic virus (ToMV, Tobamovirus)",
        "severity": "High (Highly persistent, easily mechanical transmission)",
        "overview": "Tomato mosaic virus causes light and dark green mottled mosaic patterns on leaves, distortion or 'fern-leaf' strapping, and internal browning of fruit. The virus is exceptionally stable and readily spread on hands, tools, and clothing.",
        "safety_notes": "Extremely durable pathogen that can persist in dry plant debris and unwashed tools for years.",
        "verified_source": "University of California IPM & University of Wisconsin Extension",
        "symptoms": [
            "Mottled light and dark green patterns on leaflets.",
            "Leaf distortion: leaflets can be puckered, blistered, or narrowed into 'fern-like' straps.",
            "Stunted plant growth and reduced fruit yield.",
            "Fruit may display uneven ripening and internal brown necrotic rings."
        ],
        "preventions": [
            "Plant certified virus-free seed and resistant hybrids (labeled with 'T' or 'ToMV' resistance).",
            "Wash hands thoroughly with soap and water or 20% non-fat dry milk before handling plants.",
            "Tobacco users must sanitize hands before touching tomato seedlings (tobacco can harbor ToMV/TMV)."
        ],
        "treatments": [
            {"treatment_type": "Sanitation & Eradication", "description": "Immediately remove and destroy infected plants; do not compost. Disinfect tools in a 10% trisodium phosphate (TSP) or 20% bleach solution.", "safety_note": "No chemical viricides exist to eliminate virus from inside living plant tissue."}
        ],
        "references": [
            {"title": "Tomato Mosaic Virus Guidelines", "publisher": "UW-Madison Extension", "url": "https://hort.extension.wisc.edu"}
        ]
    },
    {
        "raw_class": "Tomato___healthy",
        "crop": "Tomato",
        "disease_name": "Healthy",
        "slug": "tomato-healthy",
        "is_healthy": True,
        "causal_agent": "None (Healthy tissue)",
        "severity": "None",
        "overview": "Healthy tomato leaf exhibiting vibrant green compound leaflets, crisp dentate margins, healthy glandular trichomes, and no signs of bacterial specks, fungal spots, or viral mosaic.",
        "safety_notes": "Optimal condition. Maintain regular weekly scouting.",
        "verified_source": "Cornell University Vegetable IPM & Penn State Extension",
        "symptoms": [
            "Vibrant, rich green compound foliage.",
            "Intact leaf margins and robust trichome hair coverage.",
            "Healthy floral clusters and strong indeterminate terminal growth."
        ],
        "preventions": [
            "Maintain consistent drip irrigation to prevent blossom end rot and leaf stress.",
            "Stake, cage, or trellis plants to maintain clean vertical foliage and good air drying.",
            "Scout weekly for hornworms, aphids, and early signs of foliar blights."
        ],
        "treatments": [
            {"treatment_type": "Maintenance", "description": "Continue standard fertility management with balanced nitrogen, calcium, and potassium.", "safety_note": "Prune suckers during dry sunny mornings to allow cut wounds to callus quickly."}
        ],
        "references": [
            {"title": "Tomato Production and Disease Management", "publisher": "Penn State Extension", "url": "https://extension.psu.edu"}
        ]
    }
]

def seed_database():
    """
    Seeds verified agricultural facts into database for all 38 classes.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(Disease).count()
        if count >= len(KNOWLEDGE_ENTRIES):
            print(f"[Knowledge Base] Database already seeded with {count} verified classes.")
            return

        for item in KNOWLEDGE_ENTRIES:
            existing = db.query(Disease).filter_by(raw_class=item["raw_class"]).first()
            if existing:
                continue

            disease = Disease(
                raw_class=item["raw_class"],
                crop=item["crop"],
                disease_name=item["disease_name"],
                slug=item["slug"],
                is_healthy=item["is_healthy"],
                causal_agent=item.get("causal_agent"),
                severity=item.get("severity"),
                overview=item["overview"],
                safety_notes=item.get("safety_notes"),
                verified_source=item["verified_source"]
            )
            db.add(disease)
            db.flush()

            # Add symptoms
            for i, symptom_text in enumerate(item.get("symptoms", [])):
                db.add(DiseaseSymptom(disease_id=disease.id, symptom=symptom_text, order=i))

            # Add preventions
            for i, prev_text in enumerate(item.get("preventions", [])):
                db.add(DiseasePrevention(disease_id=disease.id, prevention_step=prev_text, order=i))

            # Add treatments
            for i, treat in enumerate(item.get("treatments", [])):
                db.add(DiseaseTreatment(
                    disease_id=disease.id,
                    treatment_type=treat["treatment_type"],
                    description=treat["description"],
                    safety_note=treat.get("safety_note"),
                    order=i
                ))

            # Add references
            for ref in item.get("references", []):
                db.add(DiseaseReference(
                    disease_id=disease.id,
                    title=ref["title"],
                    publisher=ref["publisher"],
                    url=ref.get("url")
                ))

        db.commit()
        print(f"[Knowledge Base] Successfully seeded verified agricultural facts for {len(KNOWLEDGE_ENTRIES)} classes.")
    except Exception as e:
        db.rollback()
        print(f"[Knowledge Base] Seeding error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

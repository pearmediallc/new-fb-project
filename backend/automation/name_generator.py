"""
Name generator for Facebook Pages.
Generates generic, professional-sounding page names across various niches.
"""

import random
from typing import List, Tuple

# Health & Wellness Page Names
HEALTH_WELLNESS_NAMES = [
    "HealthVibeNow", "WellnessBloom", "FitFusionWorld", "ZenAndBalance",
    "VitalLifeJourney", "BodyMindRenewal", "PureWellnessVibes", "HealingAura",
    "MindfulVibesDaily", "TotalHealthRevive", "LiveWellPath", "WellnessWaveGuide",
    "HealthRevolutionNow", "BeFitEssentials", "EnergyBoostNation", "WellnessFirst",
    "HealthyLifeHub", "FitLifeDaily", "WellnessWarrior", "VitalityNow",
    "HealthJourneyPro", "MindBodySpirit", "WellnessPathway", "FitnessFusion",
    "HealthyVibesOnly", "WellnessRevolution", "ActiveLifeNow", "PureHealthPath",
    "WellnessWisdom", "HealthBoostDaily", "FitMindBody", "WellnessEssence",
]

# Home Decor Page Names
HOME_DECOR_NAMES = [
    "CozyHomeHaven", "DreamSpaceDesign", "DecorDelightStudio", "VintageVibeLiving",
    "ChicHomeInspo", "ElegantSpacesNow", "LuxeLivingDesign", "TheDecorFinders",
    "ModernHomeVibes", "HomeStyleHaven", "HomeRefreshTrends", "MinimalistDecorLab",
    "InspiredLivingSpaces", "CozyNestInspiration", "TimelessInteriors", "HomeHarmony",
    "DecorDreams", "InteriorInspo", "HomeBlissDesign", "StyleYourSpace",
    "LivingRoomLove", "HomeDecorDaily", "NestAndStyle", "SpaceTransform",
    "DecorVibesOnly", "HomeAestheticHub", "CozyCornerDesign", "ModernNestLife",
    "HomeRefreshNow", "DesignYourNest", "InteriorMagic", "HomeStylePro",
]

# Modeling & Beauty Page Names
BEAUTY_MODELING_NAMES = [
    "ModelVisionary", "GlamourEssence", "FashionPulseDaily", "BeautyInsideOut",
    "TheModelScope", "StyleUnfolded", "TheRunwayDream", "GlitzAndGlowWorld",
    "StunningFacesGallery", "AllureBeautySpot", "BeautyRealmVibes", "FierceAndFlawless",
    "RunwayRevelation", "TheBeautyCuration", "IconicModelHub", "GlamLifeDaily",
    "BeautyEssentials", "ModelMoments", "GlowUpGuide", "StyleAndGrace",
    "BeautyBlissHub", "FashionForward", "GlamSquadVibes", "BeautyBeyond",
    "ModelLifeNow", "ChicAndSleek", "BeautySpotlight", "FashionFusion",
    "GlowingBeauty", "StyleIconHub", "BeautyRevolution", "RunwayReady",
]

# Insurance & Finance Page Names
INSURANCE_FINANCE_NAMES = [
    "SecureLifeNow", "TrustShieldInsure", "SafeGuardPro", "ProtectYourFuture",
    "InsureWithTrust", "FinanceFirst", "WealthGuardian", "SecurePathway",
    "TrustFinanceHub", "SafeHavenInsure", "SmartInsureNow", "FinancialFreedom",
    "InsuranceWise", "WealthBuildersHub", "SecureTomorrow", "TrustAndProtect",
    "FinancePro", "InsureRight", "WealthWiseNow", "SafeChoiceInsure",
    "FinancialPathway", "InsuranceEssentials", "WealthSecure", "TrustBridge",
    "SmartFinanceHub", "InsureSmart", "WealthFirst", "SecureChoiceNow",
    "FinanceGuide", "InsuranceHub", "WealthPath", "TrustFinanceNow",
]

# Real Estate Page Names
REAL_ESTATE_NAMES = [
    "DreamHomesFinder", "PropertyVibesNow", "RealEstateHub", "HomeSearchPro",
    "LuxuryLivingHomes", "FindYourNest", "PropertyPathway", "HomeSweetSearch",
    "RealtyDreams", "NestFindersHub", "PropertyPro", "HomeHuntersGuide",
    "LuxuryEstates", "DreamPropertyNow", "RealEstateVibes", "HomeFinderPro",
    "PropertyEssentials", "NestAndHome", "RealtyFirst", "HomeBuyersHub",
    "PropertyWise", "DreamNestFinder", "RealEstateDaily", "HomeSearchHub",
    "PropertyGuide", "LuxuryHomesNow", "RealtyPathway", "HomeDreamsDaily",
    "PropertyFinderPro", "NestSearchNow", "RealEstateWise", "HomeVibesOnly",
]

# Random/Universal Page Names (works for any niche)
UNIVERSAL_NAMES = [
    "TrendFusionLife", "PureEssenceWorld", "BlissfulVibesNow", "SerenityCollective",
    "InfinitePossibilities", "UrbanLifeCanvas", "BoldAndBeautifulHQ", "EcoChicEssentials",
    "LifestyleElevate", "ExploreTheVibe", "FreshBeginningsNow", "NextLevelGlow",
    "PeacefulFusionLiving", "SimplyInspiredLiving", "PositiveEnergyVibes", "LifeInspired",
    "VibrantLifeNow", "PureVibesOnly", "EssenceOfLife", "InspireDaily",
    "LifeStyleHub", "VibeAndThrive", "PureJoyLiving", "BrightLifeNow",
    "InspirationStation", "LifeElevated", "PositivePathway", "VibrantVibesHub",
    "PurePossibilities", "LifeBloomNow", "ThriveTogether", "InspiredLivingHub",
    "VibeHighNow", "LifeInMotion", "PureEnergyVibes", "BlossomAndGrow",
    "LifeUnfolded", "VibrantJourney", "PureLifeEssence", "InspireAndThrive",
]

# All page names combined
ALL_PAGE_NAMES = (
    HEALTH_WELLNESS_NAMES +
    HOME_DECOR_NAMES +
    BEAUTY_MODELING_NAMES +
    INSURANCE_FINANCE_NAMES +
    REAL_ESTATE_NAMES +
    UNIVERSAL_NAMES
)


def generate_page_names(base_name: str, count: int) -> List[Tuple[str, str]]:
    """
    Generate generic page names from predefined lists.

    Args:
        base_name: Category hint (e.g., "Insurance", "Beauty") - used to select relevant names
        count: Number of page names to generate

    Returns:
        List of tuples: (page_name, category)
    """
    base_lower = base_name.lower()

    # Select appropriate name list based on base_name hint
    if any(word in base_lower for word in ['health', 'wellness', 'fit', 'gym', 'yoga', 'medical']):
        name_pool = HEALTH_WELLNESS_NAMES + UNIVERSAL_NAMES
        category = "health_wellness"
    elif any(word in base_lower for word in ['home', 'decor', 'interior', 'design', 'furniture', 'living']):
        name_pool = HOME_DECOR_NAMES + UNIVERSAL_NAMES
        category = "home_decor"
    elif any(word in base_lower for word in ['model', 'beauty', 'fashion', 'makeup', 'glam', 'style']):
        name_pool = BEAUTY_MODELING_NAMES + UNIVERSAL_NAMES
        category = "beauty_modeling"
    elif any(word in base_lower for word in ['insurance', 'finance', 'invest', 'money', 'bank', 'loan']):
        name_pool = INSURANCE_FINANCE_NAMES + UNIVERSAL_NAMES
        category = "insurance_finance"
    elif any(word in base_lower for word in ['real estate', 'property', 'home', 'house', 'apartment', 'realty']):
        name_pool = REAL_ESTATE_NAMES + UNIVERSAL_NAMES
        category = "real_estate"
    else:
        # Use all names for unknown categories
        name_pool = ALL_PAGE_NAMES
        category = "universal"

    # Select random unique names
    if count <= len(name_pool):
        selected_names = random.sample(name_pool, count)
    else:
        # If requesting more names than available, allow repetition with suffix
        selected_names = []
        for i in range(count):
            name = random.choice(name_pool)
            if name in selected_names:
                name = f"{name}{i+1}"
            selected_names.append(name)

    # Return as list of tuples (name, category)
    return [(name, category) for name in selected_names]


def get_page_name_for_sequence(base_name: str, sequence_num: int, total_count: int) -> Tuple[str, str]:
    """
    Get a deterministic page name for a specific sequence number.

    Args:
        base_name: Category hint for the page
        sequence_num: The sequence number (1-indexed)
        total_count: Total number of pages being created

    Returns:
        Tuple of (page_name, category)
    """
    base_lower = base_name.lower()

    # Select appropriate name list based on base_name hint
    if any(word in base_lower for word in ['health', 'wellness', 'fit', 'gym', 'yoga', 'medical']):
        name_pool = HEALTH_WELLNESS_NAMES + UNIVERSAL_NAMES
        category = "health_wellness"
    elif any(word in base_lower for word in ['home', 'decor', 'interior', 'design', 'furniture', 'living']):
        name_pool = HOME_DECOR_NAMES + UNIVERSAL_NAMES
        category = "home_decor"
    elif any(word in base_lower for word in ['model', 'beauty', 'fashion', 'makeup', 'glam', 'style']):
        name_pool = BEAUTY_MODELING_NAMES + UNIVERSAL_NAMES
        category = "beauty_modeling"
    elif any(word in base_lower for word in ['insurance', 'finance', 'invest', 'money', 'bank', 'loan']):
        name_pool = INSURANCE_FINANCE_NAMES + UNIVERSAL_NAMES
        category = "insurance_finance"
    elif any(word in base_lower for word in ['real estate', 'property', 'home', 'house', 'apartment', 'realty']):
        name_pool = REAL_ESTATE_NAMES + UNIVERSAL_NAMES
        category = "real_estate"
    else:
        name_pool = ALL_PAGE_NAMES
        category = "universal"

    # Seed random with sequence number for consistent name selection
    random.seed(sequence_num + hash(base_name))

    # Select name based on sequence
    index = (sequence_num - 1) % len(name_pool)
    name = name_pool[index]

    # Reset random seed
    random.seed()

    return (name, category)


def get_random_page_name(category: str = None) -> str:
    """
    Get a single random page name.

    Args:
        category: Optional category hint ('health', 'home', 'beauty', 'insurance', 'realestate')

    Returns:
        A random page name string
    """
    if category:
        category_lower = category.lower()
        if 'health' in category_lower:
            return random.choice(HEALTH_WELLNESS_NAMES)
        elif 'home' in category_lower or 'decor' in category_lower:
            return random.choice(HOME_DECOR_NAMES)
        elif 'beauty' in category_lower or 'model' in category_lower:
            return random.choice(BEAUTY_MODELING_NAMES)
        elif 'insurance' in category_lower or 'finance' in category_lower:
            return random.choice(INSURANCE_FINANCE_NAMES)
        elif 'real' in category_lower or 'property' in category_lower:
            return random.choice(REAL_ESTATE_NAMES)

    return random.choice(ALL_PAGE_NAMES)

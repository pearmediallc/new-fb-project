"""
Celery tasks for Facebook Page generation using Selenium.
Handles async batch processing and stores results in MongoDB.
"""

import time
import random
import logging
from celery import shared_task
from django.conf import settings

# Facebook Page Categories with keyword matching
CATEGORY_KEYWORDS = {
    # Local Business or Place
    'Restaurant': ['restaurant', 'cafe', 'bistro', 'diner', 'eatery', 'dining'],
    'Shopping & Retail': ['shop', 'store', 'retail', 'mart', 'boutique', 'mall', 'outlet'],
    'Food & Beverage': ['food', 'coffee', 'tea', 'chai', 'pizza', 'burger', 'bakery', 'snack', 'juice', 'drinks', 'bar', 'grill'],
    'Beauty, Cosmetic & Personal Care': ['beauty', 'cosmetic', 'makeup', 'skincare', 'parlor', 'nail'],
    'Health/Beauty': ['salon', 'spa', 'haircut', 'barber', 'grooming'],
    'Hospital/Clinic': ['hospital', 'clinic', 'medical', 'doctor', 'pharma', 'dental'],

    # Company, Organization, or Institution
    'Business': ['business', 'enterprise', 'corp', 'inc', 'ltd'],
    'Consulting Agency': ['consulting', 'consultant', 'advisor', 'advisory'],
    'Marketing Agency': ['marketing', 'advertising', 'ads', 'promotion', 'branding'],
    'Technology Company': ['tech', 'software', 'app', 'digital', 'saas', 'it'],
    'Non-Profit Organization': ['ngo', 'nonprofit', 'charity', 'foundation', 'volunteer'],
    'Educational Organization': ['school', 'college', 'university', 'academy', 'tutor', 'education', 'learning', 'course'],

    # Brand or Product
    'Consumer Electronics': ['electronics', 'gadget', 'device', 'mobile', 'phone', 'laptop', 'computer'],
    'Clothing (Apparel)': ['clothing', 'apparel', 'fashion', 'wear', 'dress', 'shirt', 'jeans'],
    'Fitness & Health': ['fitness', 'gym', 'workout', 'exercise', 'training'],
    'Health & Wellness Website': ['wellness', 'health', 'yoga', 'meditation', 'mindfulness'],

    # Artist, Band, or Public Figure
    'Musician/Band': ['music', 'band', 'singer', 'song', 'album', 'concert'],
    'Actor/Director': ['actor', 'actress', 'director', 'film', 'cinema'],
    'Writer': ['writer', 'author', 'book', 'novel', 'blog', 'content'],
    'Public Figure': ['influencer', 'celebrity', 'star', 'famous'],
    'Comedian': ['comedy', 'comedian', 'funny', 'humor', 'standup'],

    # Entertainment
    'Movie': ['movie', 'film', 'cinema', 'theater', 'hollywood'],
    'TV Show': ['tv', 'show', 'series', 'episode', 'streaming'],
    'Video Game': ['game', 'gaming', 'gamer', 'esports', 'xbox', 'playstation'],
    'Podcast': ['podcast', 'audio', 'talk', 'interview'],
    'Radio Station': ['radio', 'fm', 'broadcast', 'station'],

    # Community or Cause
    'Charity': ['charity', 'donate', 'help', 'support', 'cause'],
    'Social Services': ['social', 'community', 'service', 'welfare'],
    'Animal Shelter': ['animal', 'pet', 'dog', 'cat', 'rescue', 'shelter'],
    'Religious Organization': ['church', 'temple', 'mosque', 'religious', 'faith', 'spiritual'],

    # Health & Wellness
    'Gym/Physical Fitness Center': ['gym', 'fitness center', 'crossfit', 'bodybuilding'],
    'Nutritionist': ['nutrition', 'diet', 'weight loss', 'healthy eating'],
    'Wellness Center': ['wellness center', 'retreat', 'healing'],

    # E-commerce
    'Retail Company': ['retail', 'ecommerce', 'online store', 'marketplace'],
    'Fashion Retailer': ['fashion', 'style', 'trendy', 'designer'],
    'Home Goods': ['home', 'furniture', 'decor', 'interior', 'kitchen'],

    # Food & Beverage specific
    'Food Delivery Service': ['delivery', 'order', 'takeaway', 'takeout'],
    'Food Trucks': ['food truck', 'street food', 'mobile food'],
    'Catering': ['catering', 'event food', 'party food'],
    'Recipe Blog': ['recipe', 'cooking', 'cook', 'chef', 'kitchen tips'],

    # Technology
    'Software Company': ['software', 'saas', 'platform', 'tool'],
    'App Developer': ['app', 'developer', 'mobile app', 'ios', 'android'],
    'Tech Startup': ['startup', 'innovation', 'disrupt', 'venture'],
    'Gadget Reviews': ['review', 'unbox', 'tech review', 'product review'],
}

# Creative page name templates by category type
PAGE_NAME_TEMPLATES = {
    'food': [
        '{adj} Kitchen', '{adj} Cafe', '{adj} Bistro', '{adj} Grill', '{adj} Bites',
        'The {adj} Table', '{name} Eats', '{name} Kitchen', 'Cafe {name}', '{adj} Food Hub',
        '{name} Restaurant', 'The {adj} Diner', '{adj} Delights', '{name} Cuisine',
        'Chai {suffix}', 'Coffee {suffix}', 'Pizza {suffix}', 'Burger {suffix}',
    ],
    'fashion': [
        '{adj} Fashion', '{adj} Style', '{name} Boutique', '{adj} Trends', 'The {adj} Closet',
        '{name} Wear', '{adj} Apparel', 'Style by {name}', '{adj} Wardrobe', '{name} Fashion House',
        'The Fashion {suffix}', '{adj} Clothing Co', '{name} Styles',
    ],
    'tech': [
        '{name} Tech', '{adj} Solutions', '{name} Digital', '{adj} Systems', 'Tech {suffix}',
        '{name} Software', '{adj} Labs', '{name} Technologies', 'Digital {suffix}', '{adj} IT',
        '{name} Apps', 'Smart {suffix}', '{adj} Innovations', 'Code {suffix}',
    ],
    'health': [
        '{adj} Wellness', '{name} Fitness', '{adj} Health Hub', 'Fit {suffix}', '{name} Gym',
        '{adj} Spa', 'Wellness by {name}', 'The {adj} Clinic', '{name} Care', 'Healthy {suffix}',
        '{adj} Yoga', 'Mind & Body {suffix}', '{name} Therapy',
    ],
    'beauty': [
        '{adj} Beauty', '{name} Salon', 'Glow {suffix}', '{adj} Skincare', 'Beauty by {name}',
        'The {adj} Parlor', '{name} Cosmetics', '{adj} Makeover', 'Radiant {suffix}',
        '{name} Beauty Bar', 'Luxe {suffix}',
    ],
    'education': [
        '{name} Academy', '{adj} Learning', 'The {adj} School', '{name} Institute', 'Learn {suffix}',
        '{adj} Education Hub', 'Study {suffix}', '{name} Tutors', 'The Learning {suffix}',
        '{adj} Classes', '{name} Training Center',
    ],
    'entertainment': [
        '{adj} Entertainment', '{name} Music', 'The {adj} Show', '{name} Productions', 'Fun {suffix}',
        '{adj} Events', 'Party {suffix}', '{name} Studios', 'The {adj} Stage', 'Live {suffix}',
    ],
    'home': [
        '{adj} Home', '{name} Interiors', 'Home {suffix}', '{adj} Decor', 'The {adj} House',
        '{name} Furnishings', 'Cozy {suffix}', '{adj} Living', 'Design by {name}', 'Home & {suffix}',
    ],
    'business': [
        '{name} Consulting', '{adj} Agency', '{name} Group', 'The {adj} Company', '{name} Services',
        '{adj} Enterprises', '{name} Solutions', 'Pro {suffix}', '{adj} Partners', '{name} Co',
    ],
    'community': [
        '{name} Foundation', '{adj} Community', 'Help {suffix}', '{name} Charity', 'Care {suffix}',
        'The {adj} Initiative', '{name} Volunteers', 'Support {suffix}', 'Give {suffix}',
    ],
}

# Adjectives for page names
PAGE_ADJECTIVES = [
    'Urban', 'Royal', 'Golden', 'Silver', 'Fresh', 'Prime', 'Elite', 'Classic', 'Modern', 'Trendy',
    'Happy', 'Lucky', 'Sunny', 'Cozy', 'Deluxe', 'Premium', 'Supreme', 'Grand', 'Global', 'Local',
    'Green', 'Blue', 'Red', 'Pink', 'Purple', 'Bright', 'Crystal', 'Diamond', 'Pearl', 'Velvet',
    'Express', 'Quick', 'Smart', 'Easy', 'Simple', 'Magic', 'Wonder', 'Dream', 'Star', 'Moon',
]

# Names for page names
PAGE_NAMES = [
    'Alex', 'Maya', 'Arya', 'Zara', 'Nova', 'Luna', 'Aria', 'Mia', 'Leo', 'Max',
    'Ruby', 'Jade', 'Ivy', 'Rose', 'Lily', 'Bella', 'Sophia', 'Emma', 'Olivia', 'Ava',
    'Zen', 'Bliss', 'Joy', 'Grace', 'Faith', 'Hope', 'Sky', 'Ocean', 'River', 'Storm',
]

# Suffixes for page names
PAGE_SUFFIXES = [
    'Hub', 'Zone', 'Spot', 'Place', 'Point', 'Corner', 'Studio', 'House', 'Central', 'World',
    'Pro', 'Plus', 'Max', 'Prime', 'Elite', 'Express', 'Direct', 'Online', 'Now', 'Daily',
]

def generate_creative_page_name(base_name: str = None) -> str:
    """Generate a creative page name."""
    # Pick a random category type
    category_types = list(PAGE_NAME_TEMPLATES.keys())
    cat_type = random.choice(category_types)

    # Pick a random template
    template = random.choice(PAGE_NAME_TEMPLATES[cat_type])

    # Fill in the template
    adj = random.choice(PAGE_ADJECTIVES)
    name = random.choice(PAGE_NAMES)
    suffix = random.choice(PAGE_SUFFIXES)

    page_name = template.format(adj=adj, name=name, suffix=suffix)

    # Add a random number sometimes for uniqueness
    if random.random() < 0.3:
        page_name = f"{page_name} {random.randint(1, 99)}"

    return page_name

def get_category_for_name(page_name: str) -> str:
    """Get a relevant category based on page name keywords."""
    name_lower = page_name.lower()

    # Check each category's keywords
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                return category

    # No match found - pick random from common categories
    common_categories = ['Business', 'Shopping & Retail', 'Food & Beverage', 'Restaurant', 'Technology Company']
    return random.choice(common_categories)

from pages.mongodb import (
    get_task,
    update_task_status,
    increment_task_counter,
    store_page_details,
    get_profile,
)
from .selenium_driver import FacebookPageGenerator

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def create_pages_task(self, task_id: str):
    """
    Celery task to create multiple Facebook pages.

    Args:
        task_id: MongoDB ObjectId of the task document

    Returns:
        dict with execution results and metrics
    """
    logger.info(f"Starting page creation task: {task_id}")

    # Get task from MongoDB
    task = get_task(task_id)
    if not task:
        logger.error(f"Task not found: {task_id}")
        return {'error': f'Task {task_id} not found'}

    # Update task with Celery task ID
    update_task_status(task_id, 'running', celery_task_id=self.request.id)

    # Get profile credentials
    profile = get_profile(task['profile_id']) if task.get('profile_id') else None

    # Configuration
    headless = getattr(settings, 'SELENIUM_HEADLESS', True)
    timeout = getattr(settings, 'SELENIUM_TIMEOUT', 30)
    test_mode = True  # Set to False to use real Facebook (NOT RECOMMENDED)

    num_pages = task['num_pages']
    base_page_name = task['base_page_name']
    assigned_bm = task.get('assigned_bm', '')

    overall_start = time.time()
    results = {
        'task_id': task_id,
        'processed': 0,
        'success': 0,
        'failed': 0,
        'pages': []
    }

    try:
        with FacebookPageGenerator(
            headless=headless,
            timeout=timeout,
            test_mode=test_mode
        ) as generator:

            # Login if credentials provided and not in test mode
            if profile and not test_mode:
                login_success = generator.login_facebook(
                    email=profile['email'],
                    password=profile['password']
                )
                if not login_success:
                    update_task_status(task_id, 'failed',
                                       error_message='Facebook login failed')
                    return {'error': 'Facebook login failed'}

            # Create pages
            for i in range(1, num_pages + 1):
                # Check if task was cancelled
                current_task = get_task(task_id)
                if current_task and current_task.get('status') == 'cancelled':
                    logger.info(f"Task {task_id} was cancelled")
                    break

                # Generate creative page name or use base name
                if base_page_name and base_page_name.strip():
                    page_name = f"{base_page_name} {i}" if num_pages > 1 else base_page_name
                else:
                    page_name = generate_creative_page_name()

                logger.info(f"Creating page {i}/{num_pages}: {page_name}")

                # Create the page with smart category based on page name
                smart_category = get_category_for_name(page_name)
                print(f">>> Page: {page_name} → Category: {smart_category}")
                result = generator.create_facebook_page(
                    page_name=page_name,
                    category=smart_category,
                    description=f'{page_name} - Your trusted destination'
                )

                if result.success:
                    # Store page in MongoDB
                    store_page_details(
                        task_id=task_id,
                        page_id=result.page_id,
                        page_name=result.page_name,
                        page_url=result.page_url,
                        assigned_bm=assigned_bm,
                        sequence_num=i
                    )
                    increment_task_counter(task_id, 'pages_created')
                    results['success'] += 1
                else:
                    increment_task_counter(task_id, 'pages_failed')
                    results['failed'] += 1

                results['processed'] += 1
                results['pages'].append({
                    'name': page_name,
                    'page_id': result.page_id,
                    'page_url': result.page_url,
                    'success': result.success,
                    'duration': result.duration,
                    'error': result.error
                })

            # Get final metrics
            metrics = generator.get_metrics()
            results['metrics'] = metrics

    except Exception as e:
        logger.error(f"Task {task_id} failed with error: {e}")
        update_task_status(task_id, 'failed', error_message=str(e))
        results['error'] = str(e)
        return results

    # Update final task status
    total_time = time.time() - overall_start
    results['total_time'] = total_time

    final_status = 'completed' if results['failed'] == 0 else 'completed'
    if results['success'] == 0 and results['failed'] > 0:
        final_status = 'failed'

    update_task_status(task_id, final_status)

    logger.info(f"Task {task_id} completed: {results['success']} success, {results['failed']} failed")
    return results


@shared_task
def run_benchmark_task(base_name: str, count: int, headless: bool = True,
                       timeout: int = 30, test_mode: bool = True):
    """
    Celery task to run a Selenium benchmark test.

    Args:
        base_name: Base name for generated pages
        count: Number of pages to create
        headless: Whether to run browser in headless mode
        timeout: Selenium timeout in seconds
        test_mode: Use test site instead of real Facebook

    Returns:
        dict with benchmark results
    """
    logger.info(f"Starting benchmark: {count} pages with base name '{base_name}'")

    results = {
        'pages': [],
        'metrics': {}
    }

    start_time = time.time()

    try:
        with FacebookPageGenerator(
            headless=headless,
            timeout=timeout,
            test_mode=test_mode
        ) as generator:

            for i in range(1, count + 1):
                page_name = f"{base_name}_{i}"

                result = generator.create_facebook_page(page_name=page_name)

                results['pages'].append({
                    'name': page_name,
                    'page_id': result.page_id,
                    'success': result.success,
                    'duration': result.duration,
                    'error': result.error
                })

            results['metrics'] = generator.get_metrics()

    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
        results['error'] = str(e)

    results['total_time'] = time.time() - start_time
    logger.info(f"Benchmark completed in {results['total_time']:.2f}s")

    return results


# Synchronous versions for direct API calls (non-Celery)
def run_page_generation_sync(task_id: str) -> dict:
    """
    Synchronous version of page generation (runs immediately).
    Use this for testing or when Celery is not available.
    """
    return create_pages_task(task_id)


def run_efficiency_test(base_name: str, count: int, headless: bool = True,
                        timeout: int = 30) -> dict:
    """
    Run a standalone efficiency test synchronously.
    """
    results = {
        'pages': [],
        'metrics': {}
    }

    start_time = time.time()

    with FacebookPageGenerator(
        headless=headless,
        timeout=timeout,
        test_mode=True
    ) as generator:

        for i in range(1, count + 1):
            page_name = f"{base_name}_{i}"
            result = generator.create_facebook_page(page_name=page_name)
            results['pages'].append({
                'name': page_name,
                'page_id': result.page_id,
                'success': result.success,
                'duration': result.duration,
                'error': result.error
            })

        results['metrics'] = generator.get_metrics()

    results['total_time'] = time.time() - start_time
    return results

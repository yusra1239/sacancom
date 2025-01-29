from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Aboutus
import math
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.auth.models import User
from Advertiser.models import (
    AdsSource, Rules, Services_details, Advertiser, Area,
    RealEstateType, RealEstate, Service, Feature, RealEstate_Feature,
    Advertisement, RealEstateImage, Rating, Favorite
)

def index(request):
    """Render the index page with advertisements and other details."""
    ads = Advertisement.objects.filter(source__source_name='real_estate', promoted=True, is_active=True)
    # Get the average rating for the advertisement
    ads_with_ratings = []
    for ad in ads:
        avg_rating = Rating.objects.filter(advertisement=ad).aggregate(avg_rating=Avg('stars'))['avg_rating']
        ads_with_ratings.append({
            'advertisement': ad,
            'average_rating': avg_rating if avg_rating is not None else "0.0" # Default message if no rating
        })
    user_favorite_ids = (
        request.user.favorite_set.values_list('advertisement__ID', flat=True)
        if request.user.is_authenticated else []
    )    
    context = {
        'Aboutus': Aboutus.objects.all(),  # Fetch all Aboutus entries
        'Advertisement': ads,
        'Services_details': Services_details.objects.all(),
        'RealEstateType': RealEstateType.objects.all(),
        'ads_with_ratings': ads_with_ratings,  # Pass advertisements with their average ratings
        'user_favorite_ids': user_favorite_ids,

    }
    return render(request, 'core/index.html', context)



from django.core.paginator import Paginator
from math import radians, sin, cos, sqrt, atan2


def see_ads(request):
    """Filter and display advertisements based on user-selected criteria."""
    ads = Advertisement.objects.filter(is_active=True)
    latitude = float(request.GET.get('latitude', 0))
    longitude = float(request.GET.get('longitude', 0))
    # Get filter parameters from the request
    selected_features = request.GET.getlist('selected_features')
    selected_area = request.GET.get('district')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_type = request.GET.get('type_name')
    rooms = request.GET.get('rooms')

    # Build filter conditions using Q objects
    filter_conditions = Q()
    if selected_type:
        filter_conditions &= Q(RealEstate_id__type_id__id=selected_type)
    if rooms:
        filter_conditions &= Q(RealEstate_id__rooms=rooms)  # Use exact match for rooms
    if selected_area:
        filter_conditions &= Q(RealEstate_id__area_id__ID=selected_area)
    if selected_features:
        filter_conditions &= Q(RealEstate_id__realestate_feature__feature_ID__feature_name__in=selected_features)
    if min_price:
        filter_conditions &= Q(RealEstate_id__price__gte=min_price)
    if max_price:
        filter_conditions &= Q(RealEstate_id__price__lte=max_price)

    # Apply the combined filter conditions to the ads queryset
    ads = ads.filter(filter_conditions).distinct()
    nearby_ads = []
    for ad in ads:
        # Get ad's latitude and longitude
        ad_latitude = ad.RealEstate_id.attitude
        ad_longitude = ad.RealEstate_id.longitude

        # Calculate the distance between the user's location and the ad's location
        distance = haversine(latitude, longitude, ad_latitude, ad_longitude)

        # You can set a max distance (e.g., 10 km)
        if distance <=0.01:  # 100 meters = 0.1 km
            nearby_ads.append(ad)
    # Prepare ads with ratings
    ads_with_ratings = []
    for ad in ads:
        avg_rating = Rating.objects.filter(advertisement=ad).aggregate(avg_rating=Avg('stars'))['avg_rating']
        ads_with_ratings.append({
            'advertisement': ad,
            'average_rating': avg_rating if avg_rating is not None else "0.0"
        })

    # Pagination
    paginator = Paginator(ads_with_ratings, 9)  # Show 9 ads per page
    page_number = request.GET.get('page')  # Get the page number from the request
    page_obj = paginator.get_page(page_number)  # Get the ads for the current page

    user_favorite_ids = (
        request.user.favorite_set.values_list('advertisement__ID', flat=True)
        if request.user.is_authenticated else []
    )

    return render(request, 'core/see_ads.html', {
        'page_obj': page_obj,
        'user_favorite_ids': user_favorite_ids,
    })
@login_required
def see_ads_details(request, ads_id):
    """Display details of a specific advertisement, including features and images."""
    advertisement = get_object_or_404(Advertisement, ID=ads_id)

    # Fetch related features and images
    features = RealEstate_Feature.objects.filter(
        realEstate_ID=advertisement.RealEstate_id
    ).select_related('feature_ID') if advertisement.RealEstate_id else []
    images = RealEstateImage.objects.filter(
        RealEstate_id=advertisement.RealEstate_id
    ) if advertisement.RealEstate_id else []
    real_estate = advertisement.RealEstate_id if advertisement.RealEstate_id else None

    # Handle rating submission
    if request.method == 'POST':
        rating_value = request.POST.get('rating')  # Get rating from the form
        if rating_value:
            # Update or create the rating
            Rating.objects.update_or_create(
                advertisement=advertisement,
                user=request.user,
                defaults={'stars': int(rating_value)},  # Convert rating to integer
            )
            return redirect('see_ads_details', ads_id=ads_id)  # Redirect to the same page

    # Get the average rating for the advertisement
    average_rating = Rating.objects.filter(advertisement=advertisement).aggregate(
        avg_rating=Avg('stars')
    )['avg_rating']

    context = {
        'ads': advertisement,
        'features': features,
        'images': images,
        'real_estate': real_estate,
        'user': request.user,  # Pass user to the template
        'average_rating': average_rating,  # Pass average rating
    }
    return render(request, 'core/see_ads_details.html', context)

def see_servecs(request):
    """Display services based on user-selected criteria."""
    ads = Advertisement.objects.filter(source__source_name='service', is_active=True)
    selected_service = request.GET.get('Service_id')
    if selected_service:
        ads = ads.filter(service_id__services_details_id__ID=selected_service)

    return render(request, 'core/see_servecs.html', {'Advertisement': ads})

def search(request):
    """Render the search page with available areas, features, and real estate types."""
    real_estates = RealEstate.objects.all()
    unique_rooms = set(real_estate.rooms for real_estate in real_estates)


    context = {
        'Area': Area.objects.all(),
        'Feature': Feature.objects.all(),
        'unique_rooms': unique_rooms,  # Pass the unique room numbers to the template

    }
    return render(request, 'core/search.html', context)



@login_required
def favorate(request):
    """Show all favorite ads for the logged-in user."""
    favorites = Favorite.objects.filter(user=request.user).select_related('advertisement')
    context = {
        'favorites': [fav.advertisement for fav in favorites],
    }
    return render(request, 'core/favorate.html', context)

@login_required
def toggle_favorite(request, ad_id):
    """Toggle favorite status for an advertisement."""
    try:
        advertisement = Advertisement.objects.get(ID=ad_id)
    except Advertisement.DoesNotExist:
        return JsonResponse({'error': 'Advertisement not found'}, status=404)

    favorite, created = Favorite.objects.get_or_create(user=request.user, advertisement=advertisement)

    if not created:
        favorite.delete()  # Remove the favorite
        return JsonResponse({'status': 'removed'}, status=200)
    return JsonResponse({'status': 'added'}, status=200)


def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Difference in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance
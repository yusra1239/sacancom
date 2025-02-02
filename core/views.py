from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from math import radians, sin, cos, sqrt, atan2
from .models import Aboutus
from django.db.models import Count
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User
from Advertiser.models import (
    AdsSource, Rules, Services_details, Advertiser, Area,
    RealEstateType, RealEstate, Service, Feature, RealEstate_Feature,
    Advertisement, RealEstateImage, Rating, Favorite
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math


def index(request):
    """عرض الصفحة الرئيسية مع الإعلانات والتوصيات"""
    ads = Advertisement.objects.filter(is_active=True, promoted=True)
    
    # حساب متوسط التقييمات للإعلانات العادية
    ads_with_ratings = [
        {
            'advertisement': ad,
            'average_rating': Rating.objects.filter(advertisement=ad).aggregate(avg_rating=Avg('stars'))['avg_rating'] or "0.0"
        }
        for ad in ads
    ]
    
    # الحصول على الإعلانات الموصى بها للمستخدم
    recommended_ads = []
    if request.user.is_authenticated:
        recommendations = recommend_ads(request.user)
        if recommendations.exists():  # التحقق من وجود توصيات
            recommended_ads = [
                {
                    'advertisement': ad,
                    'average_rating': Rating.objects.filter(advertisement=ad).aggregate(avg_rating=Avg('stars'))['avg_rating'] or "0.0"
                }
                for ad in recommendations
            ]
        else:
            recommended_ads = []  # لا توجد توصيات
    
    
    user_favorite_ids = (
        request.user.favorite_set.values_list('advertisement__ID', flat=True)
        if request.user.is_authenticated else []
    )

    context = {
        'ads_with_ratings': ads_with_ratings,  # الإعلانات العادية مع التقييمات
        'recommended_ads': recommended_ads,  # الإعلانات المقترحة مع التقييمات
        'user_favorite_ids': user_favorite_ids,
        'RealEstateType': RealEstateType.objects.all(),
    }

    return render(request, 'core/index.html', context)


def see_ads(request):
    """Filter and display advertisements based on user-selected criteria."""
    ads = Advertisement.objects.filter(is_active=True)
    
    # Apply additional filters
    selected_type = request.GET.get('type_name')
    rooms = request.GET.get('rooms')
    selected_area = request.GET.get('district')
    selected_features = request.GET.getlist('selected_features')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    filter_conditions = Q()

    if selected_type:
        filter_conditions &= Q(RealEstate_id__type_id__id=selected_type)
    if rooms:
        filter_conditions &= Q(RealEstate_id__rooms=rooms)
    if selected_area:
        filter_conditions &= Q(RealEstate_id__ID=selected_area)
    if selected_features:
        filter_conditions &= Q(RealEstate_id__realestate_feature__feature_ID__feature_name__in=selected_features)
    if min_price:
        filter_conditions &= Q(RealEstate_id__price__gte=min_price)
    if max_price:
        filter_conditions &= Q(RealEstate_id__price__lte=max_price)

    ads = ads.filter(filter_conditions).distinct()

    # Check if there are filter parameters
    has_filters = any(
        key in request.GET for key in ['latitude', 'longitude']
    )

    if has_filters:
        # Apply geographic filtering if coordinates are available
        latitude = float(request.GET.get('latitude', 0))
        longitude = float(request.GET.get('longitude', 0))

        lat_range = 1.1  # ~1.1 km
        lon_range = 1.1  # ~1.1 km
        ads = ads.filter(
            RealEstate_id__attitude__range=(latitude - lat_range, latitude + lat_range),
            RealEstate_id__longitude__range=(longitude - lon_range, longitude + lon_range)
        )
       
        # Calculate distance for each advertisement
        nearby_ads = []
        for ad in ads:
            ad_latitude = ad.RealEstate_id.attitude
            ad_longitude = ad.RealEstate_id.longitude
            distance = haversine(latitude, longitude, ad_latitude, ad_longitude)
            if distance <= 10:  # 10 km maximum
                nearby_ads.append(ad)
    else:
        nearby_ads = ads

    # Prepare advertisements with ratings
    ads_with_ratings = []
    for ad in nearby_ads:
        avg_rating = Rating.objects.filter(advertisement=ad).aggregate(avg_rating=Avg('stars'))['avg_rating']
        ads_with_ratings.append({
            'advertisement': ad,
            'average_rating': avg_rating if avg_rating is not None else "0.0"
        })

    # Pagination setup
    paginator = Paginator(ads_with_ratings, 9)  # Display 9 advertisements per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get the user's favorite advertisements (if authenticated)
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
            Rating.objects.update_or_create(
                advertisement=advertisement,
                user=request.user,
                defaults={'stars': int(rating_value)},  # Convert rating to integer
            )
            return redirect('see_ads_details', ads_id=ads_id)

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
    """Calculate the distance between two geographic coordinates."""
    R = 6371.0  # Radius of the Earth in kilometers

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def get_ad_features(ad):
    """Transform advertisement features into text for similarity computation."""
    features = [
        ad.RealEstate_id.type_id.type,  # نوع العقار
        ad.area_id.directorate_name,  # المنطقة
        str(ad.RealEstate_id.price),  # السعر
        str(ad.RealEstate_id.rooms) if ad.RealEstate_id.rooms else "",  # عدد الغرف
        str(ad.RealEstate_id.space) if ad.RealEstate_id.space else "",  # المساحة
    ]
    return " ".join(features)


def recommend_ads(user):
    """Recommend advertisements based on user preferences (favorites and ratings)."""
    # Get user's favorite and rated ads
    favorite_ads = Favorite.objects.filter(user=user).values_list('advertisement', flat=True)
    rated_ads = Rating.objects.filter(user=user).values_list('advertisement', flat=True)
    user_ads = set(favorite_ads) | set(rated_ads)

    if not user_ads:
        return Advertisement.objects.none()

    # Collect features of user's preferred ads
    ads_data = []
    for ad_id in user_ads:
        ad = Advertisement.objects.filter(ID=ad_id, RealEstate_id__isnull=False).first()
        if ad:
            ads_data.append(get_ad_features(ad))

    if not ads_data:
        return Advertisement.objects.none()

    # Convert text features to vectors using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(ads_data)

    # Calculate similarity between ads
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find similar ads
    recommended_ads = set()
    for i, ad_id in enumerate(user_ads):
        similar_indices = similarity_matrix[i].argsort()[-2::-1]  # Get most similar ads
        for idx in similar_indices:
            recommended_ads.add(list(user_ads)[idx])

    return Advertisement.objects.filter(ID__in=recommended_ads)[:9]
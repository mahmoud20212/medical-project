from django.core.paginator import Paginator
from django.db.models import Count, Max, Q
from django.shortcuts import render, get_object_or_404
from .models import Specialization, Course, Team, HomePageContent


def paginate_queryset(request, queryset, per_page):
  paginator = Paginator(queryset, per_page)
  page_obj = paginator.get_page(request.GET.get('page'))
  query_params = request.GET.copy()
  query_params.pop('page', None)
  return page_obj, query_params.urlencode()

def index(request):
  try:
    home_page_content = HomePageContent.objects.get(pk=1)
  except HomePageContent.DoesNotExist:
    home_page_content = None

  home_specializations = Specialization.objects.filter(is_active=True).order_by('display_order', 'name')
  team_members = Team.objects.filter(is_active=True).order_by('display_order', 'name')


  return render(request, 'index.html', {
    'home_page_content': home_page_content,
    'home_specializations': home_specializations,
    'team_members': team_members,
  })

def resources(request):
  specializations = Specialization.objects.annotate(
    course_count=Count('courses', distinct=True),
    resource_count=Count('courses__resources', distinct=True),
  ).order_by('display_order', 'name')
  specializations, page_query = paginate_queryset(request, specializations, 8)
  return render(
    request,
    'resources.html',
    {
      'specializations': specializations,
      'page_query': page_query,
    }
  )

def specialization_detail(request, slug):
  specializations = Specialization.objects.all()
  specialization = get_object_or_404(specializations, slug=slug)
  courses = Course.objects.filter(specializations__slug=slug).distinct()

  selected_year = request.GET.get('year', '').strip()
  selected_semester = request.GET.get('semester', '').strip()
  search_query = request.GET.get('q', '').strip()

  valid_years = {str(value) for value, _ in Course.YEAR_CHOICES}
  valid_semesters = {str(value) for value, _ in Course.SEMESTER_CHOICES}

  if selected_year in valid_years:
    courses = courses.filter(academic_year=int(selected_year))
  else:
    selected_year = ''

  if selected_semester in valid_semesters:
    courses = courses.filter(semester=int(selected_semester))
  else:
    selected_semester = ''

  if search_query:
    courses = courses.filter(
      Q(name__icontains=search_query)
      | Q(code__icontains=search_query)
      | Q(description__icontains=search_query)
    )

  courses = courses.order_by('code', 'name')
  courses, page_query = paginate_queryset(request, courses, 9)
  active_filters_count = sum(bool(value) for value in (selected_year, selected_semester, search_query))

  return render(request, 'specialization_detail.html', {
    'specialization': specialization,
    'specializations': specializations,
    'courses': courses,
    'year_choices': Course.YEAR_CHOICES,
    'semester_choices': Course.SEMESTER_CHOICES,
    'filters': {
      'year': selected_year,
      'semester': selected_semester,
      'q': search_query,
    },
    'page_query': page_query,
    'active_filters_count': active_filters_count,
  })

def course_detail(request, pk):
  course = get_object_or_404(Course, pk=pk)
  resources = course.resources.all()

  selected_type = request.GET.get('type', '').strip()
  search_query = request.GET.get('q', '').strip()

  valid_types = {value for value, _ in course.resources.model.RESOURCE_TYPE_CHOICES}

  if selected_type in valid_types:
    resources = resources.filter(resource_type=selected_type)
  else:
    selected_type = ''

  if search_query:
    resources = resources.filter(
      Q(title__icontains=search_query)
      | Q(description__icontains=search_query)
      | Q(url__icontains=search_query)
    )

  filtered_resources = resources.order_by('title')
  filtered_resources, page_query = paginate_queryset(request, filtered_resources, 10)
  active_filters_count = sum(bool(value) for value in (selected_type, search_query))

  return render(request, 'course_detail.html', {
    'course': course,
    'filtered_resources': filtered_resources,
    'resource_type_choices': course.resources.model.RESOURCE_TYPE_CHOICES,
    'filters': {
      'type': selected_type,
      'q': search_query,
    },
    'page_query': page_query,
    'active_filters_count': active_filters_count,
  })

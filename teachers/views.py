from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.http import JsonResponse
from teachers.filter import ProductFilter
from teachers.utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage

from .models import Teachers


# Create your views here.


def index(request):
    return render(request, 'index.html')


def teacher(request):
    all_teachers = Teachers.objects.all()

    my_filter = ProductFilter(request.GET, queryset=all_teachers, )
    all_teachers = my_filter.qs
    count = all_teachers.count()

    items_per_page = 30
    paginator = Paginator(all_teachers, items_per_page)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    num_pages = paginator.num_pages
    if num_pages <= 7:
        page_range = range(1, num_pages + 1)
    elif page_obj.number <= 4:
        page_range = set(range(1, 6)) | {num_pages}
    elif page_obj.number >= num_pages - 3:
        page_range = {1} | set(range(num_pages - 4, num_pages + 1))
    else:
        page_range = {1} | set(range(page_obj.number - 2, page_obj.number + 3)) | {num_pages}

    start_index = (page_obj.number - 1) * items_per_page + 1
    end_index = min(page_obj.number * items_per_page, count)

    items_with_index = [(i + start_index, item) for i, item in enumerate(page_obj)]

    context = {
        "page_obj": page_obj,
        "page_range": page_range,
        "count": count,
        "start_index": start_index,
        "end_index": end_index,
        "items_with_index": items_with_index,
        "my_filter": my_filter,
    }

    return render(request, 'html/teachers.html', context)


def get_teacher(request):
    search = request.GET.get('search')
    payload = []
    if search:
        teacher_names = Teachers.objects.filter(full_name__icontains=search)
        for t_name in teacher_names:
            payload.append(t_name.full_name)

    return JsonResponse({
        'status': True,
        'data': payload,
    })


def teacher_info(request, id):
    teacher_info: Teachers = Teachers.objects.get(id=id)
    context = {
        "teacher_data": teacher_info
    }

    return render(request, 'html/teacherInfo.html', context)


def teacher_add(request, id):
    teacher = Teachers.objects.get(id=id)

    if request.method == 'POST':
        if request.POST.get('hidden_input') == 'rank':
            academic_rank_data = AcademicRankData.objects.filter(academic_rank_data_name=teacher).first()

            if academic_rank_data:
                academic_rank_data.place_of_defense_rank = request.POST.get('place_of_defense_rank')
                academic_rank_data.council_number_rank = request.POST.get('council_number_rank')
                academic_rank_data.given_by_whom_rank = request.POST.get('given_by_whom_rank')
                academic_rank_data.date_of_defense_rank = request.POST.get('date_of_defense_rank')
                academic_rank_data.number_of_degree_rank = request.POST.get('number_of_degree_rank')
                academic_rank_data.confirmed_date_rank = request.POST.get('confirmed_date_rank')
                academic_rank_data.account_number_rank = request.POST.get('account_number_rank')
                academic_rank_data.created_rank = request.POST.get('created_rank')
                academic_rank_data.changed_rank = request.POST.get('changed_rank')

                academic_rank_file_rank = request.FILES.get('file-2[]')
                if academic_rank_file_rank:
                    academic_rank_data.academic_rank_file_rank = academic_rank_file_rank

                academic_rank_data.save()

            else:
                academic_rank_data = AcademicRankData.objects.create(
                    place_of_defense_rank=request.POST.get('place_of_defense_rank'),
                    council_number_rank=request.POST.get('council_number_rank'),
                    given_by_whom_rank=request.POST.get('given_by_whom_rank'),
                    date_of_defense_rank=request.POST.get('date_of_defense_rank'),
                    number_of_degree_rank=request.POST.get('number_of_degree_rank'),
                    confirmed_date_rank=request.POST.get('confirmed_date_rank'),
                    account_number_rank=request.POST.get('account_number_rank'),
                    created_rank=request.POST.get('created_rank'),
                    changed_rank=request.POST.get('changed_rank'),
                    academic_rank_file_rank=request.FILES.get('file-2[]')
                )
                academic_rank_data.academic_rank_data_name.set([teacher])

        elif request.POST.get('hidden_input') == 'degree':
            place_of_defense_degree = request.POST.get('place_of_defense_degree')
            council_number_degree = request.POST.get('council_number_degree')
            given_by_whom_degree = request.POST.get('given_by_whom_degree')
            date_of_defense_degree = request.POST.get('date_of_defense_degree')
            number_of_degree_degree = request.POST.get('number_of_degree_degree')
            confirmed_date_degree = request.POST.get('confirmed_date_degree')
            account_number_degree = request.POST.get('account_number_degree')
            created_degree = request.POST.get('created_degree')
            changed_degree = request.POST.get('changed_degree')
            academic_degree_file_degree = request.FILES.get('file-1[]')

            academic_degree_data = AcademicDegreeData.objects.create(
                place_of_defense_degree=place_of_defense_degree,
                council_number_degree=council_number_degree,
                given_by_whom_degree=given_by_whom_degree,
                date_of_defense_degree=date_of_defense_degree,
                number_of_degree_degree=number_of_degree_degree,
                confirmed_date_degree=confirmed_date_degree,
                account_number_degree=account_number_degree,
                created_degree=created_degree,
                changed_degree=changed_degree,
                academic_degree_file_degree=academic_degree_file_degree,
            )

            academic_degree_data.academic_degree_data_name.set([teacher])
        elif request.POST.get('hidden_input') == 'lang':
            cert_type = request.POST.get('cert_type')
            cert_score = request.POST.get('cert_score')
            cert_file = request.FILES.get('file-3[]')

            language_cert = LanguageCert.objects.create(
                cert_type=cert_type,
                cert_score=cert_score,
                cert_file=cert_file,
            )

            language_cert.language_cert_name.set([teacher])

        return redirect('teacher_info', id=id)
    context = {
        'teacher_add': teacher_add,
        'teacher': teacher
    }
    return render(request, 'html/teacherAdd.html', context)


def teacher_data(request):
    saveData()
    saveFacultet()
    saveDepartment()
    saveTeacher()
    return HttpResponse("Data written to database")



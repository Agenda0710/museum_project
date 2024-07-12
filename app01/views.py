import uuid

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db import connection
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

import pickle
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import numpy as np

from .models import *

# Create your views here. 调用函数,经常动


# def news(request):
#     result = requests.get(
#         "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0",
#         headers={"User-Agent": 'Mozilla/5.0'})
#     data = result.json()
#     subjects = data.get('subjects', [])
#     return render(request, "news.html", {"subjects": subjects})


def getRelics(request):
    # 获取分页参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 4))
    museum_id = request.GET.get('museum_id', None)
    date = request.GET.get('date', None)
    name = request.GET.get('name', None)

    relics_query = Relics.objects.all()

    if museum_id:
        relics_query = relics_query.filter(museum_id=museum_id)
    if date:
        relics_query = relics_query.filter(date=date)
    if name:
        relics_query = relics_query.filter(name__icontains=name)

    # 分页
    paginator = Paginator(relics_query, page_size)
    page_obj = paginator.get_page(page)

    data_list = []
    for relic in page_obj:
        museum = Museum.objects.get(id=relic.museum_id).name
        data_list.append({
            'name': relic.name,
            'category': relic.category.name,
            'date': relic.date,
            'location': relic.location,
            'status': relic.status,
            'image': relic.image,
            'museum': museum,
        })

    # 获取所有文物的年代和博物馆列表
    dates = Relics.objects.values_list('date', flat=True).distinct()
    museums = Museum.objects.values('id', 'name')
    categories = Category.objects.values('id', 'name')

    return JsonResponse({
        'data': data_list,
        'total': paginator.count,
        'dates': list(dates),
        'museums': list(museums),
        'categories': list(categories),
    }, safe=False)


def getCategory(request):
    with connection.cursor() as cursor:
        cursor.execute("select category.id id,category.name name from cultural_relics.category order by category.id")
        data = cursor.fetchall()
        data_list = [{'id': row[0], 'name': row[1]} for row in data]
        return JsonResponse(data_list, safe=False)


@csrf_exempt
def updateCategory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_name = data.get('name', None)

        if new_name is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided'}, status=400)

        try:
            # 假设这里根据某些唯一条件确定要更新的记录，例如 name 是唯一的
            with connection.cursor() as cursor:
                cursor.execute("UPDATE cultural_relics.category SET name = %s WHERE name = %s", [new_name, new_name])

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def deleteCategory(request, id):
    if request.method == 'DELETE':
        try:
            category = Category.objects.get(pk=id)
            category.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except Category.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Category not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def uploadFile(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
        bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com/', 'web-framework0710')
        number = uuid.uuid4()
        baseFileName = str(number) + '.jpg'
        file.name = baseFileName
        bucket.put_object(file.name, file)

        image_url = f'https://web-framework0710.oss-cn-beijing.aliyuncs.com/{baseFileName}'
        print(image_url)

        return JsonResponse({'imageUrl': image_url})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def updateRelics(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category = data.get('category', None)
        name = data.get('name', None)
        date = data.get('date', None)
        location = data.get('location', None)
        status = data.get('status', None)
        image = data.get('image', None)
        print(image)

        if category is None or name is None or date is None or location is None or status is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid data provided'}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM cultural_relics.category WHERE name = %s", [category])
                category_id = cursor.fetchone()

                if category_id is None:
                    return JsonResponse({'status': 'error', 'message': 'Category not found'}, status=404)

                category_id = category_id[0]

                cursor.execute(
                    "UPDATE cultural_relics.relics "
                    "SET category_id = %s, date = %s, location = %s, status = %s, name = %s, image = %s "
                    "WHERE name = %s",
                    [category_id, date, location, status, name, image, name]
                )

                return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def getPercent(request):
    museumId = request.GET.get('id', None)
    if not museumId:
        return JsonResponse({"error": "Museum ID is required"}, status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM cultural_relics.relics WHERE museum_id = %s AND status = 1", [museumId])
        count_active = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM cultural_relics.relics WHERE museum_id = %s AND status = 0", [museumId])
        count_inactive = cursor.fetchone()[0]

        if count_active + count_inactive == 0:
            percent = 0
        else:
            percent = int((count_active / (count_active + count_inactive)) * 100)

        return JsonResponse({"percent": percent})


def getRelicsInfo(request):
    with connection.cursor() as cursor:
        cursor.execute("select relics.name,museum.name,relics.location "
                       "from cultural_relics.relics,cultural_relics.museum "
                       "where relics.museum_id = museum.id and status = 1")
        tableData = cursor.fetchall()
        data_list = [{'name': row[0], 'museumName': row[1], 'location': row[2]} for row in tableData]
        return JsonResponse(data_list, safe=False)


def getCircleInfo(request):
    with connection.cursor() as cursor:
        cursor.execute("select category.name, count(*) from cultural_relics.category,"
                       "cultural_relics.relics where category.id = relics.category_id group by category.name")
        data = cursor.fetchall()
        data_list = [{'name': row[0], 'count': row[1]} for row in data]
        return JsonResponse(data_list, safe=False)


def getColumChartInfo(request):
    with connection.cursor() as cursor:
        cursor.execute("select relics.date, count(*) from "
                       "cultural_relics.relics"
                       " group by relics.date")
        data = cursor.fetchall()
        data_list = [{'name': row[0], 'count': row[1]} for row in data]
        return JsonResponse(data_list, safe=False)


@csrf_exempt
def deleteRelics(request):
    if request.method == 'DELETE':
        relics_name = request.GET.get('name', None)
        if relics_name is None:
            return JsonResponse({'status': 'error', 'message': '缺少name参数'}, status=400)
        try:
            relic = get_object_or_404(Relics, name=relics_name)
            relic.delete()
            return JsonResponse({'status': 'success', 'message': '文物已删除'})
        except Relics.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '文物未找到'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': '请求方法错误'}, status=405)


@csrf_exempt
def insertRelics(request):
    data = json.loads(request.body)
    name = data.get('name')
    category_id = data.get('category')
    date = data.get('date')
    location = data.get('location')
    status = data.get('status')
    museum_id = data.get('museum')

    if not all([name, category_id, date, location, status, museum_id]):
        return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)

    category = Category.objects.get(id=category_id)
    museum = Museum.objects.get(id=museum_id)

    new_relic = Relics.objects.create(
        name=name,
        category=category,
        date=date,
        location=location,
        status=status,
        museum=museum
    )

    print(new_relic)

    return JsonResponse({'status': 'success', 'message': 'Relic added successfully'}, status=201)


def getAllUsers(request):
    users = MuseumUsers.objects.all().values('name', 'gender', 'birthday', 'status', 'position', 'user_name')
    return JsonResponse(list(users), safe=False)


class PredictVisitorsView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        data = json.loads(request.body)
        date_type = int(data.get('date_type'))
        weather_condition = int(data.get('weather_condition'))
        temperature = float(data.get('temperature'))
        promotion = int(data.get('promotion'))

        model = pickle.load(open('visitor_model.pkl', 'rb'))
        input_data = np.array([[date_type, weather_condition, temperature, promotion]])
        visitors = model.predict(input_data)[0]

        return JsonResponse({'visitors': int(visitors)})

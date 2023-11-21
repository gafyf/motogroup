from django.shortcuts import render
from .models import New
from django.core.paginator import Paginator
from .run_scraping import run_file_periodically
# from .scrap import scraped_data
# from .scraper import scraped_data
# from django.core.files.images import ImageFile
# from io import BytesIO
# from django.http import JsonResponse
# import boto3
# import requests
# import json


# def get_data_from_lambda(request):
#     # Initialize AWS Lambda client
#     lambda_client = boto3.client('lambda')

#     # Define the Lambda function name
#     lambda_function_name = 'selenium-test'  # Replace with your Lambda function name

#     # Invoke the Lambda function
#     response = lambda_client.invoke(
#         FunctionName=lambda_function_name,
#         InvocationType='RequestResponse',
#         # Add any necessary Payload or context
#     )

#     # Process the Lambda response
#     lambda_response = response['Payload'].read()
#     data_list = lambda_response.decode('utf-8')

#     # Convert the data_list string to a Python list
#     data_list = eval(data_list)

#     # Return the data as JSON response
#     # return JsonResponse({'data_list': data_list})
#     # return data_list
#     return JsonResponse(data_list, safe=False)

def new(request):
    # lambda_client = boto3.client('lambda', region_name='eu-central-1')

    # # Define the Lambda function name
    # lambda_function_name = 'selenium-test'  # Replace with your Lambda function name

    # # Invoke the Lambda function
    # response = lambda_client.invoke(
    #     FunctionName=lambda_function_name,
    #     InvocationType='RequestResponse',
    #     # Add any necessary Payload or context
    # )

    # # Process the Lambda response
    # lambda_response = response['Payload'].read()

    # data_list = lambda_response.decode('utf-8')

    # # Convert the data_list string to a Python list
    # data_list = eval(data_list)
    # Parse the JSON string into a list of dictionaries
    # data_list = json.loads(lambda_response)

    # print('scraped_data', scraped_data)
    
    # for data in scraped_data:
    #     title = data['article_title']
    #     # Check if a New object with the same title already exists
    #     if not New.objects.filter(title=title).exists():
    #         response = requests.get(data['article_image'])
    #         response.raise_for_status()
    #         # Get the image data in bytes
    #         image_data = response.content
    #         # Create a BytesIO object to create a Django File object
    #         image_file = ImageFile(BytesIO(image_data), name=f"{data['article_title']}.jpg")

    #         new = New(
    #             title=data['article_title'], 
    #             description=data['article_description'], 
    #             text=data['article_block_text'], 
    #             link=data['link'],
    #             image=image_file,
    #             )
    #         new.save()
    #     else:
    #         print('Exista deja')
    
    news = New.objects.all()
    title = request.GET.get('title')
    print('title ,' , title)

    if title:
        news = news.filter(title__icontains=title)

    paginator = Paginator(news, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'new/new.html', {'page_obj': page_obj, 'news': news})


def new_detail(request, pk):
    run_file_periodically()
    new = New.objects.get(pk=pk)
    return render(request, 'new/new_detail.html', {'new': new})


# def new(request):
#     print('scraped_data', scraped_data)
    
#     for data in scraped_data:
#         title = data['article_title']
#         # Check if a New object with the same title already exists
#         if not New.objects.filter(title=title).exists():
#             response = requests.get(data['article_image'])
#             response.raise_for_status()
#             # Get the image data in bytes
#             image_data = response.content
#             # Create a BytesIO object to create a Django File object
#             image_file = ImageFile(BytesIO(image_data), name=f"{data['article_title']}.jpg")

#             new = New(
#                 title=data['article_title'], 
#                 description=data['article_description'], 
#                 text=data['article_block_text'], 
#                 link=data['link'],
#                 image=image_file,
#                 )
#             new.save()
#         else:
#             print('Exista deja')
#     news = New.objects.all()
#     title = request.GET.get('title')
#     print('title ,' , title)

#     if title:
#         news = news.filter(title__icontains=title)

#     paginator = Paginator(news, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'new/new.html', {'page_obj': page_obj, 'news': news})


# def new_detail(request, pk):
#     new = New.objects.get(pk=pk)
#     return render(request, 'new/new_detail.html', {'new': new})




# def new(request):
#     print('scraped_data', scraped_data)
    
#     # for data in scraped_data:
#     #     response = requests.get(data['article_image'])
#     #     response.raise_for_status()
#     #     # Get the image data in bytes
#     #     image_data = response.content
#     #     # Create a BytesIO object to create a Django File object
#     #     image_file = ImageFile(BytesIO(image_data), name=f"{data['article_title']}.jpg")

#     #     new = New(
#     #         title=data['article_title'], 
#     #         description=data['article_descritpion'], 
#     #         text=data['article_block_text'], 
#     #         link=data['link'],
#     #         image=image_file,
#     #         )
#     #     new.save()

#     new_objects = []

#     for data in scraped_data:
#         response = requests.get(data['article_image'])
#         response.raise_for_status()
#         # Get the image data in bytes
#         image_data = response.content
#         # Create a BytesIO object to create a Django File object
#         image_file = ImageFile(BytesIO(image_data), name=f"{data['article_title']}.jpg")

#         new = New(
#             title=data['article_title'], 
#             description=data['article_description'],  # Fix the typo here
#             text=data['article_block_text'], 
#             link=data['link'],
#             image=image_file,
#         )
#         new_objects.append(new)

#     # Save all the 'new' objects in a single transaction
#     New.objects.bulk_create(new_objects)

    
#     news = New.objects.all()
#     title = request.GET.get('title')
#     print('title ,' , title)

#     if title:
#         news = news.filter(title__icontains=title)

#     paginator = Paginator(news, 6)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'new/new.html', {'page_obj': page_obj, 'news': news})
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DocumentSerializer, FolderSerializer, TopicSerializer, GetDocumentSerializer
from .models import Topic, Document, Folder
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



class DocumentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = DocumentSerializer

    id = openapi.Parameter('id', openapi.IN_QUERY, description="id of the document resource", type=openapi.TYPE_STRING, required=False)
    id_2 = openapi.Parameter('id', openapi.IN_QUERY, description="id of the document resource", type=openapi.TYPE_STRING, required=True)
    file = openapi.Parameter('file', openapi.IN_QUERY, description="file to upload", type=openapi.TYPE_FILE,required=True)
    folder = openapi.Parameter('folder', openapi.IN_QUERY, description="folder id to assign", type=openapi.TYPE_STRING,required=True)
    status = openapi.Parameter('status', openapi.IN_QUERY, description="status of the document resource", type=openapi.TYPE_STRING, required=False)
    limit_access = openapi.Parameter('limit_access', openapi.IN_QUERY, description="limit the access of the document to the user created", type=openapi.TYPE_BOOLEAN,required=False)
    res_200 = """
            "{
            'error': 'NULL',
            'error_code': 'NULL',
            'data': {
                    "documents" : [
                        {
                            'id':{id},
                            'file':{file},
                            'folder':{folder}
                        }
                    ]
            }
            """
    res_404 = """
            "{
                'error': Invalid document id.,
                'error_code': 'I001' ,
                'data': {},
            }
            """
    res_400 = """
        "{
            'error': '{error}',
            'error_code': '{error_code}',
            'data': {}
        }"""
    res_403 = """
        "{
            'error': 'Access Forbidden.',
            'error_code': 'F001',
            'data': {}
        }
            """
    @swagger_auto_schema(manual_parameters=[id], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized",403:res_403})
    def get(self,request, pk=None):
        context = {'request': request}
        query_list = []
        if not pk:
            query = Document.objects.filter(status = 'A',folder__status = 'A', folder__topic__status = 'A').distinct()
            for i in query:
                if (i.created_by == request.user):
                    query_list.append(i)
                else:
                    if i.limit_access == False:
                        query_list.append(i)
            results = self.serializer(query_list,context= context, many = True)
            return Response({'error': '', 'error_code': '',
                        'data': {"documents": results.data}}, status=200)
        else:
            query = Document.objects.filter(id = pk, status = 'A',folder__status = 'A', folder__topic__status = 'A').distinct()
            for i in query:
                if (i.created_by == request.user):
                    query_list.append(i)
                else:
                    if i.limit_access == False:
                        query_list.append(i)
            if query_list:
                results = self.serializer(query_list,context= context, many = True)
                
                # print()
                # url = results.data[0].get('file')
                # print(url)
                # parse_url = urlparse(url)
                # m = magic.Magic(mime=True)
                # r = requests.get(url)
                # f = io.BytesIO()
                # f.write(r.content)
                # print(m.from_buffer(f.getvalue()))
                # response = HttpResponse(f.getvalue(),content_type='application/force-download')
                # response['Content-Length'] = len(response.content)
                # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(parse_url.path))
                # return response
                return Response({'error': '', 'error_code': '',
                        'data': {"documents": results.data}}, status=200)
            else:
                error = 'Invalid document id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code': error_code,
                        'data': {}}, status=404)

    @swagger_auto_schema(manual_parameters=[file, status, limit_access], responses={200: res_200,400: res_400, 401: "Unauthorized"})
    def post(self, request):
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response({'error': '', 'error_code': '',
                        'data': {"documents": serializer.data}}, status=200)
        else:
            error = ', '.join(
                ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
            error_code = 'H001'
            return Response({'error': error,'error_code':error_code,'data':{}}, status=200)


    @swagger_auto_schema(manual_parameters=[id_2, status, limit_access], responses={200: res_200, 403:res_403,404: res_404, 400: res_400, 401: "Unauthorized"})
    def put(self, request, pk = None):
        if pk:
            document = Document.objects.filter(id = pk)
            if document.exists():
                document = document.first()
                if document.created_by == request.user:
                    serializer = self.serializer(data = request.data, instance=document,partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'error': '', 'error_code': '',
                                    'data': {"documents": serializer.data}}, status=200)
                    else:
                        error = ', '.join(
                            ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
                        error_code = 'H001'
                        return Response({'error': error,'error_code':error_code,'data':{}}, status=200)
                else:
                    error = 'Access Forbidden.'
                    error_code = 'F001'
                    return Response({'error': error, 'error_code': error_code,
                                    'data': {}}, status=403)

            else:
                error = 'Invalid document id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code': error_code,
                                'data': {}}, status=404)
        else:
            error = 'Resource id not provided.'
            error_code = 'I002'
            return Response({'error': error, 'error_code': error_code,
                    'data': {}}, status=404)

class GetDocuments(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = GetDocumentSerializer
    topic_id = openapi.Parameter('topic_id', openapi.IN_QUERY, description="id of the topic resource", type=openapi.TYPE_STRING, required=False)
    folder_id = openapi.Parameter('folder_id', openapi.IN_QUERY, description="id of the folder resource", type=openapi.TYPE_STRING, required=False)
    topic_name = openapi.Parameter('topic_name', openapi.IN_QUERY, description="name of the topic resource", type=openapi.TYPE_STRING,required=False)
    folder_name = openapi.Parameter('folder_name', openapi.IN_QUERY, description="name of the folder resource", type=openapi.TYPE_STRING,required=False)
    
    res_200 = """
            "{
            'error': 'NULL',
            'error_code': 'NULL',
            'data': {
                    "documents" : [
                        {
                            'id':{id},
                            'file':{file},
                            'folder':{folder}
                        }
                    ]
            }
            """
    res_404 = """
            "{
                'error': Invalid document id.,
                'error_code': 'I001' ,
                'data': {},
            }
            """
    res_400 = """
        "{
            'error': '{error}',
            'error_code': '{error_code}',
            'data': {}
        }
            """
    res_403 = """
        "{
            'error': 'Access Forbidden.',
            'error_code': 'F001',
            'data': {}
        }
            """
    
    @swagger_auto_schema(manual_parameters=[topic_id,folder_id,topic_name,folder_name], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized"})
    def post(self, request):
        context = {'request': request}
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            filter_dict = dict()
            filter_dict['status'] = 'A'
            filter_dict['folder__status'] = 'A'
            filter_dict['folder__topic__status'] = 'A'
            if data.get('topic_id', None):
                filter_dict['folder__topic__id'] = data.get('topic_id')
            if data.get('folder_id', None):
                filter_dict['folder__id'] = data.get('folder_id')
            if data.get('topic_name', None):
                filter_dict['folder__topic__name'] = data.get('topic_name')
            if data.get('folder_name', None):
                filter_dict['folder__name'] = data.get('folder_name')

            query = Document.objects.filter(**filter_dict).distinct()
            query_list = []
            for i in query:
                if (i.created_by == request.user):
                    query_list.append(i)
                else:
                    if i.limit_access == False:
                        query_list.append(i)

            if query_list:
                results = DocumentSerializer(query_list,context= context, many = True)
                return Response({'error': '', 'error_code': '',
                            'data': {"documents": results.data}}, status=200)
            else:
                error = 'Invalid document id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code': error_code,
                        'data': {}}, status=404)

        else:
            error = ', '.join(
                ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
            error_code = 'H001'
            return Response({'error': error, 'error_code': error_code,
                                    'data': {}}, status=200)


class FolderView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = FolderSerializer

    id = openapi.Parameter('id', openapi.IN_QUERY, description="id of the folder resource", type=openapi.TYPE_STRING, required=True)
    id_2 = openapi.Parameter('id', openapi.IN_QUERY, description="id of the folder resource", type=openapi.TYPE_STRING, required=False)
    name = openapi.Parameter('name', openapi.IN_QUERY, description="name of the folder resource", type=openapi.TYPE_STRING, required=True)
    topic = openapi.Parameter('topic', openapi.IN_QUERY, description="id of the topic resource", type=openapi.TYPE_STRING, required=True)
    status = openapi.Parameter('status', openapi.IN_QUERY, description="status of the folder resource", type=openapi.TYPE_STRING, required=False)
    res_200 = """
            "{
            'error': 'NULL',
            'error_code': 'NULL',
            'data': {
                    "folders" : [
                        {
                            'id':{id},
                            'name':{name},
                            'topic':{topic}
                        }
                    ]
            }
            """
    res_404 = """
            "{
                'error': {error},
                'error_code': {error_code},
                'data': {},
            }
            """
    res_400 = """
        "{
            'error': '{error}',
            'error_code': '{error_code}',
            'data': {}
        }
            """
    res_403 = """
        "{
            'error': 'Access Forbidden.',
            'error_code': 'F001',
            'data': {}
        }
            """

    @swagger_auto_schema(manual_parameters=[id_2], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized"})
    def get(self,request, pk=None):
        if not pk:
            query = Folder.objects.filter(status = 'A',topic__status = 'A').distinct()
            results = self.serializer(query, many = True)
            return Response({'error': '', 'error_code': '',
                        'data': {"folders": results.data}}, status=200)
        else:
            query = Folder.objects.filter(id = pk,status = 'A',topic__status = 'A').distinct()
            if query.exists():
                results = self.serializer(query, many= True)
                return Response({'error': '', 'error_code': '',
                        'data': {"folders": results.data}}, status=200)
            else:
                error = 'Invalid folder id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code':error_code,'data':{}}, status=404)
    @swagger_auto_schema(manual_parameters=[name, topic, status], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized"})
    def post(self, request):
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response({'error': '', 'error_code': '',
                        'data': {"folders": serializer.data}}, status=200)
        else:
            error = ', '.join(
                ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
            error_code = 'H001'
            return Response({'error': error,'error_code':error_code,'data':{}}, status=200)


    @swagger_auto_schema(manual_parameters=[id, status], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized",403:res_403})
    def put(self, request, pk = None):
        if pk:
            folder = Folder.objects.filter(id = pk)
            if folder.exists():
                folder = folder.first()
                if folder.created_by == request.user:
                    serializer = self.serializer(data = request.data, instance=folder,partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'error': '', 'error_code': '',
                        'data': {"folders": serializer.data}}, status=200)
                    else:
                        error = ', '.join(
                            ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
                        error_code = 'H001'
                        return Response({'error': error,'error_code':error_code,'data':{}}, status=200)
                else:
                    error = 'Access Forbidden.'
                    error_code = 'F001'
                    return Response({'error': error, 'error_code': error_code,
                                    'data': {}}, status=403)

            else:
                error = 'Invalid folder id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code': error_code,
                                'data': {}}, status=404)
        else:
            error = 'Resource id not provided.'
            error_code = 'I002'
            return Response({'error': error, 'error_code': error_code,
                    'data': {}}, status=404)





class TopicView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = TopicSerializer

    id = openapi.Parameter('id', openapi.IN_QUERY, description="id of the topic resource", type=openapi.TYPE_STRING, required=True)
    id_2 = openapi.Parameter('id', openapi.IN_QUERY, description="id of the topic resource", type=openapi.TYPE_STRING, required=False)
    name = openapi.Parameter('name', openapi.IN_QUERY, description="name of the topic resource", type=openapi.TYPE_STRING, required=True)
    status = openapi.Parameter('status', openapi.IN_QUERY, description="status of the topic resource", type=openapi.TYPE_STRING, required=False)
    short_description = openapi.Parameter('short_description', openapi.IN_QUERY, description="short description of the topic resource", type=openapi.TYPE_STRING, required=True)
    long_description = openapi.Parameter('long_description', openapi.IN_QUERY, description="long description of the topic resource", type=openapi.TYPE_STRING, required=True)
    res_200 = """
            "{
            'error': 'NULL',
            'error_code': 'NULL',
            'data': {
                    "topics" : [
                        {
                            'id':{id},
                            'name':{name},
                            'short_description':{short_description},
                            'long_description':{long_description}
                        }
                    ]
            }
            """
    res_404 = """
            "{
                'error': {error},
                'error_code': {error_code},
                'data': {},
            }
            """
    res_400 = """
        "{
            'error': '{error}',
            'error_code': '{error_code}',
            'data': {}
        }
            """
    res_403 = """
        "{
            'error': 'Access Forbidden.',
            'error_code': 'F001',
            'data': {}
        }
            """

    @swagger_auto_schema(manual_parameters=[id_2], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized"})
    def get(self,request, pk=None):
        if not pk:
            u = self.serializer(Topic.objects.filter(status = 'A'), many = True)
            return Response({'error': '', 'error_code': '',
                        'data': {"topics": u.data}}, status=200)
        else:
            d = Topic.objects.filter(id = pk,status = 'A')
            if d.exists():
                u = self.serializer(d, many= True)
                return Response({'error': '', 'error_code': '',
                        'data': {"topics": u.data}}, status=200)
            else:
                error = 'Invalid topic id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code':error_code,'data':{}}, status=404)

    @swagger_auto_schema(manual_parameters=[name, short_description, long_description,status], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized"})
    def post(self, request):
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response({'error': '', 'error_code': '',
                        'data': {"topics": serializer.data}}, status=200)
        else:
            error = ', '.join(
                ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
            error_code = 'H001'
            return Response({'error': error,'error_code':error_code,'data':{}}, status=200)

    @swagger_auto_schema(manual_parameters=[id, short_description, long_description,status], responses={200: res_200, 404: res_404, 400: res_400, 401: "Unauthorized",403:res_403})
    def put(self, request, pk = None):
        if pk:
            topic = Topic.objects.filter(id = pk)
            if topic.exists():
                topic = topic.first()
                if topic.created_by == request.user:
                    serializer = self.serializer(data = request.data, instance=topic,partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'error': '', 'error_code': '',
                        'data': {"topics": serializer.data}}, status=200)
                    else:
                        error = ', '.join(
                            ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
                        error_code = 'H001'
                        return Response({'error': error,'error_code':error_code,'data':{}}, status=200)
                else:
                    error = 'Access Forbidden.'
                    error_code = 'F001'
                    return Response({'error': error, 'error_code': error_code,
                                    'data': {}}, status=403)

            else:
                error = 'Invalid topic id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code': error_code,
                                'data': {}}, status=404)
        else:
            error = 'Resource id not provided.'
            error_code = 'I002'
            return Response({'error': error, 'error_code': error_code,
                    'data': {}}, status=404)


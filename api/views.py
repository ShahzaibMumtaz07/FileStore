from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import DocumentSerializer, FolderSerializer, TopicSerializer
from .models import *
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated


class DocumentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = DocumentSerializer

    def get(self,request, pk=None):
        context = {'request': request}
        if not pk:
            query = Document.objects.filter(status = 'A',limit_access = False,folder__status = 'A', folder__topic__status = 'A').distinct()
            results = self.serializer(query,context= context, many = True)
            return Response({'error': '', 'error_code': '',
                        'data': {"documents": results.data}}, status=200)
        else:
            query = Document.objects.filter(id = pk, status = 'A',limit_access = False,folder__status = 'A', folder__topic__status = 'A').distinct()
            if query.exists():
                results = self.serializer(query, many = True)
                return Response({'error': '', 'error_code': '',
                        'data': {"documents": results.data}}, status=200)
            else:
                error = 'Invalid document id.'
                error_code = 'I001'
                return Response({'error': error, 'error_code': error_code,
                        'data': {}}, status=404)


    def post(self, request):
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(True)
        else:
            error = ', '.join(
                ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
            return Response({'error': error}, status=200)
    
    def put(self, request, pk = None):
        if pk:
            document = Document.objects.filter(id = pk)
            if document.exists():
                document = document.first()
                if document.created_by == request.user:
                    serializer = self.serializer(data = request.data, instance=document,partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(True)
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




class FolderView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = FolderSerializer

    def get(self,request, pk=None):
        if not pk:
            u = self.serializer(Folder.objects.filter(status = 'A'), many = True)
            return Response({'error': '', 'error_code': '',
                        'data': {"folders": u.data}}, status=200)
        else:
            d = Folder.objects.filter(id = pk,status = 'A')
            if d.exists():
                u = self.serializer(d, many= True)
                return Response({'error': '', 'error_code': '',
                        'data': {"folders": u.data}}, status=200)
            else:
                error = 'Invalid folder id.'
                return Response({'error': error}, status=200)

    def post(self, request):
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(True)
        else:
            error = ', '.join(
                ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
            return Response({'error': error}, status=200)

    def put(self, request, pk = None):
        if pk:
            folder = Folder.objects.filter(id = pk)
            if folder.exists():
                folder = folder.first()
                if folder.created_by == request.user:
                    serializer = self.serializer(data = request.data, instance=folder,partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(True)
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





class TopicView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer = TopicSerializer

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
                error = 'Invalid folder id.'
                return Response({'error': error}, status=200)

    def post(self, request):
        serializer = self.serializer(data = request.data)
        if serializer.is_valid():
            serializer.save(created_by = request.user)
            return Response(True)
        else:
            error = ', '.join(
                ['{0}:{1}'.format(k, str(v[0])) for k, v in serializer.errors.items()])
            return Response({'error': error}, status=200)

    def put(self, request, pk = None):
        if pk:
            topic = Topic.objects.filter(id = pk)
            if topic.exists():
                topic = topic.first()
                if topic.created_by == request.user:
                    serializer = self.serializer(data = request.data, instance=topic,partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(True)
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


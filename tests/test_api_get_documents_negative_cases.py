from pydoc import Doc
from tkinter.tix import Tree
from django.test import TestCase
from django.urls import reverse

from api.models import Document, Folder, Topic
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()
class APITest(TestCase):
    client_ = APIClient()
    auth_token = None

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='abc123')
        
        self.username = 'admin'
        self.email = 'admin@g.com'
        self.password = 'abc123'
        self.data = {'username':self.username, 'password': self.password}


    def test_get_documents_by_combo_wrong(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:get-documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        f = Folder.objects.create(
            name = 'Folder 1',
            created_by = self.user
        )


        f2 = Folder.objects.create(
            name = 'Folder 2',
            created_by = self.user
        )

        f.topic.add(t)
        f2.topic.add(t)

        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        d2 = Document.objects.create(
            file = 'tests/index2.png',
            created_by = self.user
        )
        d2.folder.add(f2)



        query = {
            "topic_id" : 400,
            "folder_id" : 500,
            "folder_name" : 'Hello',
            "topic_name" : 'Feedback'
        }
        # print(query, url)

        resp = self.client_.post(url,query)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')

    def test_get_documents_by_id_wrong(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:get-documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        f = Folder.objects.create(
            name = 'Folder 1',
            created_by = self.user
        )


        f2 = Folder.objects.create(
            name = 'Folder 2',
            created_by = self.user
        )

        f.topic.add(t)
        f2.topic.add(t)

        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        d2 = Document.objects.create(
            file = 'tests/index2.png',
            created_by = self.user
        )
        d2.folder.add(f2)



        query = {
            "topic_id" : 400
        }

        resp = self.client_.post(url,query)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')


    def test_get_documents_by_name_wrong(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:get-documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        f = Folder.objects.create(
            name = 'Folder 1',
            created_by = self.user
        )


        f2 = Folder.objects.create(
            name = 'Folder 2',
            created_by = self.user
        )

        f.topic.add(t)
        f2.topic.add(t)

        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        d2 = Document.objects.create(
            file = 'tests/index2.png',
            created_by = self.user
        )
        d2.folder.add(f2)



        query = {
            "topic_name" : "Hello"
        }

        resp = self.client_.post(url,query)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')

    
    def test_get_documents_by_name_combo_wrong(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:get-documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        f = Folder.objects.create(
            name = 'Folder 1',
            created_by = self.user
        )


        f2 = Folder.objects.create(
            name = 'Folder 2',
            created_by = self.user
        )

        f.topic.add(t)
        f2.topic.add(t)

        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        d2 = Document.objects.create(
            file = 'tests/index2.png',
            created_by = self.user
        )
        d2.folder.add(f2)



        query = {
            "topic_name" : "Hello",
            "folder_name" : f.name
        }

        resp = self.client_.post(url,query)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')



    def test_get_documents_by_folder_id_combo_wrong(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:get-documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        f = Folder.objects.create(
            name = 'Folder 1',
            created_by = self.user
        )


        f2 = Folder.objects.create(
            name = 'Folder 2',
            created_by = self.user
        )

        f.topic.add(t)
        f2.topic.add(t)

        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        d2 = Document.objects.create(
            file = 'tests/index2.png',
            created_by = self.user
        )
        d2.folder.add(f2)



        query = {
            "folder_id" : 400
        }

        resp = self.client_.post(url,query)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')



    def test_get_documents_by_folder_name_combo_wrong(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:get-documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        f = Folder.objects.create(
            name = 'Folder 1',
            created_by = self.user
        )


        f2 = Folder.objects.create(
            name = 'Folder 2',
            created_by = self.user
        )

        f.topic.add(t)
        f2.topic.add(t)

        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        d2 = Document.objects.create(
            file = 'tests/index2.png',
            created_by = self.user
        )
        d2.folder.add(f2)



        query = {
            "folder_name" : "Feedback"
        }

        resp = self.client_.post(url,query)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')



    
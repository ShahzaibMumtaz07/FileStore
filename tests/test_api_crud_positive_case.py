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
        
        self.user2 = User.objects.create_superuser(username='admin1', password='abc123')
        
        self.username2 = 'admin1'
        self.email2 = 'admin1@g.com'
        self.password2 = 'abc123'
        self.data2 = {'username':self.username2, 'password': self.password2}

    def test_get_topic(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )

        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.get(url)
        
        topic_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertGreater(len(topic_data),0)

        url = url + str(t.id) + '/'
        resp = self.client_.get(url)
        
        topic_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(topic_data),1)

    def test_get_folder(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

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

        f.topic.add(t)

        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.get(url)
        
        folder_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertGreater(len(folder_data),0)

        url = url + str(f.id) + '/'
        resp = self.client_.get(url)
        
        folder_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(folder_data),1)


    def test_get_document(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

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

        f.topic.add(t)

        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertGreater(len(document_data),0)

        url = url + str(d.id) + '/'
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(document_data),1)

    def test_create_topic(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        query = {
            "name" : "Topic 1",
            "short_description" : 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            "long_description" : 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas'
        }

        resp = self.client_.post(url,query)
        
        topic_data = resp.data.get('data').get('topics')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        


    def test_create_folder(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        query = {
            "name": "Folder 1",
            "topic" : t.id
        }
        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.post(url, query)

        
        
        folder_data = resp.data.get('data').get('folders')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')

        f = Folder.objects.filter(id = folder_data.get('id')).exists()
        self.assertEquals(f,True)



    def test_create_document(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

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

        f.topic.add(t)

        temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        
        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        query = {
            'file':temp_file,
            'folder':f.id
        }

        resp = self.client_.post(url,query)
        document_data = resp.data.get('data').get('documents')
        
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        d = Document.objects.filter(id = document_data.get('id')).exists()

        self.assertEquals(d,True)

    def test_update_topic(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )

        url = url + str(t.id) + '/'
        query = {
            "status" : 'D'
        }

        resp = self.client_.put(url,query)
        topic_data = resp.data.get('data').get('topics')
        t = Topic.objects.get(id = topic_data.get('id'))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(t.status,'D')
        


    def test_update_folder(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

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

        # f.topic.add(t)
        query = {
            "status":'D'
        }
        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(f.id) + '/'
        resp = self.client_.put(url, query)

        
        
        folder_data = resp.data.get('data').get('folders')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')

        f = Folder.objects.get(id = folder_data.get('id'))
        self.assertEquals(f.status,'D')



    def test_update_document(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

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

        f.topic.add(t)

        
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(d.id) + '/'
        query = {
            "status":'D',
            "limit_access":True
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        d = Document.objects.get(id = document_data.get('id'))

        self.assertEquals(d.status,'D')
        self.assertEquals(d.limit_access,True)

    

    def test_get_document_limit_access(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data2)

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

        f.topic.add(t)

        
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user,
            limit_access = True
        )
        d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(document_data),0)

        url = url + str(d.id) + '/'
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error'], 'Invalid document id.')
        self.assertEquals(resp.data['error_code'], 'I001')
        # self.assertEquals(len(document_data),1)

    def test_get_document_limit_access_2(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

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

        f.topic.add(t)

        
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user,
            limit_access = True
        )
        d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(document_data),1)

        url = url + str(d.id) + '/'
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(document_data),1)

    def test_get_document_limit_access_3(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data2)

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

        f.topic.add(t)

        
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user,
        )
        d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(document_data),1)

        url = url + str(d.id) + '/'
        resp = self.client_.get(url)
        
        document_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error'], '')
        self.assertEquals(resp.data['error_code'], '')
        self.assertEquals(len(document_data),1)
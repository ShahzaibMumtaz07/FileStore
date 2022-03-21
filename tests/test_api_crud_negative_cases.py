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


    def test_get_topic_wrong_id(self):
        
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

        url = url + str(500) + '/'
        resp = self.client_.get(url)
        
        topic_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error'], 'Invalid topic id.')
        self.assertEquals(resp.data['error_code'], 'I001')

    
    def test_create_document_invalid_params(self):
        
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
        # with open('tests/index.png','rb') as f:    
        # d = Document.objects.create(
        #     file = 'tests/index.png',
        #     created_by = self.user
        # )
        # d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        query = {
            'file':temp_file,
            'folder':500
        }

        resp = self.client_.post(url,query)
        document_data = resp.data.get('data').get('documents')
        
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')

    def test_update_document_invalid_params(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
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
            "status":'E'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')

    def test_update_document_invalid_user(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
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
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Access Forbidden.')
        self.assertEquals(resp.status_code, 403)
        self.assertEquals(resp.data['error_code'], 'F001')

    def test_update_document_invalid_id(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(500) + '/'
        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Invalid document id.')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error_code'], 'I001')

    def test_update_document_missing_id(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:documents')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Resource id not provided.')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error_code'], 'I002')

    def test_get_folder_invalid_param(self):
        
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

        url = url + str(500) + '/'
        resp = self.client_.get(url)
        
        folder_data = resp.data.get('data')
        
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error'], 'Invalid folder id.')
        self.assertEquals(resp.data['error_code'], 'I001')

    def test_create_folder_invalid_params(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        # f = Folder.objects.create(
        #     name = 'Folder 1',
        #     created_by = self.user
        # )

        # f.topic.add(t)
        query = {
            "name": "",
            "topic" : t.id
        }
        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.post(url, query)

        
        
        folder_data = resp.data.get('data').get('folders')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')


##################################################################


    def test_update_folder_invalid_params(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(f.id) + '/'
        query = {
            "status":'E'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('folders')
        
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')

    def test_update_folder_invalid_user(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(f.id) + '/'
        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Access Forbidden.')
        self.assertEquals(resp.status_code, 403)
        self.assertEquals(resp.data['error_code'], 'F001')

    def test_update_folders_invalid_id(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(500) + '/'
        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Invalid folder id.')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error_code'], 'I001')

    def test_update_folder_missing_id(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:folders')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Resource id not provided.')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error_code'], 'I002')

###############################################################################
    
    def test_update_topic_invalid_params(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(t.id) + '/'
        query = {
            "status":'E'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('folders')
        
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')

    def test_update_topics_invalid_user(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(t.id) + '/'
        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Access Forbidden.')
        self.assertEquals(resp.status_code, 403)
        self.assertEquals(resp.data['error_code'], 'F001')

    def test_update_topics_invalid_id(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        url = url + str(500) + '/'
        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Invalid topic id.')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error_code'], 'I001')

    def test_update_topic_missing_id(self):
        
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

        # temp_file = SimpleUploadedFile("tests/index.png", open('tests/index.png', 'rb').read(), content_type="image/png")
        # with open('tests/index.png','rb') as f:    
        d = Document.objects.create(
            file = 'tests/index.png',
            created_by = self.user
        )
        d.folder.add(f)

        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        

        query = {
            "status":'D'
        }

        resp = self.client_.put(url,query)
        document_data = resp.data.get('data').get('documents')
        
        self.assertEquals(resp.data['error'],'Resource id not provided.')
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(resp.data['error_code'], 'I002')

    def test_create_topics_invalid_params(self):
        
        url = reverse('obtain_jwt_token')
        resp = self.client_.post(url, self.data)

        t = Topic.objects.create(
            name = 'Topic 1',
            short_description = 'Topic dsadsad asdsadas asdasdasd asdasdas sadsadasd sadasd',
            long_description = 'Topic sdadasd sdasdasd sadasdasd aasdsadasd sadasdasdas asdasdasdasdas sa dasdasdas',
            created_by = self.user
        )
        # f = Folder.objects.create(
        #     name = 'Folder 1',
        #     created_by = self.user
        # )

        # f.topic.add(t)
        query = {
            "name": "sdasd",
            "short_description":"",
            "long_description":"dasdaskd sdsdsdas sadsadasdsad sadsadasdasdas sadasdasdasdsad sadsadasdsadsad sadasdasd asdasdasdasd asdasdsad"
        }
        url = reverse('api:topics')
        token = resp.data.get('token', None)
        self.client_.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        
        resp = self.client_.post(url, query)

        
        
        folder_data = resp.data.get('data').get('folders')
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data['error_code'], 'H001')
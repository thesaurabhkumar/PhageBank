from django.test import TestCase, modify_settings, override_settings
import unittest,shutil, subprocess, django, io
# import Image
# import StringIO
from django.test import Client
from django.core.management import call_command
from PhageBank.core.views import *
from PhageBank.core.forms import *
import tempfile
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData, PreData
from django.core.files.uploadedfile import SimpleUploadedFile
from PhageBank.core.forms import Add_ResearchForm, AForm, AIForm, Edit_Phage_DataForm, Edit_ResearcherForm, Edit_ResearchForm, Edit_IsolationDataForm, Edit_Experiment_Form
from django.http.response import  HttpResponse
from faker import Faker
from django.conf import settings

from PIL import Image
from io import StringIO  # Python 3: from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

fake = Faker()

username = fake.word()

class SimpleTest(TestCase):    #unittest.TestCase
    valid_credentials = {
        'username': "test_user",
        'password': 'pass@123'}
    invalid_credentials = {
        'username': 'abcde',
        'password': '12345'}

    #client = Client()

    def setUp(self):
        # Every test needs a client.
        user = User.objects.create_user("test_user", 'testuser@test.com', 'pass@123')
        user.save()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/mylogin/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_user_exist(self):
        # Check that login is successful with valid user
        response = self.client.post('/mylogin/', self.valid_credentials, follow=True)
        #self.assertEqual(response.status_code,200)

        form_is_valid = response.json()['form_is_valid']
        self.assertEqual(form_is_valid,True)

    def test_user_doesnt_exist(self):
        # Check that login is unsuccessful with invalid user
        response = self.client.post('/mylogin/', self.invalid_credentials, follow=True)
        #index = response.content.find(b"Your username and password didn\'t match. Please try again.")

        form_is_valid = response.json()['form_is_valid']

        self.assertEqual(form_is_valid,False)
# Create your tests here.

    def test_add_phage_req(self):
        phage_desc = {"phage_lab": "Lab-A", "flag":1}
        self.client.login(username = "test_user", password= 'pass@123')
        response = self.client.post('/add_phage/', phage_desc, follow=True)
        approvePhage = response.json()['approvePhage']
        approveCPTid = response.json()['approveCPTid']
        self.assertEqual(approvePhage,1)
        self.assertEqual(approveCPTid,1)


    def test_add_phage_ut(self):
        phage_desc = {"phage_name" : "test_newphage", "phage_CPT_id" : "test_123", "phage_lab": "Lab-A", "flag":1}
        self.client.login(username = "test_user", password= 'pass@123')
        response = self.client.post('/add_phage/', phage_desc, follow=True)

        approvePhage = response.json()['approvePhage']
        approveCPTid = response.json()['approveCPTid']

        self.assertEqual(approvePhage,1)
        self.assertEqual(approveCPTid,1)

    def test_add_phage_invalid(self):
        phage_desc = {"phage_name" : "test_newphage", "phage_CPT_id" : "test_123", "phage_lab": "Lab-A", "flag":1}
        self.client.login(username = "test_user", password= 'pass@123')
        response = self.client.get('/add_phage/', phage_desc, follow=True)
        self.assertEqual(response.status_code,200)

    def test_edit_phage_ut(self):
        phage_desc = {"phage_name" : "test_newphage", "phage_CPT_id" : "test_123", "phage_lab": "Lab-A", "flag":1}
        self.client.login(username = "test_user", password= 'pass@123')
        response = self.client.post('/add_phage/', phage_desc, follow=True)
        phage_desc2 = {"phage_name" : "test_newphage12", "phage_CPT_id" : "test_1234", "phage_lab": "Lab-B", "flag":1}
        data = {'name':'test_newphage'}
        response1 = self.client.get('/edit_details/', data, follow=True)
        # phage_desc2 = {"phage_name" : "test_newphage12", "phage_CPT_id" : "test_1234", "phage_lab": "Lab-B", "flag":1}
        response2 = self.client.post(response1, phage_desc2, follow=True)
        response3 = self.client.post('/edit_details/?name=test_newphage', phage_desc2, follow=True)
        # last, code = response1.redirect_chain[0]
        # print(last)
        # self.assertEqual(approvePhage,1)
        self.assertEqual(response1.status_code,200)
        self.assertEqual(response2.status_code,404)
        self.assertEqual(response3.status_code,200)

fake = Faker()

username=fake.word()

class URLGETTest(unittest.TestCase):
    client = Client()

    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_home_url(self):
        response = self.client.get('/')
        print (response)
        self.assertEqual(response.status_code, 200)

    def test_view_phages_url(self):
        response = self.client.get('/view_phages/')
        self.assertEqual(response.status_code, 200)

    def test_search_phage_url(self):
        response = self.client.get('/search_phage/')
        self.assertEqual(response.status_code, 200)

    def test_uploads_url(self):
        response = self.client.get('/uploads/form/')
        self.assertEqual(response.status_code, 302)

    def test_edit_details_url(self):
        response = self.client.get('/edit_details/')
        self.assertEqual(response.status_code, 302)

    def test_change_password_url(self):
        response = self.client.get('/change_password/')
        self.assertEqual(response.status_code, 302)

    def test_logout_url(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)

    def test_mylogin_url(self):
        response = self.client.get('/mylogin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_url(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_addphage_url(self):
        response = self.client.get('/add_phage/')
        self.assertEqual(response.status_code, 302)

    def test_deleteall_url(self):
        response = self.client.get('/delete_all/')
        self.assertEqual(response.status_code, 302)

    def test_delete_url(self):
        response = self.client.get('/delete/')
        self.assertEqual(response.status_code, 302)

    def test_my_phages_url(self):
        response = self.client.get('/my_phages/')
        self.assertEqual(response.status_code, 200)


class RenewBookFormTest(TestCase):
    def test_renew_form_date_field_label(self):

        data={'username': 'foo',
              'email': 'alice@example.com',
              'password1': 'foo',
              'password2': 'foo'}
        form = SignUpForm(data)
        # self.assertEqual(form.errors['email'], [u"This email address is already in use."])
        self.assertTrue(form.is_valid())
        response = self.client.post('/signup', data, follow=True)
        self.assertEqual(response.status_code,200)
        data1={'username': 'foobar',
              'email': 'alice@example.com',
              'password1': 'foo',
              'password2': 'foo'}
        form1 = SignUpForm(data1)
        self.assertTrue(form1.is_valid())
        response1 = self.client.post('/signup', data1, follow=True)
        self.assertEqual(response1.status_code,200)

    def test_validates_password(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        data = {
            'old_password': 'sekret',
            'new_password1': 'testclient',
            'new_password2': 'testclient2',
        }
        self.client.login(username='testclient', password='sekret')
        response = self.client.post('/change_password', data, follow=True)
        # form = PasswordChangeForm(user, data)
        # self.assertFalse(form.is_valid())
        # self.assertEqual(len(form["new_password2"].errors), 1)
        # self.assertEqual(response.status_code, 302)
        index = response.content.find(b"The two password fields didn\'t match.")
        user.delete()
        self.assertEqual(index,-1)

    def test_validates_password_success(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        data = {
            'old_password': 'sekret',
            'new_password1': 'testclient',
            'new_password2': 'testclient',
        }
        self.client.login(username='testclient', password='sekret')
        form = PasswordChangeForm(user, data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form["new_password2"].errors), 0)
        user.delete()
    # def test_validates_password_success(self):
    #     user = User.objects.create_user(username='testclient', password='sekret')
    #     data = {
    #         'old_password': 'sekret',
    #         'new_password1': 'testclient',
    #         'new_password2': 'testclient',
    #     }
    #     form = PasswordChangeForm(user, data)
    #     self.assertFalse(form.is_valid())
    #     self.assertEqual(len(form["new_password2"].errors), 1)


class PhageViewTest(TestCase):

    def test_count(self):
        path = 'test1'
        os.mkdir(path)
        filename1 = '1' + '.jpg'
        f1 = open(os.path.join(path, filename1), 'wb')
        f1.close()

        filename2 = '2' + '.jpg'
        f2 = open(os.path.join(path, filename2), 'wb')
        f2.close()

        filename3 = '3' + '.csv'
        f3 = open(os.path.join(path, filename3), 'wb')
        f3.close()

        dir_name = os.path.join(os.curdir, path)
        val = count(dir_name)
        self.assertEqual(val, 2)
        shutil.rmtree(path)

    def test_list_path(self):
        path = "test2"
        os.mkdir(path)
        filename1 = '1' + '.jpg'
        f1 = open(os.path.join(path, filename1), 'wb')
        f1.close()
        val = list_path(path)
        self.assertEqual('1.jpg', str(val[0]))
        shutil.rmtree(path)

    def test_file_extension(self):
        class temp:
            def __init__(self, val):
                self.name = val
        x = temp('1.jpg')
        filename1 = '1' + '.jpg'
        f1 = open(filename1, 'wb')
        f1.close()

        self.assertRaises(ValidationError, validate_file_extension, x)
        os.remove(filename1)

    def test_delete_all_phages(self):
        user = User.objects.create_superuser(username='admin1', password='admin1', email="admin1@gmail.com")
        p1= PhageData.objects.create(phage_name='test21',phage_CPT_id='121')
        p2= PhageData.objects.create(phage_name='test22',phage_CPT_id='122')
        p3= PhageData.objects.create(phage_name='test23',phage_CPT_id='123')
        self.client.login(username='admin1', password='admin1')
        response = self.client.post('/delete_all/',follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    @override_settings(MEDIA_ROOT ='temp')
    def test_func(self):
        pname = 'A'
        print(settings.MEDIA_ROOT)
        os.mkdir(os.path.join(os.curdir,settings.MEDIA_ROOT ))
        dest_dir = os.path.join(os.curdir, settings.MEDIA_ROOT, "images")
        print (dest_dir)
        os.mkdir(dest_dir)
        docs_dest_dir = os.path.join(os.curdir, settings.MEDIA_ROOT, "docs")
        print(docs_dest_dir)
        os.mkdir(docs_dest_dir)
        func(pname)
        func(pname)
        shutil.rmtree(os.path.join(os.curdir,settings.MEDIA_ROOT ))

    def test_model_form_upload(self):
        user = User.objects.create_superuser(username='admin2', password='admin2', email="admin2@gmail.com")
        self.client.login(username='admin2', password='admin2')
        response2 = self.client.get('/uploads/form/', follow=True)
        self.assertEqual(response2.status_code, 200)

        response = self.client.post('/uploads/form/', follow=True, FILES='test2.csv')
        response.FILES = 'test2.csv'
        response.method ='POST'
        response.POST = True
        response.user = user
        # print(response)
        self.assertEqual(response.status_code, 200)
        user.delete()
        # model_form_upload(response)

    # def get_temporary_image(self):
    #     io = StringIO.StringIO()
    #     size = (200, 200)
    #     color = (255, 0, 0, 0)
    #     image = Image.new("RGBA", size, color)
    #     image.save(io, format='JPEG')
    #     image_file = InMemoryUploadedFile(io, None, 'foo.jpg', 'jpeg', io.len, None)
    #     image_file.seek(0)
    #     return image_file
    #
    # def test_handle_uploaded_file(self):
    #     dest = "a.jpg"
    #     self.get_temporary_image()
    #
    #     handle_uploaded_file(self.get_temporary_image(), dest)
    #
    #     os.remove("a.jpg")

    # def test_fillExpObjectedit(self):
    #     expform = Add_Experiment_Form()
    #     expform.owner = "blah"
    #     # expform={"owner:", "TimeStamp","category","short_name","full_name","methods","results")}
    #     p1= PhageData.objects.create(phage_name='test21',phage_CPT_id='121')
    #     p_exp= ExperimentData.objects.create(expkey=p1)
    #     self.client.post('/')
    #     if expform.is_valid():
    #         print("here")
    #         fillExpObjectedit(expform, p_exp)
    #         print(p_exp)
    #     self.assertEqual('blah', 'none')

class ModelTest(TestCase):

    def test_validate_latest(self):
        phage = PhageData.objects.create(phage_name='TestPhage', phage_CPT_id='123456')
        phage.save()
        q = PhageData.objects.all()
        val = validate_latest_phage(q)
        self.assertEqual(val, phage.phage_name)
        phage.delete()

    # def test_my_phages(self):
    #     user = User.objects.create_user(username='testclient', password='sekret')
    #     phage = PhageData.objects.create(phage_name='TestPhage', phage_CPT_id='123456',phage_submitted_user='testclient')
    #     phage.save()
    #     self.client.login(username='testclient', password='sekret')
    #     response = self.client.get('/my_phages')
    #     # q = PhageData.objects.filter(phage_submitted_user=user.username)
    #     # val = validate_latest_phage(q)
    #     # self.assertEqual(q, phage)
    #     # self.assertTrue(form.is_valid())
    #     self.assertEqual(response.status_code, 301)
    #     user.delete()
    #     phage.delete()

   # def test_isodata(self):
        #isoform = Isolation_Form.objects.create(owner_name='testowner', location='testloc')
    def test_my_phages(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        phage = PhageData.objects.create(phage_name='TestPhage', phage_CPT_id='123456',phage_submitted_user='testclient')
        phage.save()
        self.client.login(username='testclient', password='sekret')
        response = self.client.get('/my_phages')
        # q = PhageData.objects.filter(phage_submitted_user=user.username)
        # val = validate_latest_phage(q)
        # self.assertEqual(q, phage)
        # self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 301)
        user.delete()
        phage.delete()


    def test_view_all_phages(self):
        # user = User.objects.create_user(username='testclient', password='sekret')
        phage = PhageData.objects.create(phage_name='TestPhage', phage_CPT_id='123456')
        phage.save()
        # self.client.login(username='testclient', password='sekret')
        response = self.client.get('/view_phages')
        # q = PhageData.objects.filter(phage_submitted_user=user.username)
        # val = validate_latest_phage(q)
        # self.assertEqual(q, phage)
        # self.assertTrue(form.is_valid())
        self.assertEqual(response.status_code, 301)
        # user.delete()
        phage.delete()


    def test_count(self):
        p1= PhageData.objects.create(phage_name='test',phage_CPT_id='123')
        p2 = PhageData.objects.create(phage_name='test123',phage_CPT_id='12345')
        p3 = PreData.objects.create(phagename='test12', testkey=p1)
        name='manish'
        val = check_entry(name)
        self.assertEqual(val, False)

        name='test'
        val2 = check_entry(name)
        self.assertEqual(val2, True)
        p1.delete()
        p2.delete()
        p3.delete()

    def test_delete(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        p1= PhageData.objects.create(phage_name='test22',phage_CPT_id='123')
        dest_dir = os.path.join(settings.MEDIA_ROOT, "images", p1.phage_name)
        docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", p1.phage_name)
        os.mkdir(dest_dir)
        os.mkdir(docs_dest_dir)
        self.client.login(username='testclient', password='sekret')
        data = {"name":"test22"}
        response = self.client.get('/delete/',data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    def test_view_phage(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        p1= PhageData.objects.create(phage_name='test22',phage_CPT_id='123')
        dest_dir = os.path.join(settings.MEDIA_ROOT, "images", p1.phage_name)
        docs_dest_dir = os.path.join(settings.MEDIA_ROOT, "docs", p1.phage_name)
        os.mkdir(dest_dir)
        os.mkdir(docs_dest_dir)
        self.client.login(username='testclient', password='sekret')
        data = {"name":"test22"}
        response = self.client.get('/view_phage/',data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()
        os.rmdir(dest_dir)
        os.rmdir(docs_dest_dir)

# class ManageTest(TestCase):
#     @override_settings(DJANGO_SETTINGS_MODULE = "lala.settings")
#     @override_settings(PYTHONPATH = "C://test")
#     def test_manage(self):
#         print(settings.DJANGO_SETTINGS_MODULE)
#         arg = "python manage.py show_urls"
#         cmd = "deactivate.bat %s" % arg
#         os.system(cmd)

class PhageDataTest(TestCase):
    def create_PhageData(self, title="only a test", body="yes, this is only a test"):
        return PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123')


    def test_PhageData_adv_search_name(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123')
        data = {
            'phage_name': 'test_pname'
        }
        self.client.login(username='testclient', password='sekret')
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()


    def test_PhageData_adv_search_host_name(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123', phage_host_name='hostA')
        data = {
            'phage_host_name': 'hostA'
        }
        self.client.login(username='testclient', password='sekret')
        response = self.client.post('/search_phage/', data, follow=True)
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()


    def test_PhageData_adv_search_iso_name(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        self.client.login(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123', phage_isolator_name='IsolatorA')
        data = {
            'phage_isolator_name': 'IsolatorA'
        }
        response = self.client.post('/search_phage/', data, follow=True)
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    def test_PhageData_adv_search_start_year(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        self.client.login(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123', phage_isolator_name='IsolatorA')
        data = {
            'submitted_year_gt': '-10'
        }
        response = self.client.post('/search_phage/', data, follow=True)
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    def test_PhageData_adv_search_end_year(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        self.client.login(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123', phage_isolator_name='IsolatorA')
        data = {
            'submitted_year_lt': '-10'
        }
        response = self.client.post('/search_phage/', data, follow=True)
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    def test_PhageData_adv_search_start_month(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        self.client.login(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123', phage_isolator_name='IsolatorA')
        data = {
            'submitted_month_gt': '-10'
        }
        response = self.client.post('/search_phage/', data, follow=True)
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    def test_PhageData_adv_search_end_month(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        self.client.login(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123', phage_isolator_name='IsolatorA')
        data = {
            'submitted_month_lt': '-10'
        }
        response = self.client.post('/search_phage/', data, follow=True)
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

class PhageDataLoginTest(TestCase):
    def create_PhageDataLogin(self, title="only a test", body="yes"):
        return PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123')

    def test_login1(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        dest_dir = os.path.join(settings.MEDIA_ROOT, "images")
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        response = self.client.get('/search_phage/', follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    def test_logged_in_index(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        self.client.login(username='testclient', password='sekret')
        p1 = PhageData.objects.create(phage_name='test_pname1', phage_CPT_id='1231', phage_isolator_name='IsolatorA')
        p2 = PhageData.objects.create(phage_name='test_pname2', phage_CPT_id='1232', phage_isolator_name='IsolatorB')
        p3 = PhageData.objects.create(phage_name='test_pname3', phage_CPT_id='1233', phage_isolator_name='IsolatorC')
        dest_dir = os.path.join(settings.MEDIA_ROOT, "images")
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)
        response = self.client.get('//', follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()

    def test_ChangePassword(self):
        user = User.objects.create_user(username='testclient', password='sekret')
        self.client.login(username='testclient', password='sekret')
        response = self.client.get('/change_password/')
        self.assertEqual(response.status_code, 200)
        data = {
            'old_password': 'sekret',
            'new_password1': 'testclient',
            'new_password2': 'testclient',
        }
        response = self.client.post('/change_password/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        user.delete()


class EditPhageDataTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        user = User.objects.create_user("test_user", 'testuser@test.com', 'pass@123')
        user.save()

    def create_EditPhageData(self, title="only a test", body="yes"):
        return PhageData.objects.create(phage_name='test_pname', phage_CPT_id='123')


    def test_EditPhageData1(self):
        self.client.login(username="test_user", password='pass@123')
        phage_desc = {"phage_name": "test_pname1", "phage_CPT_id": "test_123", "phage_lab": "Lab-A", "flag": 1}
        response = self.client.post('/add_phage/', phage_desc, follow=True)
        data = {
            'phage_name': 'test_pname1'
        }
        response = self.client.get('/view_phage/?name=test_pname1')
        self.assertEqual(response.status_code, 200)
        #response = self.client.get('/edit_details/', data, follow=True)
        response = self.client.get('/edit_details/?name=test_pname1')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/edit_details/?name=test_pname1', phage_desc, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/search_phage/', data, follow=True)
        self.assertEqual(response.status_code, 200)



    def test_EditPhageData2(self):
        self.client.login(username="test_user", password='pass@123')
        phage_desc = {"phage_name": "test_pname1", "phage_CPT_id": "test_123", "phage_lab": "Lab-A", "flag": 1}
        response = self.client.post('/add_phage/', phage_desc, follow=True)
        data = {
            'phage_name': 'test_pname1'
        }
        response = self.client.get('/view_phage/?name=test_pname1')
        self.assertEqual(response.status_code, 200)
        # response = self.client.get('/edit_details/', data, follow=True)
        response = self.client.get('/edit_details/?name=test_pname1')
        self.assertEqual(response.status_code, 200)

        data = {
                'phage_name' : 'test_pname1',
                'phage_host_name' : 'hostA',
                'phage_isolator_name' : 'IsolatorA',
                'phage_experimenter_name' : 'ScientistA',
                'phage_lab': '0',
                'phage_CPT_id' : 'test_123',
                'phage_isolator_loc' : 'texas',
                'owner' : 'someone',
                'owner_name' : 'else',
                'link' : "www.google.com",
                'flag': 1
               }
        search_data = {
            'phage_name': 'test_pname1'
        }
        response = self.client.post('/edit_details/?name=test_pname1', data, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/search_phage/', search_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_EditPhageData3(self):
        self.client.login(username="test_user", password='pass@123')
        phage_desc = {"phage_name": "test_pname1", "phage_CPT_id": "test_123", "phage_lab": "Lab-A", "flag": 1}
        response = self.client.post('/add_phage/', phage_desc, follow=True)
        data = {
            'phage_name': 'test_pname1'
        }
        response = self.client.get('/view_phage/?name=test_pname1')
        self.assertEqual(response.status_code, 200)
        # response = self.client.get('/edit_details/', data, follow=True)
        response = self.client.get('/edit_details/?name=test_pname1')
        self.assertEqual(response.status_code, 200)

        data = {
                'phage_name' : 'test_pname2',
                'phage_host_name' : 'hostA',
                'phage_isolator_name' : 'IsolatorA',
                'phage_experimenter_name' : 'ScientistA',
                'phage_lab': '0',
                'phage_CPT_id' : 'test_123',
                'phage_isolator_loc' : 'texas',
                'owner' : 'someone',
                'owner_name' : 'else',
                'link' : "www.google.com",
                'flag': 1
               }
        search_data = {
            'phage_name': 'test_pname2'
        }
        response = self.client.post('/edit_details/?name=test_pname1', data, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/search_phage/', search_data, follow=True)
        self.assertEqual(response.status_code, 200)


class UploadPhageDataTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        user = User.objects.create_superuser("test_user", 'testuser@test.com', 'pass@123')
        user.save()


    def test_UploadPhageData1(self):
        self.client.login(username="test_user", password='pass@123')
        response = self.client.get('/uploads/form/')
        self.assertEqual(response.status_code, 200)
        csv_path = os.path.join(settings.BASE_DIR, "test2.csv")
        data = {
            'title': 'Upload1',
            'file': csv_path
        }
        with open(csv_path) as fp:
            response = self.client.post('/uploads/form/', {'title': 'Upload1', 'file': fp})
        self.assertEqual(response.status_code, 200)

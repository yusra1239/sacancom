from django.test import TestCase
from django.test import TestCase, Client
from django.middleware.csrf import get_token

class SaveCardAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_csrf_protection(self):
        # الحصول على رمز CSRF
        response = self.client.get("/path-to-get-csrf-token/")  # استبدل بالمسار الصحيح
        csrf_token = get_token(response.wsgi_request)

        # إرسال طلب POST بدون رمز CSRF (يجب أن يفشل)
        response = self.client.post("/save-card/", data={}, content_type="application/json")
        self.assertEqual(response.status_code, 403)  # 403 Forbidden

        # إرسال طلب POST برمز CSRF (يجب أن ينجح)
        response = self.client.post(
            "/save-card/",
            data={},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=csrf_token,
        )
        self.assertEqual(response.status_code, 201)  # 201 Created
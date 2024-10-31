from django.shortcuts import redirect

class RedirectUnauthorizedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 401:
            # Redirect to the login page if 401 Unauthorized is encountered
            return redirect('/login')
        return response

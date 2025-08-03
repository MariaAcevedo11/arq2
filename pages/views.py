from django.shortcuts import render
from django.views import View
#from django.http import HttpResponse
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
#def homePageView(request):
    #return HttpResponse('Hello world!')


class HomePageView(TemplateView):
    template_name = "pages/home.html"

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: María Acevedo",
        })
        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact",
            "subtitle": "Contact us",
            "description": "Email: onlineStore@gmail.com | Address: 128 Mapple St "
            "| Phone number: +98 12389012312 "

        })
        return context    

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price" : 17},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price" : 18},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price" : 19},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price" : 101}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id) - 1]
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] = product["name"] + " - Product information"
            viewData["price"] = product["price"]
            viewData["product"] = product
            return render(request, self.template_name, viewData)
        except (IndexError, ValueError):
            # Redirige a la página principal si el id no es válido
            return HttpResponseRedirect(reverse('home'))


from django import forms
from django.shortcuts import render, redirect
from django.views import View

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("The price must be greater than 0.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            viewData = {
                "title": "Success"
            }
            return render(request, "products/success.html", viewData)
        else:
            viewData = {
                "title": "Create product",
                "form": form
            }
            return render(request, self.template_name, viewData)

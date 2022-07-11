import datetime

from django.shortcuts import render,redirect

from main.models import Category,Actor,Director,Movie,Review
from main.forms import MovieForm,DirectorForm,RegisterForm,LoginForm,
from django.contrib.auth import authenticate,login,logout
from django.views.generic import ListView,DetailView,FormView,
from django.views import View
# Create your views here.


class NewsView(View):
    def get(self,request):
        dict_={
           'key': 'Cartoons',
           'color': 'red',
           'list_': ["Maikraft", 'Tomy and Jery', 'Alady','Aktan Akylai']
        }
        return render(request,'news.html',context=dict_)
    def post(self,request):
        pass

# def movie_list_view(request):
#     context={
#        'movie_list': Movie.objects.all(),
#        'category_list': Category.objects.all()
#     }
#     return render(request, 'movie.html', context=context)
class ContextData():
    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['category_list']=Category.objects.all()
        return context


class MovieListView(ContextData,ListView):
    queryset = Movie.objects.all()
    template_name = 'movie.html'
    context_object_name = 'movie_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data()
        context['category_list']=Category.objects.all()
        return context


class MovieDetailView(ContextData,DetailView):
    model=Movie
    template_name = 'detail.html'
    context_object_name = 'movie_detail'
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['reviews']=Review.objects.filter(movie=self.object)
        return context

# def category_movie_filter_view(request,category_id):
#     context = {
#         'movie_list': Movie.objects.filter(category_id=category_id),
#         'category_list': Category.objects.all()
#     }
#     return render(request, 'movie.html', context=context)

class CategoryMovieFilterView(ContextData,ListView):
    queryset = Movie.objects.all()
    template_name = 'movie.html'
    context_object_name = 'movie_list'
    def get_queryset(self):
        return Movie.objects.filter(category_id=self.request.resolver_match.kwargs['category_id'])


class AddNewsView(ContextData,ListView  ):
     def add_news(self,request):
         print("  ..............           ")
         now = datetime.datetime.now()
         print(now)
         year = now.year
         month = now.month
         day = now.day
         if len(str(day)) == 1:
            day = "0"+str(day)
         if len(str(month)) == 1:
            month = "0"+str(month)
         print(year, month, day)
         print(" .........               ")
     pass




class NationalView(View):
    def get(self, request):
        return render(request, 'national.html')

class ChildrenView(View):
    def get(self, request):
        return render(request,'children.html')

   

class AddMovieFormView(ContextData,FormView):
    form_class = MovieForm()
    template_name = 'add_movie.html'
    success_url = '/movie'

    def form_valid(self, form):
        form.save()
        return super().form_valid()




class AddDirectorFormView(ContextData,FormView):
    form_class = MovieForm()
    template_name = 'add_director.html'
    success_url = '/movie'

    def form_valid(self, form):
        form.save()
        return super().form_valid()


# def register_view(request):
#     form = RegisterForm()
#     if request.method == 'POST':
#         form = RegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/register/')
#     return render(request, 'register.html', context={
#         'form': form
#     })
class RegisterFormView():
    form_class = RegisterForm()
    template_name = 'register.html'
    success_url = '/register'

    def form_valid(self, form):
        form.save()
        return super().form_valid()

    @classmethod
    def as_view(cls):
        pass


# def login_view(request):
#     form = LoginForm()
#     if request.method=='POST':
#         form=LoginForm(data=request.POST)
#         if form.is_valid():
#             username=form.cleaned_data['username']
#             password=form.cleaned_data['password']
#             user=authenticate(username=username,password=password)
#             if user:
#                 login(request,user=user)
#         return redirect('/login/')
#     return render(request, 'login.html',context={
#         'form': form
#     })
class LoginView(View):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.POST = None
        self.method = None

    def login_view(request):
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user=user)
            return redirect('/login/')
        return render(request, 'login.html', context={
            'form': form
        })
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('/login/')
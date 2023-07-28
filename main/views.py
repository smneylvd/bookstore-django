from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from main.models import User, Book, RentList


# Create your views here.

def index(req):
    if not req.user.is_authenticated:
        return redirect("login")
    q = ''
    books = Book.objects.all()
    if req.GET:
        q = req.GET['q']
        books = Book.objects.filter(name__contains=q)
    return render(req, 'index.html', {'books': books, 'q': q})


def rentBook(req, book_id):
    if not req.user.is_authenticated:
        return redirect("login")
    book = Book.objects.get(id=book_id)

    if not book:
        messages.error(req, "Incorrect book id")
        return redirect("index")

    rentList = RentList(book=book, user=req.user)
    rentList.save()
    book.status = True
    book.save()
    return redirect("favourites")


def removeRent(req, book_id):
    if not req.user.is_authenticated:
        return redirect("login")
    book = Book.objects.get(id=book_id)

    if not book:
        messages.error(req, "Incorrect book id")
        return redirect("index")

    rentList = RentList.objects.get(book=book, user=req.user)
    rentList.delete()
    book.status = False
    book.save()
    return redirect("favourites")


def bookDetails(req, book_id):
    if not req.user.is_authenticated:
        return redirect("login")
    book = Book.objects.get(id=book_id)

    if not book:
        messages.error(req, "Incorrect book id")
        return redirect("index")
    c = int(book.rating)
    rating = []
    for i in range(c):
        rating.append(1)
    for i in range(10 - c):
        rating.append(0)
    user = ''
    try:
        rent = RentList.objects.get(book=book)
        if rent:
            user = rent.user
    except:
        pass
    return render(req, "book.html", {"book": book, "rating": rating, 'current_owner': user})


def favourites(req):
    book_ids = []
    rent_list = RentList.objects.filter(user=req.user).values("book_id")
    for i in rent_list:
        book_ids.append(i['book_id'])
    books = Book.objects.filter(id__in=book_ids)
    return render(req, "favourites.html", {'books': books})


def login_view(req):
    if req.method == "POST":
        try:
            user = authenticate(req, nickname=req.POST['nickname'], password=req.POST['password'])
            login(req, user)
            return redirect('index')
        except:
            messages.error(req, "Incorrect username or password")
            return render(req, 'login_page.html')

    return render(req, 'login_page.html')


def logout_view(req):
    logout(req)
    return redirect('index')


def register(req):
    if req.method == "POST":
        try:
            first_name = req.POST['firstname']
            last_name = req.POST['lastname']
            email = req.POST['email']
            nickname = req.POST['nickname']
            password = req.POST['password']
            user = User(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        nickname=nickname)
            user.set_password(password)
            user.save()
        except:
            messages.error(req, "Email address or nickname is duplicated, try to use another one")
            return render(req, "register_page.html")
        return redirect('login')
        # print(first_name, last_name, email, phone, nickname, password)
    return render(req, "register_page.html")

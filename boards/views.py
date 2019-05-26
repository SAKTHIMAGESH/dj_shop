from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Board
import MySQLdb
import random
from .forms import PasswordUpdate,Forgotp,LoginForm,RegisterForm,AddProduct
from django.core.mail import send_mail
def board_topics(request, pk):
    # board = Board.objects.get(pk=pk)
    # return render(request, 'topics.html', {'board': board})
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})

def home1(request):
	if 'logout' in request.POST:
		print("session destroyed")
		# del request.sesssion['mail']
		del request.session['user']
		return redirect('login')
	return render(request,"index.html",{"user":request.session['user']})

def admin1(request):
	return render(request,"admin.html",{})
def passwordupdate(request):
	pup=PasswordUpdate(request.POST or None)
	context_={"form":pup}
	if pup.is_valid():
		password=pup.cleaned_data.get("password")
		cpassword=pup.cleaned_data.get("password1")
		if 'update' in request.POST and password == cpassword:
			print(request.session['mail'])
			print(password)
			db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="register",port=3306)
			c=db.cursor()
			c.execute("""UPDATE user set password=%s where email=%s""",(password,request.session['mail'],))	
			c.execute("""UPDATE forgot set active=%s where mail=%s""",(1,request.session['mail'],))
			c.execute("""DELETE from forgot where active=1""")
			del request.session['mail']
			db.commit()
			c.close()
			db.close()	
			return redirect('login')
	return render(request,'pupdate.html',context_)

def forgot(request):
	forgotp=Forgotp(request.POST or None)
	context_={"form":forgotp}
	if forgotp.is_valid():
		mail=forgotp.cleaned_data.get("mail")
		otp=forgotp.cleaned_data.get("otp")
		otpp=random.randint(1111,9999)
		db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="register",port=3306)
		c=db.cursor()
		if 'go' in request.POST:
			c.execute("""INSERT INTO forgot ( mail,otp,active) VALUES (%s,%s,%s)""",(mail,otpp,0,))
			send_mail('OTP', str(otpp), 'sakthimagesh2199@gmail.com', [mail,])
		elif 'ro' in request.POST:
			print("dummy")
			rotp=random.randint(1111,9999)
			print(rotp)
			print(mail)
			c.execute("""UPDATE forgot set otp=%s where mail=%s""",(rotp,mail,))
			
		else:
			print(otp)
			request.session['mail']=mail
			c.execute("""SELECT otp from forgot where mail=%s""",(mail,))
			db_otp=c.fetchone()
			if db_otp[0] == otp:
				return redirect('pupdate')
			else:
				print('not same')
		c.close()
		db.commit()
		db.close()
	return render(request,'forgot.html',context_)	



def add(request):
    add_p=AddProduct(request.POST or None)
    context_={"form":add_p}
    uploaded_file_url=""
    # print(add_p.cleaned_data.get("productprice"))
    if add_p.is_valid():
    	productname=add_p.cleaned_data.get("productname")
    	productprice=add_p.cleaned_data.get("productprice")
    	productdescription=add_p.cleaned_data.get("productdescription")
    	if request.FILES['myfile']:
    	 myfile = request.FILES['myfile']
    	 fs = FileSystemStorage()
    	 filename = fs.save(myfile.name, myfile)
    	 uploaded_file_url = fs.url(filename)
    	 # return render(request, 'upload.html', {"form":add_p,'uploaded_file_url': uploaded_file_url})
    	print(productname)
    	print(productprice)
    	print(productdescription)
    	print(uploaded_file_url)
    	db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="register",port=3306)
    	c=db.cursor()
    	c.execute("""INSERT INTO product (pr_na, pr_pr, pr_de, pr_im)
    	 VALUES (%s,%s,%s,%s)""",(productname,1000,productdescription,uploaded_file_url,))
    	c.close()
    	db.commit()
    	db.close()
    return render(request, 'upload.html',{"form":add_p,'uploaded_file_url': uploaded_file_url})

User=get_user_model()

def register(request):
	register=RegisterForm(request.POST or None)
	context_={
	"form":register
	}
	if register.is_valid():
		# print(register.cleaned_data)
		username=register.cleaned_data.get("username")
		mobileno=register.cleaned_data.get("mobile_no")
		country_code=register.cleaned_data.get("")
		email=register.cleaned_data.get("email")
		password=register.cleaned_data.get("password")
		new_user=User.objects.create_user(username,email,password)
		# print(country_code)
		print(mobileno)
		print(email)
		print(username)
		print(password)
		print(new_user)
		db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="register",port=3306)
		c=db.cursor()
		c.execute(" INSERT INTO user (name, mobile, email, password) VALUES (%s,%s,%s,%s) ",(username,mobileno,email,password,))
		otp=random.randint(1111,9999)
		otp_msg="your otp is "+str(otp)
		c.execute(" INSERT INTO ver (mail, otp, active) VALUES (%s,%s,%s) ",(email,otp,0,))
		c.close()
		db.commit()
		db.close()
		print(otp_msg)
		send_mail('OTP', otp_msg, 'sakthimagesh2199@gmail.com', ['vickypotter2516@gmail.com','veeramsakthi2199@gmail.com',])
		return redirect('login')
	return render(request,'auth/register.html',context_)

def products(request):
		
		db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="register",port=3306)
		c=db.cursor()
		productname=[]
		productprice=[]
		productdescription=[]
		a=c.execute("""SELECT * FROM product""")
		products=[]
		price=[]
		des=[]
		im=[]
		while a > 0:
			i=0
			i+=1
			print(a)
			product=c.fetchone()
			print(product)
			# print()	
			productname=product[0]
			productprice=product[1]
			productdescription=product[2]
			productimg="127.0.0.1:8000"+product[3]
			products.append(('names',productname))	
			price.append(('price',productprice))
			des.append(('des',productdescription))
			im.append(('img',productimg))
			# product_1.append(products)
			a-=1
			# print("127.0.0.1:8000"+productimg)
			# productname=product[0]
			# productprice=product[1]
			# productdescription=product[2]
		# print(product_1)
		return render(request,"product.html",{'name':products,'price':price,'des':des,'im':im})


def loginpage(request):
	
	login_form=LoginForm(request.POST or None)
	context_={"form":login_form}
	if login_form.is_valid():
		print(login_form.cleaned_data)
		username=login_form.cleaned_data.get("username")
		password=login_form.cleaned_data.get("password")
		context_['form']=LoginForm()
		db=MySQLdb.connect(host="127.0.0.1",user="root",passwd="",db="register",port=3306)
		c=db.cursor()
		a=c.execute("""SELECT name,password FROM user WHERE name = %s AND password = %s""", (username,password,))
		# print(c.fetchone())
		b=c.fetchone()
		print(a)
		if a == 1:
			# user=authenticate(request,username=username,password=password)
			# print(user)
			# if user is not None:
			request.session['user']=b[0]
				# login(request,user)
			return redirect('/')
			# else:
			# 	print("Error")
		# print(False)
		if a is None and username == 'admin' and password == 'admin':
			# print(True)
			return redirect('admin1')

		# if request.method=="POST":
	# 	if request.POST.get("username")=="admin" and request.POST.get("password")=="admin":
	# 		# context_={"response":"Login Successfull"}
	# 		home1(request)
	# 	else:
	# 		context_={"response":"Login Failed"}
	context_={"form":login_form}
	return render(request,"auth/login.html",context_)

def home(request):
    # boards = Board.objects.all()
    # boards_names = list()

    # for board in boards:
    #     boards_names.append(board.name)

    # response_html = '<br>'.join(boards_names)

    # return HttpResponse(response_html)
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})
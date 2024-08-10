from django.shortcuts import render, HttpResponse, redirect
from shop.models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from django.utils.crypto import get_random_string

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, "home.html", {})

def notauth(request):
    return render(request, "not.html", {})
    


@login_required(login_url="/loginFirst")
def name_list(request):
    all_users = User.objects.all()
    deetails = UserDetails.objects.all()
    data = {"auth_users": all_users, "deets": deetails}
    return render(request, "free/index.html", context=data)



def update_customer_view(request):
    cus_instance = User.objects.get(id=request.user.id)
    data = {"cus_instance": cus_instance}
    messages.info(request, "update")
    return render(request, "free/updateUser.html", context=data)

# under progress
# def update_customer(request):
#     if (
#         request.method == "POST"
#         and request.POST["fname"]
#         and request.POST["lname"]
#         and request.POST["email"]
#         and request.POST["address"]
#     ):
#         user_id = request.user.id
#         cus = User.objects.filter(email=request.POST["email"])
#         if cus.exists() and cus.count() == 1:
#             get_cus = User.objects.get(email=request.POST["email"])
#             if get_cus.id == user_id:
#                 get_cus.fname = request.POST["fname"]
#                 get_cus.lname = request.POST["lname"]
#                 get_cus.email = request.POST["email"]
#                 get_cus.address = request.POST["address"]
#                 get_cus.save()
#                 messages.success(request, "customer updated successfuly")
#                 return redirect("/name_list")
#             else:
#                 messages.error(request, "The email you used already exist")
#                 return redirect("/name_list")
#         else:
#             cus_instance = Customer.objects.get(id=id)
#             cus_instance.fname = request.POST["fname"]
#             cus_instance.lname = request.POST["lname"]
#             cus_instance.email = request.POST["email"]
#             cus_instance.address = request.POST["address"]
#             cus_instance.save()
#             messages.success(request, "updated ok")
#             return redirect("/name_list")
#     else:
#         messages.error(request, " please enter details")
#         return redirect("/name_list")


def delete_view(request):
    try:
        id = request.user.id
        cus_instance = User.objects.get(id=id)
        data = {"delete_request": cus_instance}
        messages.warning(request, "delete")
        return render(request, "free/delete.html", context=data)
    except ObjectDoesNotExist:
        messages.error(request, "ID does not exist")
        return redirect("/name_list")


def delete(request):
    id = request.user.id
    delete_request = User.objects.get(id=id).delete()
    if delete_request:
        messages.success(request, "delete okay")
        return redirect("/name_list")
    else:
        messages.error(request, " there was an error and nothing was deleted")
        return redirect("/name_list")


@login_required(login_url="/loginFirst")
def items_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Not Authorized to view that page")
        return redirect("/name_list")
    items = Items.objects.all()
    data = {"items": items}
    messages.warning(request, "THIS TAB IS FOR ADMINS ONLY")
    return render(request, "free/items.html", context=data)


def reg_items(request):
    if not request.user.is_superuser:
        messages.error(request, "Not Authorized to view that page")
        return redirect("/name_list")
    if (
        request.method == "POST"
        and request.POST["itemName"]
        and request.POST["unitprice"]
        and request.POST["stock"]
    ):
        if Items.objects.filter(itemName=request.POST["itemName"]).exists():
            messages.warning(request, "The item you entered already exist")
            return redirect("/name_list")
        else:
            create_item = Items(
                itemName=request.POST["itemName"],
                unitprice=request.POST["unitprice"],
                stock=request.POST["stock"],
            )
            create_item.save()
            messages.success(request, " item created ok")
            return redirect("/items_view")
    else:
        messages.error(request, " please enter details")
        return redirect("/items_view")


def update_items_view(request, id):
    items_instance = Items.objects.get(id=id)
    data = {"items_instance": items_instance}
    messages.info(request, "update")
    return render(request, "free/updateItems.html", context=data)


def update_items(request, id):
    if (
        request.method == "POST"
        and request.POST["itemName"]
        and request.POST["unitprice"]
        and request.POST["stock"]
    ):
        check = Items.objects.filter(itemName=request.POST["itemName"])
        if check.exists() and check.count() == 1:
            item = Items.objects.get(itemName=request.POST["itemName"])
            if item.id == id:
                item.itemName = request.POST["itemName"]
                item.unitprice = request.POST["unitprice"]
                item.stock = request.POST["stock"]
                item.save()
                messages.success(request, "item updated ok")
                return redirect("/items_view")
            else:
                messages.error(request, "item already exist")
                return redirect("/items_view")
        else:
            item = Items.objects.get(id=id)
            item.itemName = request.POST["itemName"]
            item.unitprice = request.POST["unitprice"]
            item.stock = request.POST["stock"]
            item.save()
            messages.success(request, "item updated ok")
            return redirect("/items_view")
    else:
        messages.error(request, " please enter details")
        return redirect("/items_view")


def is_in_banned_group(user):
    banned_group, _ = Group.objects.get_or_create(name="banned")
    return not banned_group.user_set.filter(id=user.id).exists()

   
@user_passes_test(is_in_banned_group, login_url="/notauth")
def neworder_view(request):
    cus_id = request.user.id
    items = Items.objects.all()
    cus_instance = User.objects.get(id=cus_id)
    orders = Order.objects.filter(customer=cus_instance)
    if orders:
        data = {"cus_instance": cus_instance, "items": items, "orders": orders}
        return render(request, "free/orders.html", context=data)
    else:
        messages.warning(request, "no orders yet")
        data = {"cus_instance": cus_instance, "items": items, "orders": False}
        return render(request, "free/orders.html", context=data)


# for the new default user model
def newreg_order(request):
    cus_id = request.user.id
    if request.method == "POST" and request.POST["id"] and request.POST["quantity"]:
        item_instance = Items.objects.get(id=request.POST["id"])
        if item_instance.stock >= int(request.POST["quantity"]):
            deliver_state = request.POST.get("deliver", False)
            cus_instance = User.objects.get(id=cus_id)
            amount = int(request.POST["quantity"]) * int(
                    item_instance.unitprice
                )
            if deliver_state:
                cal_amount = amount + int(10)
            else:
                cal_amount = amount

            create_order = Order(
                customer=cus_instance,
                item=item_instance,
                quantity=request.POST["quantity"],
                amount= amount,
                total_amount= cal_amount,
                deliver=deliver_state,
            )
            create_order.save()
            messages.success(request, " your order created succesfuly")
            return redirect("/neworder_view")
        else:
            messages.warning(request, " not enough in stock")
            return redirect("/neworder_view")
    else:
        messages.error(request, "something went wrong please enter item")
        return redirect("/neworder_view")


def delete_order(request, ord_id):
    delete_request = Order.objects.get(id=ord_id)

    if delete_request:
        cus_id = delete_request.customer
        delete_request.delete()
        messages.success(request, "delete order okay")
        return redirect(f"/neworder_view/{cus_id.id}")
    else:
        messages.error(request, " there was an error and nothing was deleted")
        return redirect("/name_list")


def payment_history(request, cus_id):
    try:
        payments = Payment.objects.filter(customer=cus_id)
        data = {"payments": payments, "cus_id": cus_id}

        return render(request, "free/paymentHistory.html", context=data)
    except ObjectDoesNotExist:
        messages.error(request, "ID does not exist")
        return redirect("/name_list")
    
def history_admin(request):
    try:
        payments = Payment.objects.all()
        data = {"payments": payments, }

        return render(request, "free/history_admin.html", context=data)
    except ObjectDoesNotExist:
        messages.error(request, "ID does not exist")
        return redirect("/name_list")

# new
def payment_page(request):
    
    if request.method == "POST" and request.POST["order_id"]:
        payment_order = Order.objects.get(id=request.POST["order_id"])
        return render(request, "free/payments.html", {"payment_order": payment_order})
    else:
        messages.error(request, "something went wrong ")
        return redirect("neworder_view")

def payment_view(request):
    if (
        request.method == "POST"
        and request.POST["recipientname"]
        and request.POST["email"]
        and request.POST["address"]
        and request.POST["country"]
        and request.POST["state"]
        and request.POST["paymentmethod"]
        and request.POST["card_name"]
        and request.POST["card_number"]
        and request.POST["exp"]
        and request.POST["cvv"]
        and request.POST["order_id"]
        and request.POST["item_id"]
    ):
        emp_instance = User.objects.get(id=request.user.id)
        order_inst = Order.objects.get(id=request.POST["order_id"])
        item_inst = Items.objects.get(id=request.POST["item_id"])
        
        if order_inst.quantity > item_inst.stock :
            messages.warning(request, 'not enough in stock, please reoder' )
            return redirect('neworder_view')
        else:
            paymentmethod = PaymentMethod(
                method = order_inst,
                pay_method =request.POST["paymentmethod"],
                name = request.POST["card_name"],
                card_number = request.POST["card_number"],
                cvv = request.POST["cvv"],
                exp_date = request.POST["exp"]
            ) 
            paymentmethod.save()
            recipient = Recipient(
                recipient= order_inst,
                names = request.POST["recipientname"],
                email = request.POST["email"],
                ship_county = request.POST["country"],
                ship_state = request.POST["state"],
                ship_address = request.POST["address"]
            )
            recipient.save()
            payment = Payment(
                customer=emp_instance,
                order = order_inst,
                amount = order_inst.total_amount,
                status= True
            )
            payment.save()
            order_inst.status=True
            order_inst.save()
            
            newstock= int(item_inst.stock) - int(order_inst.quantity)
            item_inst.stock = newstock
            item_inst.save()
            
        messages.success(request, ' paid sussess ')
        return redirect("neworder_view")
    else:
        messages.warning(request, "please enter all details ")
        return redirect("payment_page")


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser, login_url="/notauth")
def toggle_ban_user(request):
    if request.method == "POST" and request.POST["user_id"]:
        user_id = request.POST["user_id"]
        user_to_toggle = User.objects.get(id=user_id)
        banned_group, _ = Group.objects.get_or_create(name="banned")

        # Check if the user is already in the banned group
        if banned_group.user_set.filter(id=user_id).exists():
            # User is already banned, so unban them
            banned_group.user_set.remove(user_to_toggle)
            ban_status = UserDetails.objects.get(user=user_to_toggle)
            ban_status.status = False
            ban_status.save()
          
            messages.info(request, "user unbanned")
        else:
            # User is not banned, so ban them
            banned_group.user_set.add(user_to_toggle)
            ban_status = UserDetails.objects.get(user=user_to_toggle)
            ban_status.status = True
            ban_status.save()
            messages.info(request, "user banned")

        return redirect("/name_list")
    else:
        messages.warning(request, "user not toggled")
        return redirect("/name_list")


def signup_view(request):
    messages.info(request, "Please provide information to be Registered")
    return render(request, "authenticate/signup.html", {})


def signup(request):
    if (
        request.method == "POST"
        and request.POST["first_name"]
        and request.POST["last_name"]
        and request.POST["email"]
        and request.POST["password"]
        and request.POST["username"]
        and request.POST["address"]
        and request.POST["contact"]
        and request.POST["gender"]
    ):
        if User.objects.filter(email=request.POST["email"]).exists():
            messages.warning(request, "The email you used already exist")
            return redirect("/signup")
        else:
            user_inst = User.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
            )
            user_inst.save()
            details = UserDetails(
                user=user_inst,
                contact=request.POST["contact"],
                address=request.POST["address"],
                gender=request.POST["gender"],
            )
            details.save()

            messages.success(request, "user sign in ok")
            data = {"user_detail": user_inst}
            return render(request, "authenticate/login.html", context=data)
    else:
        messages.error(request, " please enter details")
        return redirect("/signup_view")


def login_view(request):
    all_users = User.objects.all()
    data = {"persons": all_users}
    return render(request, "authenticate/login.html", context=data)


def log_in(request):
    if (
        request.method == "POST"
        and request.POST["password"]
        and request.POST["username"]
    ):
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            messages.success(request, "log in successful !")
            return redirect("/name_list")

        else:
            messages.error(request, "Account with these details Not FOund !")
            return redirect("/login_view")

    else:
        messages.error(request, " please enter correct details")
        return redirect("/signup")


def loginFirst(request):
    messages.warning(request, "please login first")
    return redirect("/login_view")


def logout_view(request):
    logout(request)
    messages.success(request, "logged out, see you another time")
    return redirect("/login_view")


def sendemail(request):
    if (
        request.method == "POST"
        and request.POST["subject"]
        and request.POST["message"]
        and request.POST["toemail"]
    ):
        try:
            send_mail(
                subject= request.POST["subject"],
                message=request.POST["message"],
                from_email="afanwitelvin@gmail.com",
                recipient_list=[request.POST["toemail"]],
                fail_silently=False,
            )
            messages.success(request, "email sent")
            return redirect("/name_list")
        except Exception as err:
            messages.error(request, f"Error sending email: {err}")
            return redirect("/name_list")

    else:
        messages.warning(request, "wrong")
        return redirect("/items_view")


def emailVerification_sign_up(request):
    if (
        request.method == "POST"
        and request.POST["first_name"]
        and request.POST["last_name"]
        and request.POST["email"]
        and request.POST["password"]
        and request.POST["username"]
        and request.POST["address"]
        and request.POST["contact"]
        and request.POST["gender"]
    ):
        if User.objects.filter(email=request.POST["email"]).exists():
            messages.warning(request, "The email you used already exist")
            return redirect("/signup")
        else:
            client_email = request.POST["email"]
            code = get_random_string(4, "1234567890")
            tempdata = Tempstore(
                fname=request.POST["first_name"],
                lname=request.POST["last_name"],
                email=request.POST["email"],
                password=request.POST["password"],
                username=request.POST["username"],
                address=request.POST["address"],
                contact=request.POST["contact"],
                gender=request.POST["gender"],
                code=code,
            )
            tempdata.save()
            send_email_verification(useremail=client_email, usercode=code)
            return redirect("/verification_view")
    else:
        messages.error(request, " please enter all the  details")
        return redirect("/signup_view")


def login_verify_view(request):

    return render(request, "authenticate/login_verify.html", {})


def login_email_verify(request):
    if (
        request.method == "POST"
        and request.POST["password"]
        and request.POST["username"]
    ):
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
            )
          
        if user is not None:
            client = User.objects.get(username=request.POST["username"])
            client_email = client.email
            code = get_random_string(4, "1234567890")
            send_email_verification(useremail=client_email, usercode=code)
            messages.info(request, "enter the 4 digit code to login")
            data = {
                "code_check": code,
                "passwordsend": request.POST["password"],
                "usernamesend": request.POST["username"],
            }
            return render(request, "authenticate/login_verify.html", context=data)
            
        else:
                messages.error(request, "user not found !")
                return redirect("/login_view")


def login_proper(request):
    if (
        request.method == "POST"
        and request.POST["passcode"]
        and request.POST["correctcode"]
        and request.POST["password"]
    ):
        if request.POST["passcode"] == request.POST["correctcode"]:
            user = authenticate(
                request,
                username=request.POST["username"],
                password=request.POST["password"],
            )
        
            login(request, user)
            messages.success(request, "log in successful !")
            return redirect("/name_list")
          
        else:
            messages.error(request, "wrong code !")
            return redirect("/login_view")
    else:
        messages.error(request, "enter all details !")
        return redirect("/login_view")


def send_email_verification(useremail, usercode):
    try:
        # send_mail(
        #     subject="email_verification",
        #     message= f'Your OTP IS {usercode}',
        #     from_email="afanwitelvin@gmail.com",
        #     recipient_list=[useremail],
        #     fail_silently=False, 
        # )
        print(f"email verification code {usercode} sent to {useremail}")
    except Exception as err:
        messages.error(f"Error sending email: {err}")
        return redirect("/verification_view")


def verification_view(request):
    messages.success(request, "fill in the 4 digit code to verify your email account")
    return render(request, "authenticate/everification.html", {})


def verification_proper(request):
    if request.method == "POST" and request.POST["passcode"]:
        if Tempstore.objects.filter(code=request.POST["passcode"]).exists():
            tempdata = Tempstore.objects.get(code=request.POST["passcode"])
            user_inst = User.objects.create_user(
                username=tempdata.username,
                email=tempdata.email,
                password=tempdata.password,
                first_name=tempdata.fname,
                last_name=tempdata.lname,
            )

            user_inst.save()
            details = UserDetails(
                user=user_inst,
                contact=tempdata.contact,
                address=tempdata.address,
                gender=tempdata.gender,
            )
            details.save()
            tempdata.delete()
            messages.success(request, "user email verification done in ok")
            data = {"user_detail": user_inst}
            return render(request, "authenticate/login.html", context=data)
        else:
            messages.warning(request, "email verification not correct")
            return redirect("/verification_view")
    else:
        messages.warning(request, "please enter email verification code")
        return redirect("/verification_view")

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "afanwitelvin@gmail.com",
            "Name": "Telvin Priestley Asanji"
        },
        "To": [
            {
            "Email": "afanwi.at@gmail.com",
            "Name": "Telvin Priestley Asanji"
            }
        ],
        "Subject": "Greetings from Mailjet.",
        "TextPart": "My first Mailjet email",
        "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you! <q> <a href='http://127.0.0.1:8000/'>app</a> </p>",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print (result.status_code)
    print (result.json()) 
    messages.info(request, f'{result.status_code}')
    messages.info(request, f'{result.json()}')
    return redirect('name_list')
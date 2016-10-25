from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from mainapp.models import Accounts, Users_Accounts, Balances, Documents
from datetime import date, datetime

# Create your views here.
def start(request):
    return render_to_response('main.html', {'username' : auth.get_user(request).username})

def accounts(request):
    args = {}
    args.update(csrf(request))

    args['username'] = auth.get_user(request).username
    accounts = Accounts.objects.all()
    for account in accounts:
        account.balance = '{:.2f}'.format(float(Balances.objects.filter(id_account=account.id).latest('dt').balance) / 100.00)
    args['accounts'] = accounts
    return render_to_response('accounts.html', args)

def account(request, id_account):
    args = {}
    args.update(csrf(request))
    documents = Documents.objects.filter(id_account=id_account)
    for document in documents:
        document.amount = '{:.2f}'.format(float(document.amount) / 100.00)


    args['documents'] = documents
    args['account'] = Accounts.objects.get(id=id_account)
    args['username'] = auth.get_user(request).username
    args['balance'] = '{:.2f}'.format(float(Balances.objects.filter(id_account=id_account).latest('dt').balance) / 100.00)
    return render_to_response('account.html', args)

def doc(request, id):
    args = {}
    args.update(csrf(request))
    document = Documents.objects.get(id=id)
    document.amount = '{:.2f}'.format(float(document.amount) / 100.00)
    document.dt = datetime.strptime(document.dt, '%Y/%m/%d %H:%M:%S')
    document.dt_bank = datetime.strptime(document.dt_bank, '%Y/%m/%d %H:%M:%S')
    args['document'] = document
    args['username'] = auth.get_user(request).username
    return render_to_response('doc.html', args)

def doc2pdf(request, id):
    args = {}
    document = Documents.objects.get(id=id)
    document.amount = document.amount / 100
    filename = file.pdf

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

def convert_int2text (number):
    number_str = str(number)
    number_int = int(number)
    number_range = number_int // 3
    while  number_range != 0:
        number_text = convert_int2text (number)
        number_range -=1
    return result

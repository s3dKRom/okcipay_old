from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from mainapp.models import Accounts, Users_Accounts, Balances, Documents, Currencies, Banks, Users
from datetime import date, datetime
from django.utils import formats

# Create your views here.
def start(request):
    return render_to_response('main.html', {'username' : auth.get_user(request).username})

def accounts(request):
    args = {}
    args.update(csrf(request))

    args['username'] = auth.get_user(request).username
    if auth.get_user(request).is_superuser:
        accounts = Accounts.objects.all()
    else:
        user = Users.objects.get(code=args['username'])
        accounts = Accounts.objects.filter(users_accounts__id_client=user)
    for account in accounts:
        account.balance = '{:.2f}'.format(float(Balances.objects.filter(id_account=account.id).latest('dt').balance) / 100.00)
        account.currency = Currencies.objects.get(code_currency=account.currency)
    args['accounts'] = accounts
    return render_to_response('accounts.html', args)

def account(request, id_account):
    args = {}
    args.update(csrf(request))
    dt_now = datetime.now(tz=None)
    start_dt = end_dt = formats.date_format(dt_now, "Y-m-d")
    args['dt_now'] = dt_now
    if request.method == 'POST':
        start_dt = request.POST['start_dt']
        end_dt = request.POST['end_dt']
    args['start_dt'] = start_dt
    args['end_dt'] = end_dt

    documents = Documents.objects.filter(id_account=id_account).filter(dt__gte=start_dt)
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
    document.words_amount = convert_num2text(document.amount)
    document.amount = '{:.2f}'.format(float(document.amount) / 100.00)
    document.dt = datetime.strptime(document.dt, '%Y-%m-%d')
    document.dt_bank = datetime.strptime(document.dt_bank, '%Y/%m/%d %H:%M:%S')
    document.bank_name_a = Banks.objects.get(code_bank=document.code_bank_a).bank_name
    document.bank_name_b = Banks.objects.get(code_bank=document.code_bank_b).bank_name
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

def convert_num2text(number):
    """ Функція для перетворення числа копійок в грошову суму словами. Число-аргумент може бути як в числовій так і в строковій формі.
        Функція приймає один аргумент number (може бути як str так і int): максимальне число 14 знаків.
        Функція повертає результат str"""

    """ Задаємо необхідні закінчення для сум"""
    kopeks = (u'копійок', u'копійка', u'копійки', u'копійки', u'копійки',)
    currency = (u'грн.', u'гривня', u'гривні', u'гривні', u'гривні', u'гривень',)

    thousand = (u'тисяч', u'тисяча', u'тисячі', u'тисячі', u'тисячі', u'тисяч',)
    million = (u'мільйонів', u'мільйон', u'мільйони', u'мільйони', u'мільйони', u'мільйонів',)
    billion = (u'мільярдів', u'мільярд', u'мільярди', u'мільярди', u'мільярди', u'мільярдів',)

    """ Локалізуємо змінні """
    number_str = str(number)
    number_int = int(number)
    number_len = len(number_str)

    """ Обнулюємо змінні """
    number_text = ''
    amount_kopeks = ''
    amount_currency = ''
    amount_thousand = ''
    amount_million = ''
    amount_billion = ''

    """ Перевіримо чи аргумент функції не перевищує 14 знаків """
    if number_len > 14:
        number_text = 'Будьте уважні! Максимальне число знаків може бути не більше 14!'
        return number_text

    """ Створюємо допоміжну функцію, яка переводить тризначне число в суму словами і добавляє в кінці відповідне закінчення.
        В функцію передаємо три аргументи: args[0] -- закінчення для суми, початкове (args[1]) і кінцеве (args[2]) значення для зрізу в number_str
        Функція повертає результат str"""
    def amount_helper(*args):
        result = ''
        result = str(convert_number_under_1000_2_text(number_str[args[1]:(args[2] + 1)]))
        if int(number_str[args[2]]) < 5:
            result += args[0][int(number_str[args[2]])]
        else:
            result += args[0][5]
        return result

    """ Формуємо суму копійок"""
    amount_kopeks = number_str[-2:] + ' коп.'


    """ Формуємо суму гривень"""
    if number_len > 2:
        if int(number_str[-5:-2]) != 0:
            amount_currency = amount_helper(currency, -5, -3)
        else:
            amount_currency = currency[0]
    else:
        amount_currency = str(convert_number_under_1000_2_text(0)) + currency[0]

    """ узгоджуємо відмінки для одиниць """
    if (amount_currency.find('один ') + 1):
        amount_currency = amount_currency.replace('один ', 'одна ')
    if (amount_currency.find('два ') + 1):
        amount_currency = amount_currency.replace('два ', 'дві ')

    """ Формуємо суму тисяч"""
    if number_len > 5 and int(number_str[-8:-5]) != 0:
        amount_thousand = amount_helper(thousand, -8, -6)

    """ узгоджуємо відмінки для тисяч """
    if (amount_thousand.find('один ') + 1):
        amount_thousand = amount_thousand.replace('один ', 'одна ')
    if (amount_thousand.find('два ') + 1):
        amount_thousand = amount_thousand.replace('два ', 'дві ')

    """ Формуємо суму мільйонів"""
    if number_len > 8 and int(number_str[-11:-8]) != 0:
        amount_million = amount_helper(million, -11, -9)

    """ Формуємо суму мільярдів"""
    if number_len > 11 and int(number_str[-14:-11]) != 0:
        number_str = '0' + number_str
        amount_billion = amount_helper(billion, -14, -12)

    """ Формуємо результат"""
    number_text = amount_billion + ' ' + amount_million + ' ' + amount_thousand + ' ' + amount_currency + ' ' + amount_kopeks
    result = number_text.capitalize()


    return result

""" Створюємо допоміжну функцію, яка переводить тризначне число в суму словами.
        В функцію передаємо один аргумент: number -- тризначне число (може бути як int так str)
        Функція повертає результат str"""
def convert_number_under_1000_2_text(number):
    """ Формуємо необхідні списки значень """
    one_to_nineteen = (u'нуль', u'один', u'два', u'три', u'чотири', u'п\'ять',
                       u'шість', u'сім', u'вісім', u'дев\'ять',u'десять',
                       u'одиннадцять', u'дванадцять', u'тринадцять', u'чотирнадцять', u'п\'ятнадцять',
                       u'шістнадцять', u'сімнадцять', u'вісімнадцять', u'девятнадцять')

    decs = ('', u'десять', u'двадцять', u'тридцять', u'сорок', u'п\'ятдесят',
            u'шістдесять', u'сімдесять', u'вісімдесять', u'дев\'яносто')

    hundreds = ('', u'сто', u'двісті', u'триста', u'чотириста', u'п\'ятсот',
                u'шістсот', u'сімсот', u'вісімсот', u'дев\'ятсот')

    """ Локалізуємо змінні """
    number_str = str(number)
    number_int = int(number)

    """ Обнулюємо результат """
    result = ''

    """ Обраховуємо результат """
    if number_int > 99:
        result += hundreds[int(number_str[0])] + ' '

    if number_int > 19 and int(number_str[-2:]) >= 20:
        result += decs[int(number_str[-2])] + ' '
        if int(number_str[-1]):
            result += one_to_nineteen[int(number_str[-1])] + ' '

    if 0 < int(number_str[-2:]) < 20:
        result += one_to_nineteen[int(number_str[-2:])] + ' '

    if number_int == 0:
        result = one_to_nineteen[0] + ' '


    return result

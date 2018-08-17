from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response
from dashboard.models import UserProfile, GraphNames, EREAccounts
from dashboard.forms import UploadFileForm
from django.db import IntegrityError

import copy
from io import TextIOWrapper
import csv
from django.utils import timezone
from dateutil import parser
import pytz

from bokeh.embed import server_session
from bokeh.util import session_id

def get_access_level(user_id):
    return UserProfile.objects.get(user__id__exact=user_id).access_level

def build_access_context(context, request):
    c = copy.deepcopy(context)
    user_id = request.user.id
    access_level = get_access_level(user_id)
    graphs = GraphNames.objects.all().order_by('displayorder')
    c['access_level'] = access_level
    access = []
    for g in graphs:
        if g.required_access_level <= access_level and g.active:
            access.append([g.url_name,g.long_name])
    c['graphs'] = access
    return c


def validate_view(request, url_name):
    try:
        user_id = request.user.id
        access_level = get_access_level(user_id)
        graph_accesslevel = GraphNames.objects.get(url_name=url_name).required_access_level
        return access_level >= graph_accesslevel
    except:
        return False


@login_required
def home(request):
    context = build_access_context({},request)
    return render(request, 'dashboard/home.html', context)

@login_required
def transactions(request):
    if validate_view(request, '820transactions'):
        bokeh_server_url = "%sbokehproxy/820transactions" % (request.build_absolute_uri(location='/'))
        transactions_script = server_session(None, session_id=session_id.generate_session_id(), url=bokeh_server_url)
        context = {"graphname": "820 Transactions",
                   "server_script": transactions_script,
                   }
        context = build_access_context(context, request)
        return render(request, 'dashboard/dynamicsingle.html', context)
    else:
        return redirect('home')

@login_required
def upload_accounts(request):
    if validate_view(request, 'upload'):
        context = build_access_context({}, request)
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                upload_message = insert_erea(request)
                context = build_access_context({'upload_message': upload_message}, request)
            else:
                context = build_access_context({'upload_message': "Choose a CSV file to upload"}, request)
            return render(request, 'dashboard/upload_accounts.html', context)
        return render(request, 'dashboard/upload_accounts.html', context)
    else:
        return redirect('home')

def view_404(request):
    # make a redirect to homepage
    return redirect('home') # or redirect('name-of-index-url')

def insert_erea(request):
    f = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
    timestamp = timezone.now()
    try:
        accounts = []
        csvreader = csv.reader(f, delimiter='!')
        isheaderrow = True
        for row in csvreader:
            if isheaderrow:
                isheaderrow = False
            else:
                if str(row[0]).lower() == 'key':
                    # skip because it's the header
                    pass
                else:
                    accounts.append(EREAccounts(
                        DocumentTrackingNumber = row[0],
                        OriginalDocumentID = float(row[1]),
                        MarketerDUNS = row[2],
                        UtilityDUNS = pytz.utc.localize(parser.parse(row[3])),
                        PaymentDueDate = row[4],
                        ESIID = row[5],
                        InvoiceTotalAmount = row[6],
                        Processed = row[7],
                        updateuser = request.user,
                        updatedatatime = timestamp,
                    )
                    )
        # remove all existing records
        EREAccounts.objects.all().delete()
        # add new records
        EREAccounts.objects.bulk_create(accounts)
        return "Successfully Uploaded"
    except IntegrityError as e:
        return "Duplicate ForeignKey: " + str(e)
    except:
        return "Unknown Upload Error. Check the format of your file. It should be a CSV file with specific columns."

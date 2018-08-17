from mysite import branding

def application_company(request):
    return {'application_company': branding.APPLICATION_COMPANY}

def application_name(request):
    return {'application_name': branding.APPLICATION_NAME}

def version_number(request):
    return {'version_number': branding.VERSION_NUMBER}

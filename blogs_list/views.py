import os
import random

from django.shortcuts import render

from gsoc.models import (
    GsocYear,
    UserProfile
)
from gsoc.settings import MEDIA_URL

from cms.models import Page


def list_blogs(request):
    gsoc_years = GsocYear.objects.all().order_by('-gsoc_year')

    blogsets = []
    for year in gsoc_years:
        profiles = UserProfile.objects.filter(gsoc_year=year)
        flag = False

        blogset = []
        for profile in profiles:
            if profile.app_config:
                flag = True
                ns = profile.app_config.namespace
                page = Page.objects.filter(application_namespace=ns)
                page = page.filter(publisher_is_draft=False).first()
                student_name = profile.user.get_full_name()
                student_username = profile.user.username
                proposal_name = profile.accepted_proposal_pdf.name
                proposal_path = os.path.join(MEDIA_URL, proposal_name)

                blogset.append({
                    'title': profile.app_config.app_title,
                    'url': page.get_absolute_url(),
                    'student': student_name if student_name else student_username,
                    'suborg': profile.suborg_full_name.suborg_name,
                    'color': random.choice(['umber', 'khaki', 'wine', 'straw']),
                    'proposal': proposal_path if proposal_name else None,
                    })

        if flag:
            blogsets.append((year.gsoc_year, blogset))

    err = "No blogs currently! Please visit again later." if not blogsets else None

    return render(request, 'list_view.html', {
        'blogsets': blogsets,
        'errors': [err]
        })

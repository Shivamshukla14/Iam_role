from __future__ import annotations

import json
from typing import Any

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST
from django.middleware.csrf import get_token


@login_required
def index(request: HttpRequest) -> HttpResponse:
    # Ensure CSRF cookie is set for JS fetch POSTs
    get_token(request)
    return render(request, 'dashboard/index.html')


@login_required
@require_GET
def api_active_employees(request: HttpRequest) -> JsonResponse:
    # Placeholder for DB query; for now, return dummy data sorted A-Z by fields where applicable
    data = [
        {
            "emp_code": "E001",
            "login": "alice.w",
            "birth_date": "1990-05-12",
            "first_name": "Alice",
            "last_name": "Walker",
            "entity_name": "PerceptiveWay Pvt Ltd",
            "internal_designation": "SE2",
            "external_designation": "Software Engineer",
            "employer_status": "A",
            "last_work_date": None,
            "date_of_join": "2021-03-01",
            "business_email": "alice.walker@example.com",
            "office_mobile": "+1-202-555-0101",
            "personal_mobile": "+1-202-555-0191",
            "created_on": "2023-01-01T10:00:00Z",
            "modified_on": "2025-09-01T12:00:00Z",
            "num": 123,
        },
        {
            "emp_code": "E002",
            "login": "bob.s",
            "birth_date": "1988-11-30",
            "first_name": "Bob",
            "last_name": "Singh",
            "entity_name": "PerceptiveWay Pvt Ltd",
            "internal_designation": "SE1",
            "external_designation": "Developer",
            "employer_status": "A",
            "last_work_date": None,
            "date_of_join": "2022-06-15",
            "business_email": "bob.singh@example.com",
            "office_mobile": "+1-202-555-0102",
            "personal_mobile": "+1-202-555-0192",
            "created_on": "2023-02-02T11:00:00Z",
            "modified_on": "2025-08-17T09:30:00Z",
            "num": 456,
        },
    ]
    return JsonResponse({"results": data})


@login_required
@require_GET
def api_pending_recertifications(request: HttpRequest) -> JsonResponse:
    data = [
        {
            "emp_code": "E010",
            "login": "john.d",
            "birth_date": "1992-02-20",
            "first_name": "John",
            "last_name": "Doe",
            "entity_name": "PerceptiveWay Pvt Ltd",
            "internal_designation": "SSE",
            "external_designation": "Senior Engineer",
            "employer_status": "A",
            "last_work_date": None,
            "date_of_join": "2020-09-01",
            "business_email": "john.doe@example.com",
            "office_mobile": "+1-202-555-0130",
            "personal_mobile": "+1-202-555-0180",
            "created_on": "2023-03-03T12:00:00Z",
            "modified_on": "2025-08-31T08:00:00Z",
            "num": 789,
        },
        {
            "emp_code": "E011",
            "login": "jane.p",
            "birth_date": "1991-07-10",
            "first_name": "Jane",
            "last_name": "Perez",
            "entity_name": "PerceptiveWay Pvt Ltd",
            "internal_designation": "QA2",
            "external_designation": "QA Engineer",
            "employer_status": "A",
            "last_work_date": None,
            "date_of_join": "2019-01-20",
            "business_email": "jane.perez@example.com",
            "office_mobile": "+1-202-555-0131",
            "personal_mobile": "+1-202-555-0181",
            "created_on": "2023-04-04T13:00:00Z",
            "modified_on": "2025-08-30T15:45:00Z",
            "num": 101,
        },
    ]
    return JsonResponse({"results": data})


@login_required
@require_POST
def api_recertify(request: HttpRequest) -> JsonResponse:
    try:
        payload: dict[str, Any] = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)

    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    business_email = payload.get("business_email")

    if not (first_name and last_name and business_email):
        return JsonResponse({"ok": False, "error": "Missing required fields"}, status=400)

    full_name = f"{first_name} {last_name}".strip()

    # Compose approval email (dummy SMTP configured in settings)
    subject = f"Recertification Approval Needed: {full_name}"
    context = {
        "full_name": full_name,
        "business_email": business_email,
        "requested_by": request.user.get_username(),
    }
    text_body = render_to_string("emails/approval.txt", context)
    html_body = render_to_string("emails/approval.html", context)

    msg = EmailMultiAlternatives(subject, text_body, to=[business_email])
    msg.attach_alternative(html_body, "text/html")
    try:
        msg.send(fail_silently=False)
        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=500)

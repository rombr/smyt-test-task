import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.forms.models import model_to_dict
from django.forms import ModelForm

from .utils import get_models_config, default_for_date
from . import models as app_models


MODELS = get_models_config()


def home(request):
    """
    Index page
    """
    return render(request, "foo/index.html", {"models": MODELS})


def api(request, model_name):
    """
    Data API
    """
    if model_name not in MODELS:
        raise Http404()

    Model = getattr(app_models, model_name.capitalize())

    # Add new object
    if request.method == "POST":

        class Form(ModelForm):
            class Meta:
                model = Model
                fields = "__all__"

        form = Form(request.POST)
        if form.is_valid():
            instance = form.save()
        else:
            return HttpResponseBadRequest()

        return HttpResponse(
            json.dumps(
                {
                    "schema": MODELS[model_name],
                    "data": model_to_dict(instance),
                },
                default=default_for_date,
            ),
            content_type="application/json",
        )

    return HttpResponse(
        json.dumps(
            {
                "schema": MODELS[model_name],
                "data": [model_to_dict(i) for i in Model.objects.all()],
            },
            default=default_for_date,
        ),
        content_type="application/json",
    )


def api_details(request, model_name, object_id):
    """
    Object details and edit
    """
    object_id = int(object_id)

    if model_name not in MODELS:
        raise Http404()

    Model = getattr(app_models, model_name.capitalize())
    obj = get_object_or_404(Model, pk=object_id)

    # Edit object
    if request.method == "POST":

        class Form(ModelForm):
            class Meta:
                model = Model
                fields = set(request.POST.keys()) & set(
                    [i.get("id") for i in MODELS[model_name].get("fields", [])]
                )

        form = Form(request.POST, instance=obj)
        if form.is_valid():
            instance = form.save()
        else:
            return HttpResponseBadRequest()

        return HttpResponse(
            json.dumps(
                {
                    "schema": MODELS[model_name],
                    "data": model_to_dict(instance),
                },
                default=default_for_date,
            ),
            content_type="application/json",
        )

    return HttpResponse(
        json.dumps(
            {
                "schema": MODELS[model_name],
                "data": model_to_dict(obj),
            },
            default=default_for_date,
        ),
        content_type="application/json",
    )

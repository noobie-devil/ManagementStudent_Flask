from my_app import db,app
from my_app.models import *
from flask import Flask, render_template, redirect, url_for, flash, request, json
from flask_admin import Admin
from my_app import admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.model.fields import InlineModelFormField, InlineFormField, InlineFieldList
from wtforms.utils import unset_value
from wtforms import form,fields
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_wtf import FlaskForm
from my_app.forms import *
from flask_admin.helpers import (get_form_data, validate_form_on_submit, get_redirect_target, flash_errors)
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.contrib.sqla.filters import BaseSQLAFilter, FilterEqual, ChoiceTypeEqualFilter
from flask_admin.model.template import EndpointLinkRowAction
from datetime import datetime
from sqlalchemy import func
from flask_admin.model.template import TemplateLinkRowAction
from flask_admin.form.widgets import Select2Widget
from flask_wtf.file import FileField, FileAllowed
import cloudinary
import cloudinary.uploader
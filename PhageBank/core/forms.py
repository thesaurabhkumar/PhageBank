from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from PhageBank.core.models import PhageData, ExperimentData, IsolationData
from crispy_forms.helper import FormHelper
from django.core.urlresolvers import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, Accordion, AccordionGroup
from crispy_forms.layout import Submit, Layout, Div, Fieldset, MultiField
from crispy_forms.layout import Submit, Reset, HTML
from crispy_forms.layout import Button
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.formsets import BaseFormSet


def validate_file_extension(value):
    if not value.name.endswith('.csv'):
        raise ValidationError(u'File In  CSV format Only')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField(validators=[validate_file_extension])

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password",)

class Add_Phage_DataForm(forms.ModelForm):
    phage_name = forms.CharField(label='Phage Name',
                                 max_length=30,
                                 required=True,
                                 help_text='Required.',
                                 widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                               'autocomplete': 'off',
                                                               'size': '100',
                                                               'style': 'font-size: small',
                                                               })
                                 )

    phage_host_name = forms.CharField(label='Host Name',
                                      max_length=30,
                                      required=False,
                                      help_text='Required.',
                                      widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                    'autocomplete': 'off',
                                                                    'size': '100',
                                                                    'style': 'font-size: small',
                                                                    })
                                      )

    class Meta:
        model = PhageData
        fields = ("phage_name", "phage_host_name",)

class Add_ResearcherForm(forms.ModelForm):
    phage_isolator_name = forms.CharField(label='Isolator Name',
                                          max_length=30,
                                          required=False,
                                          help_text='Required.',
                                          widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                        'autocomplete': 'off',
                                                                        'size': '100',
                                                                        'style': 'font-size: small',
                                                                        })
                                          )

    phage_experimenter_name = forms.CharField(label='Experimenter Name',
                                              max_length=30,
                                              required=False,
                                              help_text='Required.',
                                              widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                            'autocomplete': 'off',
                                                                            'size': '100',
                                                                            'style': 'font-size: small',
                                                                            })
                                              )
    INCIDENT_LIVE = (
        ('0', 'Lab-A'),
        ('1', 'Lab-B'),
    )
    phage_lab = forms.CharField(label='Select your Lab', widget=forms.Select(choices=INCIDENT_LIVE))
    class Meta:
        model = PhageData
        fields = ("phage_isolator_name", "phage_experimenter_name","phage_lab",)

class Add_ResearchForm(forms.ModelForm):
    phage_CPT_id = forms.CharField(label='CPT id',
                                   max_length=30,
                                   required=True,
                                   help_text='Required.',
                                   widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                 'autocomplete': 'off',
                                                                 'size': '100',
                                                                 'style': 'font-size: small',
                                                                 })
                                   )

    phage_isolator_loc = forms.CharField(label='Isolator Location',
                                         max_length=5000,
                                         required=False,
                                         help_text='Required.',
                                         widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                       'autocomplete': 'off',
                                                                       'size': '100',
                                                                       'style': 'font-size: small',
                                                                       })
                                         )

    class Meta:
        model = PhageData
        fields = ("phage_CPT_id", "phage_isolator_loc",)

class Add_Experiment_Form(forms.ModelForm):
    owner = forms.CharField(label='Owner',
                                 max_length=100,
                                 required=False,
                                 widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                               'autocomplete': 'off',
                                                               'size': '100',
                                                               'style': 'font-size: small',
                                                               })
                                 )

    TimeStamp = forms.DateField(label='Date of Experiment',required=False,
                                    widget=forms.DateInput(attrs={'autofocus': 'autofocus',
                                                                      'type': 'date'}))

    category = forms.CharField(label='Category',
                               max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                             'autocomplete': 'off',
                                                             'size': '100',
                                                             'style': 'font-size: small',
                                                             })
                               )

    short_name = forms.CharField(label='Short Name',
                               max_length=100,
                               required=False,
                               widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                             'autocomplete': 'off',
                                                             'size': '100',
                                                             'style': 'font-size: small',
                                                             })
                               )

    full_name = forms.CharField(label='Full Name',
                               max_length=5000,
                               required=False,
                               widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                             'autocomplete': 'off',
                                                             'size': '5000',
                                                             'style': 'font-size: small',
                                                             })
                               )

    methods = forms.CharField(label='Methods',
                               max_length=5000,
                               required=False,
                               widget=forms.Textarea(attrs={'autofocus': 'autofocus',
                                                             'autocomplete': 'off',
                                                             'size': '5000',
                                                             'style': 'font-size: small',
                                                             })
                               )

    results = forms.CharField(label='Results',
                               max_length=5000,
                               required=False,
                               widget=forms.Textarea(attrs={'autofocus': 'autofocus',
                                                             'autocomplete': 'off',
                                                             'size': '5000',
                                                             'style': 'font-size: small',
                                                             })
                               )

    class Meta:
        model = ExperimentData
        fields = ("owner", "TimeStamp","category","short_name","full_name","methods","results")

class Isolation_Form(forms.Form):
    owner_name = forms.CharField(label='Owner',
                            max_length=100,
                            required=False,
                            widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                          'autocomplete': 'off',
                                                          'size': '100',
                                                          'style': 'font-size: small',
                                                          })
                            )

    location = forms.CharField(label='Location',
                            max_length=100,
                            required=False,
                            widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                          'autocomplete': 'off',
                                                          'size': '100',
                                                          'style': 'font-size: small',
                                                          })
                            )

    type1 = forms.CharField(label='Type',
                            max_length=100,
                            required=False,
                            widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                          'autocomplete': 'off',
                                                          'size': '100',
                                                          'style': 'font-size: small',
                                                          })
                            )

    timestamp = forms.DateField(label='Date of Experiment',required=False,
                                    widget=forms.DateInput(attrs={'autofocus': 'autofocus',
                                                                      'type': 'date'}))

    class Meta:
        model= IsolationData
        fields = {'owner_name', 'location', 'type1', 'timestamp'}


class LinkForm(forms.Form):
    link = forms.CharField(label='URL',
                                      max_length=5000,
                                      required=False,
                                      help_text='',
                                      widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                    'autocomplete': 'off',
                                                                    'size': '100',
                                                                    'style': 'font-size: small',
                                                                    })
                                      )



class AForm(forms.Form):
    image = forms.ImageField(label='Upload Image', required=False, widget=forms.FileInput())

    doc = forms.FileField(label='Upload File', required=False, widget=forms.FileInput())



class AIForm(forms.Form):
    link = forms.CharField(label='URL',
                                      max_length=5000,
                                      required=False,
                                      help_text='',
                                      widget=forms.TextInput(attrs={'autofocus': 'autofocus',
                                                                    'autocomplete': 'off',
                                                                    'size': '100',
                                                                    'style': 'font-size: small',
                                                                    })
                                      )

class Edit_Phage_DataForm(forms.ModelForm):
    phage_name = forms.CharField(required=True,)
    phage_host_name = forms.CharField(required=False,)
    class Meta:
        model = PhageData
        fields = ('phage_name', 'phage_host_name',)

class Edit_ResearcherForm(forms.ModelForm):
    phage_isolator_name = forms.CharField(required=False,)
    phage_experimenter_name = forms.CharField(required=False,)
    INCIDENT_LIVE = (
        ('0', 'Lab-A'),
        ('1', 'Lab-B'),
    )
    phage_lab = forms.ChoiceField(choices=INCIDENT_LIVE)

    class Meta:
        model = PhageData
        fields = ("phage_isolator_name", "phage_experimenter_name","phage_lab")

class Edit_ResearchForm(forms.ModelForm):
    phage_CPT_id = forms.CharField(required=True,)
    phage_isolator_loc = forms.CharField(required=False,)
    class Meta:
        model = PhageData
        fields = ("phage_CPT_id", "phage_isolator_loc",)

class Edit_IsolationDataForm(forms.ModelForm):
    TimeStamp = forms.DateField(label='Date of Experiment',required=False,
                                    widget=forms.DateInput(attrs={'autofocus': 'autofocus',
                                                                      'type': 'date'}))
    owner_name = forms.CharField(required=False,)
    location = forms.CharField(required=False,)
    type = forms.CharField(required=False,)

    class Meta:
        model = IsolationData
        fields = ('owner_name', 'location', 'type', 'TimeStamp')

class Edit_Experiment_Form(forms.ModelForm):
    owner = forms.CharField(label='Owner',
                                 max_length=100,
                                 required=False,)

    timestamp = forms.DateField(label='Date of Experiment',required=False,
                                    widget=forms.DateInput(attrs={'autofocus': 'autofocus',
                                                                      'type': 'date'}))

    category = forms.CharField(required=False,)

    short_name = forms.CharField(required=False,)

    full_name = forms.CharField(required=False,)

    methods = forms.CharField(label='Methods',
                               max_length=5000,
                               required=False,)

    results = forms.CharField(label='Results',
                               max_length=5000,
                               required=False,)

    class Meta:
        model = ExperimentData
        fields = ("owner", "timestamp","category","short_name","full_name","methods","results")




import unicodedata
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return (
        unicodedata.normalize("NFKC", s1).casefold()
        == unicodedata.normalize("NFKC", s2).casefold()
    )
def get_users(email):
    """Given an email, return matching user(s) who should receive a reset.

    This allows subclasses to more easily customize the default policies
    that prevent inactive users and users with unusable passwords from
    resetting their password.
    """
    UserModel=User;
    email_field_name = UserModel.get_email_field_name()
    active_users = UserModel._default_manager.filter(
        **{
            "%s__iexact" % email_field_name: email,
            "is_active": True,
        }
    )
    return (
        u
        for u in active_users
        if u.has_usable_password()
           and _unicode_ci_compare(email, getattr(u, email_field_name))
    )
def send_mail(
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()
def prepare_mail(email,request):
    email_field_name = User.get_email_field_name()
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    token_generator = default_token_generator
    for user in get_users(email):
        user_email = getattr(user, email_field_name)
        context = {
            "email": user_email,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": "http" ,
            **( {}),
        }
        from_email=None
        subject_template_name = "registration/password_reset_subject.txt"
        email_template_name = "registration/password_reset_email.html"
        html_email_template_name = None
        send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            user_email,
            html_email_template_name,
        )
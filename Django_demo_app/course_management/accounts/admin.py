"""This file is used to register the models in the admin panel."""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import CustomUser, UserAddress, UserPayment


class DateInput(forms.DateInput):
    """Custom date input widget."""

    input_type = 'date'
    format = '%Y-%m-%d'


class UserAddressInline(admin.StackedInline):
    """Inline admin interface for user addresses."""

    model = UserAddress
    extra = 1
    fields = ('postal_code', 'country', 'city', 'street')


class UserPaymentInline(admin.TabularInline):
    """Inline admin interface for user payments."""

    model = UserPayment
    extra = 0
    fields = ('amount', 'payment_method', 'payment_date')
    readonly_fields = ('payment_date',)


class CustomUserCreationForm(forms.ModelForm):
    """Form for creating new users."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        """Meta options for the CustomUserCreationForm."""

        model = CustomUser
        fields = ('email', 'phone_number', 'first_name', 'last_name',
                  'date_of_birth', 'profile_picture')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }

    def clean_password2(self):
        """Check that the two password entries match.

        Raises:
            ValidationError: If the two password entries do not match.

        Returns:
            str: The second password entry if valid.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        """Save the user with the provided password.

        Args:
            commit (bool): Whether to save the user immediately.

        Returns:
            CustomUser: The created user instance.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data('password1'))
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """Form for updating existing users."""

    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text='Encrypted password. <a href="../password/">Change</a>',
    )
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        required=False,
        help_text='Leave blank to keep the same password.',
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        """Meta options for the CustomUserChangeForm."""

        model = CustomUser
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }

    def clean_password(self):
        """Clean the password field and ensure the two password entries match.

        Raises:
            ValidationError: If the two password entries do not match.

        Returns:
            dict: The cleaned data with the password field.
        """
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("Passwords don't match")

        return cleaned_data

    def save(self, commit=True):
        """Save the user with the provided password.

        Args:
            commit (bool): Whether to save the user immediately.

        Returns:
            CustomUser: The updated user instance.
        """
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get('new_password1')
        if new_password1:
            user.set_password(new_password1)
        if commit:
            user.save()
        return user


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin interface for managing custom user model."""

    inlines = [UserAddressInline, UserPaymentInline]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'full_name', 'phone_number',
                    'is_active', 'is_staff', 'payment_total', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'preferred_language')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    actions = ['activate_users', 'deactivate_users',
               'make_staff', 'unmake_staff']
    list_per_page = 10

    fieldsets = (
        (None, {'fields': ('email', 'is_active')}),
        ('Change Password', {
            'fields': ('new_password1', 'new_password2'),
            'classes': ('collapse',)}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number',
                       'date_of_birth', 'profile_picture'),
            'classes': ('wide',)}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'phone_number', 'password1', 'password2',
                'first_name', 'last_name', 'date_of_birth'),
        }),
    )

    def full_name(self, obj):
        """Full name of the user.

        Args:
            obj (CustomUser): The user object.

        Returns:
            str: The full name of the user.
        """
        return f'{obj.first_name} {obj.last_name}'
    full_name.short_description = 'Full Name'

    def payment_total(self, obj):
        """Calculate the total payment amount for the user.

        Args:
            obj (CustomUser): The user object.

        Returns:
            float: The total payment amount.
        """
        total = sum(payment.amount for payment in obj.payments.all())
        return f'{total:.2f} USD'
    payment_total.short_description = 'Total Payment Amount'

    def deactivate_users(self, request, queryset):
        """Deactivate selected users.

        Args:
            request (HttpRequest): The request object.
            queryset (QuerySet): The selected user queryset.
        """
        updated = queryset.update(is_active=False)
        self.message_user(
            request, f'Selected users {updated} have been deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'

    def activate_users(self, request, queryset):
        """Activate selected users.

        Args:
            request (HttpRequest): The request object.
            queryset (QuerySet): The selected user queryset.
        """
        updated = queryset.update(is_active=True)
        self.message_user(
            request, f'Selected users {updated} have been activated.')
    activate_users.short_description = 'Activate selected users'

    def make_staff(self, request, queryset):
        """Make selected users staff.

        Args:
            request (HttpRequest): The request object.
            queryset (QuerySet): The selected user queryset.
        """
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'Selected users {updated} are now staff.')
    make_staff.short_description = 'Make selected users staff'

    def unmake_staff(self, request, queryset):
        """Remove staff status from selected users.

        Args:
            request (HttpRequest): The request object.
            queryset (QuerySet): The selected user queryset.
        """
        updated = queryset.update(is_staff=False)
        self.message_user(
            request, f'Selected users {updated} are no longer staff.')
    unmake_staff.short_description = 'Remove staff status from selected users'


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """Admin interface for managing user addresses."""

    list_display = ('user', 'postal_code', 'country', 'city', 'street')
    list_filter = ('city', 'postal_code')
    search_fields = ('user__email', 'country', 'city')


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    """Admin interface for managing user payments."""

    list_display = ('user', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('user__email', 'payment_method')
    ordering = ('-payment_date',)
